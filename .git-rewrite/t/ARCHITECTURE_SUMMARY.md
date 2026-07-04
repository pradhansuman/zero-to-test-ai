# Services Layer Architecture - Executive Summary

## Problem Statement

The current FastAPI backend violates separation of concerns:
- **Routes** contain database queries, business logic, and validation
- **Models** are ORM objects; no schema validation layer
- **No transaction management** — unclear when data persists
- **Critical security bugs**: plaintext passwords, hardcoded user IDs, no ownership checks
- **No audit logging** — can't trace who changed what
- **Hard to test** — routes coupled to database layer

## Solution: Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│  HTTP Layer (Routes)                                    │
│  Thin handlers: parse input, call service, return JSON  │
└────────────────────────────────────────────────────────┬┘
                                                           │
┌──────────────────────────────────────────────────────────▼─┐
│  Business Logic Layer (Services)                          │
│  Validation, authorization, transactions, domain logic   │
└──────────────────────────────────────────────────────────┬─┘
                                                            │
┌─────────────────────────────────────────────────────────┬┘
│  Data Access Layer (Repositories)                       │
│  Abstract SQL queries, return domain objects            │
└──────────────────────────────────────────────────────────┘
```

## Key Architectural Decisions

| Decision | Benefit |
|----------|---------|
| **Repository Pattern** | Abstracts database; enables testing without DB; easy schema migrations |
| **Service Layer** | Centralizes business logic; reusable across routes; testable in isolation |
| **Explicit Transactions** | Services own commit/rollback; prevents data loss; easier debugging |
| **Domain Exceptions** | Services never know about HTTP; easy to reuse in CLI or workers |
| **Request-scoped Context** | Logs include request_id + user_id; can trace any issue across services |
| **Immutable Updates** | No hidden side effects; safe for async; prevents race conditions |
| **Lazy Repository Factory** | Only creates repos when needed; reduces object allocation |

## File Structure

```
backend/app/
├── routes/                         # HTTP handlers (thin)
│   ├── __init__.py
│   ├── auth.py                     # 3 auth endpoints
│   ├── projects.py                 # 5 project endpoints
│   ├── test_cases.py               # 2 test case endpoints
│   └── executions.py               # 2 execution endpoints
│
├── services/                       # Business logic (thick)
│   ├── __init__.py
│   ├── base_service.py             # Transaction + logging base
│   ├── auth_service.py             # Password hashing, JWT generation
│   ├── project_service.py          # CRUD + ownership validation
│   ├── test_case_service.py        # Test case management
│   └── execution_service.py        # Orchestration, result aggregation
│
├── repositories/                   # Data access (abstract)
│   ├── __init__.py                 # RepositoryFactory
│   ├── base.py                     # BaseRepository with CRUD
│   ├── user_repository.py
│   ├── project_repository.py
│   ├── test_case_repository.py
│   ├── execution_repository.py
│   ├── execution_result_repository.py
│   ├── report_repository.py
│   └── audit_log_repository.py
│
├── database/
│   ├── models.py                   # SQLAlchemy ORM
│   ├── session.py
│   └── base.py
│
├── models/
│   └── schemas.py                  # Pydantic request/response
│
├── utils/
│   ├── logger.py                   # Structured logging with context
│   └── ...
│
├── exceptions.py                   # Domain exceptions (not HTTP)
├── dependencies.py                 # DI: services, JWT, current_user
├── config.py                       # Settings
├── main.py                         # FastAPI app + middleware
└── ...
```

## Data Flow Example: Create Project

```
HTTP POST /api/projects
│
├─ Route Handler
│  └─ Parse ProjectCreate
│  └─ Extract user_id from JWT (get_current_user dependency)
│  └─ Call ProjectService.create(user_id, data)
│
├─ ProjectService.create()
│  ├─ Validate name (not empty, length <= 255)
│  ├─ Check duplicate: repos.projects.find_by_name(user_id, name)
│  ├─ If duplicate: raise ValidationError(422)
│  ├─ Create: repos.projects.create(name, description, owner_id, framework)
│  │  └─ ProjectRepository.create()
│  │     └─ new_project = Project(...)
│  │     └─ session.add(new_project)
│  │     └─ session.flush() [no commit yet]
│  ├─ Commit: await session.commit()
│  ├─ Log: _log_action("create", "project", project.id, user_id)
│  └─ Return Project instance
│
└─ Route Handler
   └─ Convert Project to ProjectResponse Pydantic
   └─ Return JSON (201 Created)
```

## Security Improvements

### Before (Current Code)

```python
# WRONG: Plaintext password
new_user = User(email=email, password_hash=password)  # password, not hash!

# WRONG: Hardcoded owner
new_project = Project(owner_id=1)  # User 1 owns everything

# WRONG: No ownership check
projects = db.query(Project).all()  # Anyone sees all projects

# WRONG: No validation
if project_data.name:  # Empty string is falsy but allowed
    project.name = project_data.name
```

### After (Services Layer)

```python
# RIGHT: Bcrypt hash
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# RIGHT: From authenticated user
owner_id = current_user["id"]  # From JWT token

# RIGHT: Ownership check
project = await self.get(user_id, project_id)  # Raises Unauthorized if not owner

# RIGHT: Validation
if len(data.name.strip()) == 0:
    raise ValidationError("Name cannot be empty")
```

## Transaction Management

### Explicit Commit in Service

```python
async def create(self, data):
    # Operations
    instance = await self.repos.model.create(**data)
    # Explicit commit
    await self.commit()  # Here is where data persists
    return instance
```

### Automatic Rollback on Error

```python
async def commit(self):
    try:
        await self.session.commit()
    except Exception as e:
        await self.session.rollback()  # Auto-rollback
        self.logger.error(f"Transaction failed: {e}")
        raise
```

### Multi-Entity Transactions

```python
async def start_execution(self, project_id, test_case_ids):
    # Create execution
    execution = await self.repos.executions.create(project_id=project_id, ...)
    
    # Create results
    for tc_id in test_case_ids:
        await self.repos.execution_results.create(execution_id=execution.id, ...)
    
    # Single commit for all
    await self.commit()  # All or nothing
```

## Error Handling Strategy

### Services Raise Domain Exceptions

```python
from backend.app.exceptions import (
    ValidationError,    # 422 Unprocessable Entity
    NotFound,           # 404 Not Found
    Unauthorized,       # 403 Forbidden
    AuthException       # 401 Unauthorized
)

if not user:
    raise NotFound("User")  # Becomes 404

if user.owner_id != current_user_id:
    raise Unauthorized("You don't own this")  # Becomes 403
```

### Routes Never Catch

FastAPI automatically converts exceptions to HTTP responses:

```python
@app.get("/api/projects/{id}")
async def get_project(id: int, service: ProjectService = Depends(...)):
    return await service.get(current_user["id"], id)
    # If NotFound raised → 404 JSON
    # If Unauthorized raised → 403 JSON
    # If ValidationError raised → 422 JSON
```

## Logging & Observability

### Structured Context

Every log includes request_id and user_id:

```
[2024-01-15 10:23:45] INFO [req-abc123] [user:42] project_service: Project created (ID: 1)
[2024-01-15 10:23:46] INFO [req-abc123] [user:42] execution_service: Execution started (ID: 5)
[2024-01-15 10:23:47] ERROR [req-abc123] [user:42] execution_service: Test failed: assertion error
```

### Audit Trail

```python
self._log_action("create", "project", project_id, user_id)
# Logged to audit_logs table for compliance/debugging
```

## Testing Strategy

### Unit Test (Service with Mocked Repository)

```python
@pytest.mark.asyncio
async def test_create_project_validates_name():
    # Arrange
    mock_session = AsyncMock()
    service = ProjectService(mock_session)
    service.repos.projects.find_by_name = AsyncMock(return_value=None)
    
    # Act
    with pytest.raises(ValidationError) as exc:
        await service.create(user_id=1, data=ProjectCreate(name=""))
    
    # Assert
    assert "cannot be empty" in str(exc.value)
```

### Integration Test (Real Database)

```python
@pytest.mark.asyncio
async def test_create_and_list_projects_flow(async_db):
    service = ProjectService(async_db)
    
    # Create
    project = await service.create(1, ProjectCreate(name="Test"))
    
    # List
    projects = await service.list_by_owner(1)
    
    # Assert
    assert project.id in [p.id for p in projects]
```

### E2E Test (Full HTTP Stack)

```python
def test_create_project_e2e(client, auth_token):
    response = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"name": "Test Project"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
```

## Implementation Roadmap

### Phase 1: Repositories (2 days)
- [ ] Create BaseRepository in `base.py`
- [ ] Implement 8 concrete repositories
- [ ] Create RepositoryFactory
- [ ] Unit test each repository with mocked session

### Phase 2: Services (3 days)
- [ ] Create BaseService with transaction + logging
- [ ] Implement AuthService (password hashing, JWT)
- [ ] Implement ProjectService (CRUD + validation)
- [ ] Implement TestCaseService
- [ ] Implement ExecutionService
- [ ] Unit test each service with mocked repositories

### Phase 3: Routes & DI (2 days)
- [ ] Update `dependencies.py` with service factories
- [ ] Split routes into separate files
- [ ] Update `main.py` to import routes
- [ ] Update `exceptions.py` with domain exceptions
- [ ] Integration tests for each route

### Phase 4: Polish (1 day)
- [ ] Add structured logging middleware
- [ ] Update error responses
- [ ] Add request ID tracking
- [ ] Documentation and README

## Key Metrics

| Metric | Before | After |
|--------|--------|-------|
| **Lines in main.py** | 189 | ~30 (just imports + middleware) |
| **Code duplication** | High | Low (services reuse logic) |
| **Test coverage** | 0% | 80%+ (services testable in isolation) |
| **Security vulns** | 3+ critical | 0 |
| **Transaction clarity** | Implicit | Explicit |
| **Error messages** | Generic | Specific + helpful |
| **Audit trail** | None | Full history |
| **Request traceability** | None | Logs tagged with request_id |

## Benefits by Stakeholder

### For Developers
- Clear code organization (who does what)
- Easy to test (mock repositories)
- Easy to extend (add new service methods)
- Easy to debug (structured logs, explicit transactions)

### For Operations
- Observable system (request tracing, audit logs)
- Reproducible bugs (full context in logs)
- Safe deployments (transaction safety prevents data loss)
- Faster incident response (know exactly who/what/when)

### For Security
- No plaintext passwords
- All user inputs validated
- Ownership checks on every resource
- Audit trail for compliance
- Error messages don't leak information

### For Product
- Faster feature development (reusable services)
- Higher reliability (transaction safety)
- Better user experience (specific error messages)
- Audit trail for support inquiries

## Appendix: Common Patterns

### Create with Validation

```python
async def create(self, user_id, data):
    # 1. Validate
    if not data.name: raise ValidationError("Name required")
    # 2. Check constraints
    if await self.repos.item.find_one(name=data.name):
        raise ValidationError("Name exists")
    # 3. Create
    item = await self.repos.item.create(**data.dict())
    # 4. Commit
    await self.commit()
    # 5. Log
    self._log_action("create", "item", item.id, user_id)
    return item
```

### Get with Ownership

```python
async def get(self, user_id, item_id):
    item = await self.repos.item.get_by_id(item_id)
    if not item: raise NotFound("Item")
    if item.owner_id != user_id: raise Unauthorized("Not owner")
    return item
```

### Update with Validation

```python
async def update(self, user_id, item_id, data):
    item = await self.get(user_id, item_id)  # Checks ownership
    updates = {}
    if data.name is not None:
        if not data.name: raise ValidationError("Name empty")
        updates["name"] = data.name
    if updates:
        await self.repos.item.update(item_id, **updates)
        await self.commit()
    return item
```

### Multi-Entity Transaction

```python
async def create_complex(self, data):
    # Check prerequisites
    parent = await self.repos.parent.get_by_id(data.parent_id)
    if not parent: raise NotFound("Parent")
    
    # Create entities
    primary = await self.repos.primary.create(parent_id=parent.id, ...)
    for sub in data.subs:
        await self.repos.sub.create(primary_id=primary.id, ...)
    
    # Single commit
    await self.commit()
    return primary
```

## References

- See `SERVICES_ARCHITECTURE.md` for detailed design
- See `IMPLEMENTATION_SCAFFOLD.md` for code templates
- See `ROUTES_TO_SERVICES_MAPPING.md` for 12-route refactoring plan
- See `SERVICES_QUICK_REFERENCE.md` for common patterns
