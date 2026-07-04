# Services Layer & Business Logic (Phase 2 Task 4)

**Status:** ✅ Complete  
**Date:** 2026-07-03  
**Components:** Repository Pattern + 3 Services + Structured Logging

---

## Overview

This document describes Phase 2 Task 4: the services layer implementation for the QA automation backend. The services layer sits between API routes and the database, encapsulating business logic, validation, and transaction management.

## Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Routes (main.py)        │
│  ├─ POST   /api/projects                │
│  ├─ GET    /api/projects/{id}           │
│  ├─ PUT    /api/projects/{id}           │
│  ├─ DELETE /api/projects/{id}           │
│  ├─ POST   /api/projects/{id}/test-cases│
│  ├─ GET    /api/projects/{id}/execute   │
│  └─ ...                                 │
└──────────────────────────┬──────────────┘
                           │
┌──────────────────────────▼──────────────┐
│      Services Layer (Business Logic)    │
│  ├─ ProjectService                      │
│  ├─ TestCaseService                     │
│  └─ ExecutionService                    │
└──────────────────────────┬──────────────┘
                           │
┌──────────────────────────▼──────────────┐
│  Repository Pattern (Data Access)       │
│  ├─ BaseRepository<T>                   │
│  ├─ ProjectRepository                   │
│  ├─ TestCaseRepository                  │
│  └─ ExecutionRepository                 │
└──────────────────────────┬──────────────┘
                           │
┌──────────────────────────▼──────────────┐
│    SQLAlchemy ORM (Database)            │
│    PostgreSQL                           │
└─────────────────────────────────────────┘
```

## Components

### 1. Utilities Layer

#### `app/utils/logger.py`
Structured logging with context support:
- `StructuredLogger` class for consistent log formatting
- Logs as JSON with metadata (timestamp, context, message)
- Methods: `info()`, `warning()`, `error()`, `debug()`
- Example: `logger.info("Project created", project_id=123, owner_id=456)`

### 2. Repository Pattern

Encapsulates data access behind a consistent interface.

#### `app/repositories/base.py`
Generic CRUD operations for any model:
- `create(obj_in)` - Create new record
- `get(id)` - Get record by ID
- `get_all(skip, limit)` - List records with pagination
- `update(id, obj_in)` - Update record
- `delete(id)` - Delete record
- `find_by(**filters)` - Find records by filters
- `find_one_by(**filters)` - Find single record by filters
- `count()` - Count total records

#### `app/repositories/project.py`
Project-specific queries:
- `get_by_owner(owner_id, skip, limit)` - Get projects owned by user
- `get_active_projects(skip, limit)` - Get all active projects
- `search_by_name(name)` - Search projects by name

#### `app/repositories/test_case.py`
Test case-specific queries:
- `get_by_project(project_id, skip, limit)` - Get test cases for project
- `get_by_type(project_id, test_type)` - Filter by test type
- `get_by_tags(project_id, tags)` - Filter by tags
- `search_by_name(project_id, name)` - Search by name
- `get_bulk(test_case_ids)` - Get multiple test cases by IDs

#### `app/repositories/execution.py`
Execution-specific queries:
- `get_by_project(project_id, skip, limit)` - Get executions for project
- `get_by_status(project_id, status)` - Filter by status
- `get_recent(project_id, limit)` - Get recent executions
- `update_status(execution_id, status)` - Update execution status
- `update_results(execution_id, passed, failed, skipped, duration)` - Update results
- `count_by_status(project_id, status)` - Count by status

### 3. Services Layer

Business logic layer with validation, transaction management, and error handling.

#### `app/services/project_service.py`
Project management with CRUD operations:
- `create_project(name, owner_id, description, test_framework)` - Create with validation
- `get_project(project_id, user_id)` - Get with ownership check
- `list_projects(skip, limit)` - List all active projects
- `list_user_projects(user_id, skip, limit)` - Get user's projects
- `update_project(project_id, user_id, ...)` - Update with validation
- `delete_project(project_id, user_id)` - Soft delete (deactivate)
- `search_projects(name)` - Search by name

**Validation:**
- Project name required and < 255 chars
- Test framework must be valid (playwright, pytest, selenium, cypress, custom)
- Ownership verification for updates/deletes
- Transaction management with commit/rollback

#### `app/services/test_case_service.py`
Test case management with filtering:
- `create_test_case(project_id, user_id, name, test_code, ...)` - Create with validation
- `get_test_case(test_case_id, project_id)` - Get test case
- `list_test_cases(project_id, skip, limit)` - List test cases
- `list_by_type(project_id, test_type)` - Filter by type (e2e, unit, integration, performance)
- `list_by_tags(project_id, tags)` - Filter by tags
- `search_test_cases(project_id, name)` - Search by name
- `update_test_case(test_case_id, project_id, user_id, ...)` - Update with validation
- `delete_test_case(test_case_id, project_id, user_id)` - Soft delete
- `get_bulk(test_case_ids, project_id)` - Get multiple test cases

**Validation:**
- Test case name required and < 255 chars
- Test code required and non-empty
- Valid test types: e2e, unit, integration, performance
- Ownership verification via project
- Bulk operation validation

#### `app/services/execution_service.py`
Test orchestration and execution tracking:
- `create_execution(project_id, user_id, test_case_ids)` - Create execution
- `get_execution(execution_id, project_id)` - Get execution
- `list_executions(project_id, skip, limit)` - List executions
- `list_by_status(project_id, status)` - Filter by status
- `get_recent_executions(project_id, limit)` - Get recent executions
- `start_execution(execution_id, project_id)` - Mark as running
- `complete_execution(execution_id, project_id, passed, failed, skipped, duration)` - Complete with results
- `fail_execution(execution_id, project_id, error_message)` - Mark as failed
- `get_execution_summary(execution_id)` - Get summary with stats
- `get_project_statistics(project_id)` - Get project execution statistics

**Validation:**
- Valid status transitions (PENDING → RUNNING → PASSED/FAILED)
- Test count validation (non-negative, within total)
- Duration validation (non-negative)
- Result aggregation and pass rate calculation

### 4. Updated Routes (main.py)

All routes now use the services layer:

**Projects:**
- `GET /api/projects` - List active projects
- `POST /api/projects` - Create project (requires auth)
- `GET /api/projects/{project_id}` - Get project (ownership check)
- `PUT /api/projects/{project_id}` - Update project (ownership check)
- `DELETE /api/projects/{project_id}` - Delete project (ownership check)

**Test Cases:**
- `GET /api/projects/{project_id}/test-cases` - List test cases
- `POST /api/projects/{project_id}/test-cases` - Create test case
- `GET /api/projects/{project_id}/test-cases/{test_case_id}` - Get test case
- `PUT /api/projects/{project_id}/test-cases/{test_case_id}` - Update test case
- `DELETE /api/projects/{project_id}/test-cases/{test_case_id}` - Delete test case

**Executions:**
- `POST /api/projects/{project_id}/execute` - Create execution
- `GET /api/projects/{project_id}/executions` - List executions
- `GET /api/projects/{project_id}/executions/{execution_id}` - Get execution

## Error Handling Strategy

### Exception Hierarchy
```
HTTPException (from FastAPI)
├─ ValidationError (422) - Input validation failed
├─ AuthException (401) - Authentication failed
├─ Unauthorized (403) - User lacks permission
├─ ProjectNotFound (404) - Project not found
├─ TestCaseNotFound (404) - Test case not found
└─ ExecutionNotFound (404) - Execution not found
```

### Error Flow
1. **Route handler** catches exceptions from service
2. **Service** raises domain-specific exceptions
3. **Route** converts to HTTP response with appropriate status code
4. **Logger** records error with context

Example:
```python
try:
    service = ProjectService(db)
    project = await service.get_project(project_id, user_id)
except ValidationError as e:
    raise HTTPException(status_code=422, detail=e.detail)
except Unauthorized:
    raise HTTPException(status_code=403, detail="You do not own this project")
except Exception as e:
    logger.error("Error getting project", project_id=project_id, error=str(e))
    raise HTTPException(status_code=500, detail="Failed to get project")
```

## Transaction Management

Services handle transactions:
- **Create/Update/Delete** - Explicit `await db.commit()`
- **Rollback** - Called on error in try-except
- **Isolation** - AsyncSession manages connection pooling

Example:
```python
async def update_project(self, project_id: int, ...):
    try:
        project = await self.repo.update(project_id, update_data)
        await self.session.commit()  # Explicit commit
        return project
    except Exception as e:
        await self.session.rollback()  # Explicit rollback
        raise
```

## Input Validation

Validation happens at multiple layers:

### 1. Pydantic Schema Level
```python
class ProjectCreate(BaseModel):
    name: str  # Required
    description: Optional[str] = None
    test_framework: str = "playwright"
```

### 2. Service Level
```python
if not name or not name.strip():
    raise ValidationError("Project name is required")
if len(name) > 255:
    raise ValidationError("Project name must be less than 255 characters")
```

### 3. Authorization Level
```python
if project.owner_id != user_id:
    raise Unauthorized("You do not own this project")
```

## Testing Considerations

### Unit Testing
Test individual service methods with mocked repositories:
```python
async def test_create_project_validation():
    mock_repo = Mock()
    service = ProjectService(mock_repo)
    with pytest.raises(ValidationError):
        await service.create_project("", owner_id=1)
```

### Integration Testing
Test services with real database:
```python
async def test_create_project_flow(db: AsyncSession):
    service = ProjectService(db)
    project = await service.create_project("Test", owner_id=1)
    assert project.id is not None
    assert project.is_active is True
```

### E2E Testing
Test complete request-response flow:
```python
async def test_create_project_endpoint(client):
    response = await client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "..."},
        headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"
```

## Key Design Decisions

1. **Soft Deletes** - Projects and test cases are deactivated, not hard deleted
2. **Ownership Checks** - Services verify user owns resources before modification
3. **Transaction Boundaries** - Each service method handles its own transaction
4. **Structured Logging** - All operations logged with contextual metadata
5. **Generic Repository Base** - Reduces code duplication for CRUD operations
6. **Status Transitions** - ExecutionService validates valid status changes
7. **Result Aggregation** - Services calculate statistics (pass rate, duration)

## Next Steps

Phase 2 Task 5: API Routes Continued
- Implement additional endpoints (AI generation, analytics, webhooks)
- Add WebSocket support for live execution updates
- Integrate with Phase 1 test engines

---

## Files Created

```
backend/app/
├── utils/
│   ├── __init__.py
│   └── logger.py                    (structured logging)
├── repositories/
│   ├── __init__.py
│   ├── base.py                      (generic CRUD)
│   ├── project.py                   (project queries)
│   ├── test_case.py                 (test case queries)
│   └── execution.py                 (execution queries)
├── services/
│   ├── __init__.py
│   ├── project_service.py           (project business logic)
│   ├── test_case_service.py         (test case business logic)
│   └── execution_service.py         (execution orchestration)
└── main.py                          (updated routes to use services)
```

## Implementation Summary

✅ **Repository Pattern** - Base class + 3 concrete repositories  
✅ **ProjectService** - CRUD with validation, ownership checks, transaction management  
✅ **TestCaseService** - Filtering by type/tags, bulk operations, search  
✅ **ExecutionService** - Status tracking, result aggregation, statistics  
✅ **Structured Logging** - Context-aware logging on all operations  
✅ **Error Handling** - Domain-specific exceptions, proper HTTP status codes  
✅ **Input Validation** - Schema + service-level validation  
✅ **Routes Integration** - All routes refactored to use services  

---

**Created by:** Claude Code  
**Phase:** 2 Task 4  
**Timeline:** Ready for Phase 2 Task 5
