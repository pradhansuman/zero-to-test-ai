"""Unit tests for services."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.models.project import Project
from app.database.models.test_case import TestCase
from app.services.project_service import ProjectService
from app.services.test_case_service import TestCaseService
from app.exceptions import ValidationError


@pytest.mark.asyncio
async def test_project_service_create(test_db: AsyncSession):
    """Test creating a new project."""
    service = ProjectService(test_db)

    # Create user first
    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    # Create project
    project = await service.create_project(
        name="Test Project",
        owner_id=user.id,
        description="A test project",
        test_framework="pytest"
    )

    assert project.name == "Test Project"
    assert project.owner_id == user.id
    assert project.is_active is True


@pytest.mark.asyncio
async def test_project_service_validation_empty_name(test_db: AsyncSession):
    """Test project creation validation - empty name."""
    service = ProjectService(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    with pytest.raises(ValidationError):
        await service.create_project(
            name="",
            owner_id=user.id,
            description="A test project"
        )


@pytest.mark.asyncio
async def test_project_service_get_user_projects(test_db: AsyncSession):
    """Test getting user projects."""
    service = ProjectService(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    p1 = Project(name="Project 1", owner_id=user.id, is_active=True)
    p2 = Project(name="Project 2", owner_id=user.id, is_active=True)
    test_db.add_all([p1, p2])
    await test_db.flush()

    projects = await service.list_user_projects(user.id)
    assert len(projects) == 2


@pytest.mark.asyncio
async def test_project_service_delete_soft(test_db: AsyncSession):
    """Test soft delete of project."""
    service = ProjectService(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Test Project", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    await service.delete_project(project.id, user_id=user.id)

    deleted_project = await service.get_project(project.id, user_id=user.id)
    assert deleted_project.is_active is False


@pytest.mark.asyncio
async def test_test_case_service_create(test_db: AsyncSession):
    """Test creating test case."""
    service = TestCaseService(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Test Project", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    test_case = await service.create_test_case(
        project_id=project.id,
        user_id=user.id,
        name="Login Test",
        description="Test user login",
        test_type="functional",
        tags=["auth"]
    )

    assert test_case.name == "Login Test"
    assert test_case.project_id == project.id
    assert test_case.test_type == "functional"


@pytest.mark.asyncio
async def test_test_case_service_invalid_type(test_db: AsyncSession):
    """Test test case validation - invalid type."""
    service = TestCaseService(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Test Project", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    with pytest.raises(ValidationError):
        await service.create_test_case(
            project_id=project.id,
            user_id=user.id,
            name="Test",
            description="Test",
            test_type="invalid_type"
        )


@pytest.mark.asyncio
async def test_test_case_service_list_by_type(test_db: AsyncSession):
    """Test filtering test cases by type."""
    service = TestCaseService(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Test Project", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    tc1 = TestCase(
        project_id=project.id,
        name="Functional Test",
        test_type="functional",
        is_active=True
    )
    tc2 = TestCase(
        project_id=project.id,
        name="API Test",
        test_type="api",
        is_active=True
    )
    test_db.add_all([tc1, tc2])
    await test_db.flush()

    functional_cases = await service.list_test_cases_by_type(project.id, "functional")
    assert len(functional_cases) == 1
    assert functional_cases[0].test_type == "functional"
