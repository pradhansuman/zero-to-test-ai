# Services Layer - Quick Reference

## Data Flow

```
1. HTTP Request
   ↓
2. Route Handler (thin, just parsing & calling service)
   ↓
3. Service (validation, business logic, transaction control)
   ↓
4. Repository (abstract data access)
   ↓
5. SQLAlchemy ORM (query execution)
   ↓
6. Database (PostgreSQL)
```

## Common Patterns

### Create with Validation

```python
# Service
async def create(self, user_id: int, data: SomeCreate) -> SomeModel:
    # 1. Validate input
    if not data.name:
        raise ValidationError("Name required")
    
    # 2. Check business constraints
    existing = await self.repos.some.find_one(name=data.name)
    if existing:
        raise ValidationError("Name already exists")
    
    # 3. Create entity
    instance = await self.repos.some.create(**data.dict())
    
    # 4. Commit transaction
    await self.commit()
    
    # 5. Log action
    self._log_action("create", "some", instance.id, user_id)
    
    return instance

# Route
@app.post("/api/some", response_model=SomeResponse)
async def create_some(
    data: SomeCreate,
    current_user: dict = Depends(get_current_user),
    service: SomeService = Depends(get_some_service)
):
    return await service.create(current_user["id"], data)
```

### Get with Ownership Check

```python
# Service
async def get(self, user_id: int, resource_id: int) -> SomeModel:
    # 1. Fetch resource
    resource = await self.repos.some.get_by_id(resource_id)
    if not resource:
        raise NotFound("Resource")
    
    # 2. Check ownership
    if resource.owner_id != user_id:
        raise Unauthorized("You do not own this resource")
    
    return resource

# Route
@app.get("/api/some/{resource_id}")
async def get_some(
    resource_id: int,
    current_user: dict = Depends(get_current_user),
    service: SomeService = Depends(get_some_service)
):
    return await service.get(current_user["id"], resource_id)
```

### Update with Validation

```python
# Service
async def update(self, user_id: int, resource_id: int, data: SomeUpdate) -> SomeModel:
    # 1. Get with ownership check
    resource = await self.get(user_id, resource_id)
    
    # 2. Build update dict with validation
    update_data = {}
    if data.name is not None:
        if not data.name:
            raise ValidationError("Name cannot be empty")
        update_data["name"] = data.name
    
    # 3. Update if any changes
    if update_data:
        await self.repos.some.update(resource_id, **update_data)
        await self.commit()
        self._log_action("update", "some", resource_id, user_id)
    
    return resource

# Route
@app.put("/api/some/{resource_id}")
async def update_some(
    resource_id: int,
    data: SomeUpdate,
    current_user: dict = Depends(get_current_user),
    service: SomeService = Depends(get_some_service)
):
    return await service.update(current_user["id"], resource_id, data)
```

### Multi-Entity Transaction

```python
# Service
async def create_complex_operation(self, user_id: int, data) -> Result:
    # All operations in one transaction
    
    # Check prerequisites
    parent = await self.repos.parent.get_by_id(data.parent_id)
    if not parent:
        raise NotFound("Parent")
    
    # Create primary entity
    primary = await self.repos.primary.create(parent_id=parent.id, ...)
    
    # Create related entities
    for item in data.items:
        await self.repos.items.create(primary_id=primary.id, ...)
    
    # Create audit log
    await self.repos.audit_logs.create(
        user_id=user_id,
        action="create_complex",
        resource_type="primary",
        resource_id=primary.id
    )
    
    # Single commit for all
    await self.commit()
    
    return primary
```

### Custom Query in Repository

```python
# Repository
async def find_by_owner_and_status(self, owner_id: int, status: str) -> List[Model]:
    """Custom query combining filters."""
    stmt = (select(Model)
            .where(and_(Model.owner_id == owner_id, Model.status == status))
            .order_by(desc(Model.created_at)))
    result = await self.session.execute(stmt)
    return result.scalars().all()

# Service
async def list_active_by_owner(self, owner_id: int) -> List[Model]:
    return await self.repos.model.find_by_owner_and_status(owner_id, "active")
```

## Exception Handling

### Service Raises Domain Exceptions

```python
from backend.app.exceptions import (
    ValidationError,    # 422
    NotFound,           # 404
    Unauthorized,       # 403
    AuthException,      # 401
    ConflictError       # 409
)

# In service
if not user:
    raise NotFound("User")

if user.owner_id != current_user_id:
    raise Unauthorized("You don't own this")

if email_already_exists:
    raise ConflictError("Email already registered")

if invalid_input:
    raise ValidationError("Field must be non-empty")
```

### Routes Never Catch

Routes **never** catch exceptions. FastAPI automatically converts them to HTTP responses.

```python
# WRONG - don't catch
@app.get("/api/some/{id}")
async def get_some(id: int, service: Service = Depends(get_service)):
    try:
        return await service.get(id)
    except NotFound:
        raise HTTPException(404)  # Wrong!

# RIGHT - let it propagate
@app.get("/api/some/{id}")
async def get_some(id: int, service: Service = Depends(get_service)):
    return await service.get(id)  # Exception auto-converts to HTTP response
```

## Transaction Control

### Explicit Commits in Services

```python
# RIGHT - service commits
async def create(self, data):
    instance = await self.repos.model.create(**data.dict())
    await self.commit()  # Explicit commit
    return instance

# WRONG - implicit/unclear
async def create(self, data):
    return await self.repos.model.create(**data.dict())
    # When does it commit? Unclear!
```

### Rollback on Error

```python
# Service base class handles this
async def commit(self):
    try:
        await self.session.commit()
    except Exception as e:
        await self.session.rollback()  # Auto-rollback on error
        raise
```

## Logging

### Log with Context

```python
# Set context
from backend.app.utils.logger import set_request_context
set_request_context(request_id="abc123", user_id=42)

# Logs automatically include context
self.logger.info("Project created")
# Output: [timestamp] INFO [abc123] [user:42] module: Project created
```

### Log Actions for Audit

```python
# In service methods
self._log_action("create", "project", project.id, user_id)
# Logs: "[request_id] User 42: create project (ID: 1)"
```

## Repository Operations

### Available in BaseRepository

```python
# Create (with flush, no commit)
instance = await self.repos.model.create(name="foo", owner_id=1)

# Read
instance = await self.repos.model.get_by_id(1)

# Update (with flush, no commit)
await self.repos.model.update(1, name="bar", status="active")

# Delete (with flush, no commit)
await self.repos.model.delete(1)

# Find by filters
results = await self.repos.model.find_by(owner_id=1, status="active")

# Find first
instance = await self.repos.model.find_one(name="foo")

# List all with pagination
instances = await self.repos.model.list_all(skip=0, limit=100)
```

## Service Initialization

### With Request ID (for logging)

```python
# In route dependency
service = ProjectService(db, request_id="abc123")

# In tests (optional)
service = ProjectService(mock_db, request_id="test-123")
```

### Without Request ID (optional)

```python
# Request ID defaults to empty string
service = ProjectService(db)
```

## Testing

### Mock Repositories

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_service():
    # Create mock session
    mock_session = AsyncMock()
    
    # Instantiate service
    service = ProjectService(mock_session)
    
    # Mock repository methods
    service.repos.projects.find_by_name = AsyncMock(return_value=None)
    service.repos.projects.create = AsyncMock(return_value=MagicMock(id=1))
    service.commit = AsyncMock()
    
    # Call service
    result = await service.create(user_id=1, data=ProjectCreate(name="Test"))
    
    # Assert
    assert result.id == 1
    service.commit.assert_called_once()
```

## File Checklist

- [ ] `backend/app/repositories/base.py` - BaseRepository
- [ ] `backend/app/repositories/user_repository.py`
- [ ] `backend/app/repositories/project_repository.py`
- [ ] `backend/app/repositories/test_case_repository.py`
- [ ] `backend/app/repositories/execution_repository.py`
- [ ] `backend/app/repositories/execution_result_repository.py`
- [ ] `backend/app/repositories/report_repository.py`
- [ ] `backend/app/repositories/audit_log_repository.py`
- [ ] `backend/app/repositories/__init__.py` - RepositoryFactory
- [ ] `backend/app/services/base_service.py`
- [ ] `backend/app/services/auth_service.py`
- [ ] `backend/app/services/project_service.py`
- [ ] `backend/app/services/test_case_service.py`
- [ ] `backend/app/services/execution_service.py`
- [ ] `backend/app/services/__init__.py`
- [ ] `backend/app/routes/auth.py` - Split from main.py
- [ ] `backend/app/routes/projects.py` - Split from main.py
- [ ] `backend/app/routes/test_cases.py` - Split from main.py
- [ ] `backend/app/routes/executions.py` - Split from main.py
- [ ] `backend/app/routes/__init__.py`
- [ ] `backend/app/dependencies.py` - Updated with services
- [ ] `backend/app/exceptions.py` - Updated domain exceptions
- [ ] `backend/app/utils/logger.py` - Structured logging
- [ ] Update `backend/app/main.py` - Import routes, remove inlined handlers

## Environment & Config

Ensure your `backend/app/config.py` has:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "QA Automation"
    app_version: str = "1.0.0"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    cors_origins: list = ["*"]
    database_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Common Mistakes to Avoid

| Mistake | Problem | Fix |
|---------|---------|-----|
| Committing in repositories | Unclear transaction boundaries | Commit only in services |
| Querying in routes | Violates separation of concerns | Use services |
| HTTP exceptions in services | Tight coupling to FastAPI | Use domain exceptions |
| Mutating entities in-place | Hidden side effects | Use `update()` which returns new instance |
| No ownership checks | Security vulnerability | Check in service before returning |
| Implicit transactions | Data loss if route crashes | Explicit `await self.commit()` |
| Logging without context | Can't trace requests | Use `_log_action()` method |
| Giant services | Hard to test | Keep services focused on one domain |
| Mixing business logic in routes | Untestable | Move to services |
| No validation in services | Bad data in database | Validate in service before creating |
