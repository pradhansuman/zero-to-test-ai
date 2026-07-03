# Phase 2: Backend + DevOps Blueprint

**Status:** Ready for Implementation  
**Date:** 2026-07-03  
**Phases:** 4 weeks (Weeks 3-4 of 8-week sprint)  
**Foundation:** Phase 1 (complete, all green)

---

## Overview

Phase 2 wraps Phase 1 testing engines in a **production-ready FastAPI backend**, adds persistent storage (PostgreSQL), caching (Redis), async jobs (Celery), and deploys to Kubernetes.

**Deliverables:**
- ✅ FastAPI server (9 API routes)
- ✅ PostgreSQL schema + Alembic migrations
- ✅ Redis caching layer
- ✅ Celery background jobs
- ✅ Docker Compose (local dev)
- ✅ Kubernetes manifests (production)
- ✅ GitHub Actions CI/CD (Phase 2 tests)

---

## Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Backend (Python)        │
│  ┌──────────────────────────────────┐  │
│  │  9 API Routes (CRUD + Execution) │  │
│  ├──────────────────────────────────┤  │
│  │  Services Layer (Business Logic) │  │
│  ├──────────────────────────────────┤  │
│  │  Database ORM (SQLAlchemy)       │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
         ↓           ↓           ↓
   PostgreSQL    Redis        Celery
   (Persistent) (Cache)    (Async Jobs)
         ↑                       ↑
    Phase 1 Engines ←────────────┘
  (API + Database)
```

---

## Folder Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry
│   ├── config.py                  # Config, env vars
│   ├── dependencies.py            # Dependency injection
│   ├── exceptions.py              # Custom exceptions
│   ├── middleware.py              # Auth, CORS, logging
│   │
│   ├── api/                       # 9 API route modules
│   │   ├── auth.py                # JWT, OAuth2 (routes)
│   │   ├── projects.py            # Project CRUD (routes)
│   │   ├── test_cases.py          # Test case CRUD (routes)
│   │   ├── test_data.py           # Test data mgmt (routes)
│   │   ├── execution.py           # Run tests, scheduler (routes)
│   │   ├── ai_agent.py            # AI test generation (routes)
│   │   ├── analytics.py           # Reports, dashboards (routes)
│   │   ├── webhooks.py            # GitHub, Jira, Slack (routes)
│   │   └── health.py              # Health checks (routes)
│   │
│   ├── models/                    # Pydantic request/response
│   │   ├── project.py
│   │   ├── test_case.py
│   │   ├── execution.py
│   │   ├── report.py
│   │   ├── user.py
│   │   └── ai_schema.py
│   │
│   ├── database/                  # Database layer
│   │   ├── base.py                # SQLAlchemy base
│   │   ├── session.py             # DB session mgmt
│   │   ├── migrations/            # Alembic migrations
│   │   └── models/                # SQLAlchemy ORM
│   │       ├── project.py
│   │       ├── test_case.py
│   │       ├── execution.py
│   │       ├── report.py
│   │       ├── user.py
│   │       └── audit_log.py
│   │
│   ├── services/                  # Business logic
│   │   ├── project_service.py
│   │   ├── test_generation.py
│   │   ├── execution_service.py
│   │   ├── failure_analysis.py
│   │   ├── healing_service.py
│   │   ├── report_service.py
│   │   ├── analytics_service.py
│   │   ├── auth_service.py
│   │   ├── ai_service.py
│   │   └── notification_service.py
│   │
│   ├── workers/                   # Celery background jobs
│   │   ├── celery_app.py
│   │   ├── test_execution.py
│   │   ├── report_generation.py
│   │   ├── ai_analysis.py
│   │   └── scheduler.py
│   │
│   └── utils/
│       ├── logger.py
│       ├── decorators.py
│       ├── validators.py
│       └── helpers.py
│
├── tests/                         # Backend tests (80% coverage)
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── requirements.txt               # Python dependencies
├── alembic.ini                    # Alembic configuration
├── Dockerfile                     # Backend container
├── docker-compose.yml             # Local dev stack
└── .env.example                   # Environment template

infrastructure/
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.celery
│   └── docker-compose.prod.yml
│
├── kubernetes/
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── postgres/
│   │   ├── statefulset.yaml
│   │   ├── pvc.yaml
│   │   └── service.yaml
│   ├── redis/
│   │   ├── statefulset.yaml
│   │   └── service.yaml
│   ├── celery/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── ingress.yaml
│
├── ci-cd/
│   └── .github/workflows/
│       ├── backend-test.yml
│       ├── backend-build.yml
│       ├── backend-deploy.yml
│       └── db-migrate.yml
│
└── monitoring/
    ├── prometheus.yml
    ├── grafana-dashboards.yaml
    └── alerting-rules.yaml
```

---

## 12 Implementation Tasks

### Task 1: Database Schema & Migrations
- Create SQLAlchemy ORM models (Project, TestCase, Execution, Report, User, AuditLog)
- Initialize Alembic
- Generate initial migration
- Create seed data script

### Task 2: Pydantic Request/Response Models
- Request/response DTOs for all 9 routes
- Validator decorators for inputs
- Error response envelope

### Task 3: FastAPI Server Scaffold
- Main FastAPI app initialization
- Configuration management (env vars, secrets)
- Middleware (CORS, logging, exception handling)
- Dependency injection setup

### Task 4: Authentication (JWT + OAuth2)
- JWT token generation/validation
- OAuth2 with GitHub integration
- User registration + login endpoints
- Refresh token mechanism

### Task 5-13: 9 API Routes (1 task each)
- **Task 5:** Projects API (GET, POST, PUT, DELETE)
- **Task 6:** Test Cases API (CRUD + bulk operations)
- **Task 7:** Test Data Management API
- **Task 8:** Execution API (run, history, streaming)
- **Task 9:** AI Agent API (test generation, healing)
- **Task 10:** Analytics API (trends, coverage, flaky tests)
- **Task 11:** Webhooks API (GitHub, Jira, Slack integrations)
- **Task 12:** Health Checks + Metrics
- **Task 13:** Rate limiting + quota management

### Task 14: Services Layer
- Implement 9 service classes (business logic)
- Repository pattern for data access
- Transaction management
- Error handling + retries

### Task 15: Celery + Redis Integration
- Celery app initialization
- Task definitions (test execution, reports, AI analysis)
- Periodic tasks (scheduler)
- Result backend (Redis)

### Task 16: PostgreSQL + Alembic
- Database initialization script
- Migration versioning
- Rollback testing
- Seed data population

### Task 17: Docker & Compose
- Backend Dockerfile
- Celery worker Dockerfile
- docker-compose.yml (all services)
- Database initialization script

### Task 18: Kubernetes Manifests
- Deployments (backend, celery, postgres, redis)
- Services (internal + ingress)
- ConfigMaps + Secrets
- StatefulSets for stateful services
- HPA (auto-scaling)

### Task 19: GitHub Actions CI/CD
- Backend unit tests (80%+ coverage)
- Integration tests
- Type checking (mypy)
- Docker build validation
- Deployment workflows

### Task 20: Backend Tests (80% Coverage)
- Unit tests (services, utilities, validators)
- Integration tests (API endpoints + DB)
- E2E tests (full workflows)
- Fixtures + factories

### Task 21: Documentation & Integration
- API documentation (OpenAPI/Swagger)
- Architecture decision records (ADRs)
- Deployment guide
- Troubleshooting guide

---

## Data Models (SQLAlchemy)

```python
# Core entities
User(id, email, password_hash, role, created_at)
Project(id, name, owner_id, test_framework, created_at)
TestCase(id, project_id, name, type, test_code, created_at)
TestData(id, project_id, name, data, created_at)
Execution(id, project_id, started_at, status, passed, failed, skipped)
ExecutionResult(id, execution_id, test_id, status, error, created_at)
Report(id, execution_id, format, content, created_at)
AuditLog(id, user_id, action, resource, timestamp)

# Relationships
User.projects (1:N)
Project.test_cases (1:N)
Project.executions (1:N)
Execution.results (1:N)
```

---

## API Routes (9 total)

```
POST   /api/auth/register              # User registration
POST   /api/auth/login                 # JWT login
POST   /api/auth/refresh               # Refresh token

GET    /api/projects                   # List projects
POST   /api/projects                   # Create project
GET    /api/projects/{id}              # Get project
PUT    /api/projects/{id}              # Update project
DELETE /api/projects/{id}              # Delete project

GET    /api/projects/{id}/test-cases   # List test cases
POST   /api/projects/{id}/test-cases   # Create test case
GET    /api/projects/{id}/test-cases/{tcid}
PUT    /api/projects/{id}/test-cases/{tcid}
DELETE /api/projects/{id}/test-cases/{tcid}

POST   /api/projects/{id}/execute      # Run tests
GET    /api/projects/{id}/executions   # Execution history
GET    /api/projects/{id}/executions/{eid}
WebSocket /ws/execution/{eid}          # Live updates

POST   /api/projects/{id}/ai/generate-tests
POST   /api/projects/{id}/ai/heal-locators
POST   /api/projects/{id}/ai/analyze-failure

GET    /api/analytics/dashboard
GET    /api/analytics/trends
GET    /api/analytics/coverage
GET    /api/analytics/flaky-tests

POST   /api/webhooks/github
POST   /api/webhooks/jira
POST   /api/webhooks/slack

GET    /health                         # Health check
GET    /metrics                        # Prometheus metrics
```

---

## Dependencies (requirements.txt)

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.13.1
asyncpg==0.29.0
redis==5.0.1
celery==5.3.4
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
aiohttp==3.9.1
prometheus-client==0.19.0
```

---

## Docker Compose (Local Dev)

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:pass@postgres/db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A app.workers.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://user:pass@postgres/db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

---

## Success Criteria

✅ All 12 tasks complete  
✅ 80%+ test coverage (backend + integration)  
✅ All API routes functional  
✅ Docker/Compose working  
✅ Kubernetes manifests valid  
✅ CI/CD pipelines green  
✅ Documentation complete  

---

## Timeline

**Week 3:**
- Tasks 1-10 (Schema, models, routes)
- Docker setup

**Week 4:**
- Tasks 11-21 (Services, K8s, CI/CD, tests, docs)
- Final validation + merge

---

## Next Session

Start with Task 1: Database Schema & Migrations
- Create SQLAlchemy models
- Initialize Alembic
- Generate initial migration
- Create seed data

Ready to build! 🚀
