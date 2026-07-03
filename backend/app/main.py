"""FastAPI main application."""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import jwt

from app.config import settings
from app.database.session import SessionLocal
from app.database.models import User, Project, TestCase, Execution
from app.models.schemas import (
    UserRegister, UserLogin, TokenResponse, UserResponse,
    ProjectCreate, ProjectUpdate, ProjectResponse,
    TestCaseCreate, TestCaseResponse,
    ExecutionRequest, ExecutionResponse
)
from app.exceptions import AuthException, ProjectNotFound, TestCaseNotFound
from app.dependencies import get_db

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ───── Auth Routes ─────

@app.post("/api/auth/register", response_model=TokenResponse)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register new user."""
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(email=user.email, username=user.username, password_hash=user.password)
    db.add(new_user)
    await db.commit()

    token = jwt.encode(
        {"sub": new_user.id, "email": new_user.email, "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)},
        settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return {"access_token": token}


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(creds: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user."""
    result = await db.execute(select(User).where(User.email == creds.email))
    user = result.scalar_one_or_none()
    if not user or user.password_hash != creds.password:
        raise AuthException("Invalid credentials")

    token = jwt.encode(
        {"sub": user.id, "email": user.email, "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)},
        settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return {"access_token": token}


@app.post("/api/auth/refresh", response_model=TokenResponse)
async def refresh_token():
    """Refresh JWT token."""
    token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)},
        settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return {"access_token": token}


# ───── Projects Routes ─────

@app.get("/api/projects", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    """List all projects."""
    result = await db.execute(select(Project))
    return result.scalars().all()


@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    """Create new project."""
    new_project = Project(name=project.name, description=project.description, owner_id=1, test_framework=project.test_framework)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Get project by ID."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise ProjectNotFound()
    return project


@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    """Update project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise ProjectNotFound()

    if project_data.name:
        project.name = project_data.name
    if project_data.description:
        project.description = project_data.description

    await db.commit()
    return project


@app.delete("/api/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Delete project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise ProjectNotFound()

    await db.delete(project)
    await db.commit()


# ───── Test Cases Routes ─────

@app.get("/api/projects/{project_id}/test-cases", response_model=list[TestCaseResponse])
async def list_test_cases(project_id: int, db: AsyncSession = Depends(get_db)):
    """List test cases for project."""
    result = await db.execute(select(TestCase).where(TestCase.project_id == project_id))
    return result.scalars().all()


@app.post("/api/projects/{project_id}/test-cases", response_model=TestCaseResponse)
async def create_test_case(project_id: int, tc: TestCaseCreate, db: AsyncSession = Depends(get_db)):
    """Create test case."""
    new_tc = TestCase(project_id=project_id, name=tc.name, description=tc.description, test_code=tc.test_code, test_type=tc.test_type, tags=tc.tags)
    db.add(new_tc)
    await db.commit()
    await db.refresh(new_tc)
    return new_tc


# ───── Execution Routes ─────

@app.post("/api/projects/{project_id}/execute", response_model=ExecutionResponse)
async def execute_tests(project_id: int, req: ExecutionRequest, db: AsyncSession = Depends(get_db)):
    """Execute tests for project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise ProjectNotFound()

    execution = Execution(project_id=project_id, status="running", started_at=datetime.utcnow(), total_tests=len(req.test_case_ids))
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    return execution


@app.get("/api/projects/{project_id}/executions", response_model=list[ExecutionResponse])
async def list_executions(project_id: int, db: AsyncSession = Depends(get_db)):
    """List executions for project."""
    result = await db.execute(select(Execution).where(Execution.project_id == project_id))
    return result.scalars().all()


# ───── Health Check ─────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
