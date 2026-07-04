# QA Automation Backend API Documentation

## Overview

The QA Automation Backend API provides RESTful endpoints for managing test automation projects, test cases, executions, and analytics.

**Base URL:** `https://qa-api.example.com/api`

**Version:** 1.0.0

---

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require JWT bearer token authentication.

### Authorization Header

```
Authorization: Bearer <access_token>
```

### Token Claims

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890
}
```

---

## API Endpoints

### Authentication

#### Register User
- **POST** `/auth/register`
- **Request:**
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "SecurePass123!"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
  }
  ```

#### Login
- **POST** `/auth/login`
- **Request:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123!"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
  }
  ```

#### Refresh Token
- **POST** `/auth/refresh`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
  }
  ```

---

### Projects

#### List Projects
- **GET** `/projects`
- **Query Parameters:**
  - `skip`: int (default: 0)
  - `limit`: int (default: 100)
- **Response:** `200 OK`
  ```json
  [
    {
      "id": 1,
      "name": "Project Name",
      "description": "Project description",
      "owner_id": 1,
      "test_framework": "pytest",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
  ```

#### Create Project
- **POST** `/projects`
- **Request:**
  ```json
  {
    "name": "My Project",
    "description": "Project description",
    "test_framework": "pytest"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "id": 1,
    "name": "My Project",
    "description": "Project description",
    "owner_id": 1,
    "test_framework": "pytest",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
  ```

#### Get Project
- **GET** `/projects/{project_id}`
- **Response:** `200 OK` (same as create)
- **Error:** `404 Not Found`

#### Update Project
- **PUT** `/projects/{project_id}`
- **Request:** (same fields as create)
- **Response:** `200 OK`

#### Delete Project
- **DELETE** `/projects/{project_id}`
- **Response:** `204 No Content`

---

### Test Cases

#### List Test Cases
- **GET** `/projects/{project_id}/test-cases`
- **Query Parameters:**
  - `skip`: int (default: 0)
  - `limit`: int (default: 100)
- **Response:** `200 OK` (array of test cases)

#### Create Test Case
- **POST** `/projects/{project_id}/test-cases`
- **Request:**
  ```json
  {
    "name": "Login Test",
    "description": "Test user login",
    "test_type": "functional",
    "tags": ["auth", "critical"]
  }
  ```
- **Response:** `200 OK`

#### Get Test Case
- **GET** `/projects/{project_id}/test-cases/{test_case_id}`
- **Response:** `200 OK`

#### Update Test Case
- **PUT** `/projects/{project_id}/test-cases/{test_case_id}`
- **Response:** `200 OK`

#### Delete Test Case
- **DELETE** `/projects/{project_id}/test-cases/{test_case_id}`
- **Response:** `204 No Content`

---

### Executions

#### Execute Tests
- **POST** `/projects/{project_id}/execute`
- **Request:**
  ```json
  {
    "test_case_ids": [1, 2, 3]
  }
  ```
- **Response:** `200 OK`

#### List Executions
- **GET** `/projects/{project_id}/executions`
- **Response:** `200 OK` (array of executions)

#### Get Execution
- **GET** `/projects/{project_id}/executions/{execution_id}`
- **Response:** `200 OK`

---

### Health Checks

#### Basic Health
- **GET** `/health`
- **Response:** `200 OK`
  ```json
  {
    "status": "healthy",
    "service": "qa-automation-backend",
    "version": "1.0.0"
  }
  ```

#### Readiness
- **GET** `/health/ready`
- **Response:** `200 OK` or `503 Service Unavailable`

#### Liveness
- **GET** `/health/live`
- **Response:** `200 OK` or `503 Service Unavailable`

#### Database Health
- **GET** `/health/db`
- **Response:** `200 OK` with database details

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Rate Limiting

Rate limits are applied per user:

- **Default:** 1000 requests per hour
- **Burst:** 10 requests per second

Headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

---

## Pagination

List endpoints support pagination with:

- `skip`: Number of items to skip
- `limit`: Max items to return (max 100)

---

## Interactive Documentation

Swagger UI: `GET /docs`
ReDoc: `GET /redoc`
OpenAPI Schema: `GET /openapi.json`

---

## SDK Usage

### Python

```python
import httpx

async with httpx.AsyncClient(base_url="https://qa-api.example.com/api") as client:
    # Register
    response = await client.post("/auth/register", json={
        "email": "user@example.com",
        "username": "user",
        "password": "Pass123!"
    })
    token = response.json()["access_token"]

    # Create project
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/projects", json={
        "name": "My Project"
    }, headers=headers)
```

---

## Support

For issues, feature requests, or documentation improvements, please submit an issue to the project repository.
