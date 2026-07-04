"""FastAPI main application."""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import jwt

from app.config import settings
from app.database.session import SessionLocal
from app.database.models import User
from app.models.schemas import (
    UserRegister, UserLogin, TokenResponse, UserResponse,
    ProjectCreate, ProjectUpdate, ProjectResponse,
    TestCaseCreate, TestCaseUpdate, TestCaseResponse,
    ExecutionRequest, ExecutionResponse
)
from app.exceptions import AuthException, ValidationError
from app.dependencies import get_db, get_current_user
from app.services.project_service import ProjectService
from app.services.test_case_service import TestCaseService
from app.services.execution_service import ExecutionService
from app.repositories.project import ProjectRepository
from app.utils.logger import get_logger
from app.api import analytics, ai_agent, test_data, websocket, webhooks, health, test_generation, locator_healing, failure_analysis, impact_analysis, retry_management, test_review, parallel_execution, execution_stream, scheduling, test_data_lifecycle, analytics_dashboard, reporting, coverage, flakiness, rbac, sso, ml_recommendations, test_prioritization, notifications, enterprise, phase5, phase6, phase7

app = FastAPI(title=settings.app_name, version=settings.app_version)
logger = get_logger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(health.router)
app.include_router(analytics.router)
app.include_router(ai_agent.router)
app.include_router(test_generation.router)
app.include_router(locator_healing.router)
app.include_router(failure_analysis.router)
app.include_router(impact_analysis.router)
app.include_router(retry_management.router)
app.include_router(test_review.router)
app.include_router(parallel_execution.router)
app.include_router(execution_stream.router)
app.include_router(scheduling.router)
app.include_router(test_data_lifecycle.router)
app.include_router(analytics_dashboard.router)
app.include_router(reporting.router)
app.include_router(coverage.router)
app.include_router(flakiness.router)
app.include_router(rbac.router)
app.include_router(sso.router)
app.include_router(ml_recommendations.router)
app.include_router(test_prioritization.router)
app.include_router(notifications.router)
app.include_router(enterprise.router)
app.include_router(phase5.router)
app.include_router(phase6.router)
app.include_router(phase7.router)
app.include_router(test_data.router)
app.include_router(websocket.router)
app.include_router(webhooks.router)


# ───── Auth Routes ─────

@app.post("/api/auth/register", response_model=TokenResponse)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register new user."""
    try:
        from sqlalchemy import select
        # Check if email exists
        result = await db.execute(select(User).where(User.email == user.email))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        new_user = User(
            email=user.email,
            username=user.username,
            password_hash=user.password  # TODO: Hash password properly in production (use bcrypt)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        token = jwt.encode(
            {"sub": new_user.id, "email": new_user.email, "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)},
            settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        logger.info("User registered successfully", user_id=new_user.id, email=user.email)
        return {"access_token": token}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Registration error: {str(e)}", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(creds: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user."""
    try:
        from sqlalchemy import select
        logger.info("User login attempt", email=creds.email)

        # Find user by email
        result = await db.execute(select(User).where(User.email == creds.email))
        user = result.scalar_one_or_none()

        # Verify user exists and password matches (TODO: use bcrypt for hashing in production)
        if not user or user.password_hash != creds.password:
            logger.warning("Login failed", email=creds.email, reason="Invalid credentials")
            raise AuthException("Invalid credentials")

        # Generate JWT token
        token = jwt.encode(
            {"sub": user.id, "email": user.email, "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)},
            settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        logger.info("User logged in successfully", user_id=user.id, email=creds.email)
        return {"access_token": token}
    except AuthException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")


@app.post("/api/auth/refresh", response_model=TokenResponse)
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """Refresh JWT token."""
    try:
        token = jwt.encode(
            {"sub": current_user["id"], "email": current_user["email"], "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)},
            settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        logger.info("Token refreshed", user_id=current_user["id"])
        return {"access_token": token}
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}", error=str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token refresh failed")


# ───── Projects Routes ─────

@app.get("/api/projects", response_model=list[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all active projects owned by user."""
    try:
        service = ProjectService(db)
        projects = await service.list_user_projects(current_user["id"], skip=skip, limit=limit)
        return projects
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list projects")


@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new project."""
    try:
        service = ProjectService(db)
        created = await service.create_project(
            name=project.name,
            owner_id=current_user["id"],
            description=project.description,
            test_framework=project.test_framework
        )
        return created
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}", error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create project")


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get project by ID."""
    try:
        service = ProjectService(db)
        project = await service.get_project(project_id, user_id=current_user["id"])
        return project
    except Exception as e:
        logger.error(f"Error getting project: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update project."""
    try:
        service = ProjectService(db)
        project = await service.update_project(
            project_id=project_id,
            user_id=current_user["id"],
            name=project_data.name,
            description=project_data.description,
            test_framework=project_data.test_framework
        )
        return project
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update project")


@app.delete("/api/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete (deactivate) project."""
    try:
        service = ProjectService(db)
        await service.delete_project(project_id, user_id=current_user["id"])
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete project")


# ───── Test Cases Routes ─────

@app.get("/api/projects/{project_id}/test-cases", response_model=list[TestCaseResponse])
async def list_test_cases(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List test cases for project."""
    try:
        service = TestCaseService(db)
        test_cases = await service.list_test_cases(project_id, skip=skip, limit=limit)
        return test_cases
    except Exception as e:
        logger.error(f"Error listing test cases: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list test cases")


@app.post("/api/projects/{project_id}/test-cases", response_model=TestCaseResponse)
async def create_test_case(
    project_id: int,
    tc: TestCaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create test case."""
    try:
        service = TestCaseService(db)
        test_case = await service.create_test_case(
            project_id=project_id,
            user_id=current_user["id"],
            name=tc.name,
            description=tc.description,
            test_code=tc.test_code,
            test_type=tc.test_type,
            tags=tc.tags
        )
        return test_case
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating test case: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create test case")


@app.get("/api/projects/{project_id}/test-cases/{test_case_id}", response_model=TestCaseResponse)
async def get_test_case(
    project_id: int,
    test_case_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get test case by ID."""
    try:
        service = TestCaseService(db)
        test_case = await service.get_test_case(test_case_id, project_id=project_id)
        return test_case
    except Exception as e:
        logger.error(f"Error getting test case: {str(e)}", test_case_id=test_case_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")


@app.put("/api/projects/{project_id}/test-cases/{test_case_id}", response_model=TestCaseResponse)
async def update_test_case(
    project_id: int,
    test_case_id: int,
    tc: TestCaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update test case."""
    try:
        service = TestCaseService(db)
        test_case = await service.update_test_case(
            test_case_id=test_case_id,
            project_id=project_id,
            user_id=current_user["id"],
            name=tc.name,
            test_code=tc.test_code,
            tags=tc.tags
        )
        return test_case
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except Exception as e:
        logger.error(f"Error updating test case: {str(e)}", test_case_id=test_case_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update test case")


@app.delete("/api/projects/{project_id}/test-cases/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_case(
    project_id: int,
    test_case_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete test case."""
    try:
        service = TestCaseService(db)
        await service.delete_test_case(test_case_id, project_id=project_id, user_id=current_user["id"])
    except Exception as e:
        logger.error(f"Error deleting test case: {str(e)}", test_case_id=test_case_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete test case")


# ───── Execution Routes ─────

@app.post("/api/projects/{project_id}/execute", response_model=ExecutionResponse)
async def execute_tests(
    project_id: int,
    req: ExecutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Execute tests for project."""
    try:
        service = ExecutionService(db)
        execution = await service.create_execution(
            project_id=project_id,
            user_id=current_user["id"],
            test_case_ids=req.test_case_ids if req.test_case_ids else None
        )
        return execution
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except Exception as e:
        logger.error(f"Error executing tests: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to execute tests")


@app.get("/api/projects/{project_id}/executions", response_model=list[ExecutionResponse])
async def list_executions(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List executions for project."""
    try:
        service = ExecutionService(db)
        executions = await service.list_executions(project_id, skip=skip, limit=limit)
        return executions
    except Exception as e:
        logger.error(f"Error listing executions: {str(e)}", project_id=project_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list executions")


@app.get("/api/projects/{project_id}/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    project_id: int,
    execution_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get execution by ID."""
    try:
        service = ExecutionService(db)
        execution = await service.get_execution(execution_id, project_id=project_id)
        return execution
    except Exception as e:
        logger.error(f"Error getting execution: {str(e)}", execution_id=execution_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
