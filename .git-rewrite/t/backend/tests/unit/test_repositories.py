"""Unit tests for repositories."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.models.project import Project
from app.repositories.project import ProjectRepository


@pytest.mark.asyncio
async def test_project_repository_create(test_db: AsyncSession):
    """Test creating project via repository."""
    repo = ProjectRepository(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = await repo.create(
        Project(
            name="Test Project",
            owner_id=user.id,
            description="A test project",
            is_active=True
        )
    )

    assert project.name == "Test Project"
    assert project.owner_id == user.id


@pytest.mark.asyncio
async def test_project_repository_get_by_id(test_db: AsyncSession):
    """Test retrieving project by ID."""
    repo = ProjectRepository(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Test Project", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    fetched = await repo.get_by_id(project.id)
    assert fetched is not None
    assert fetched.name == "Test Project"


@pytest.mark.asyncio
async def test_project_repository_get_by_owner(test_db: AsyncSession):
    """Test retrieving projects by owner."""
    repo = ProjectRepository(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    p1 = Project(name="Project 1", owner_id=user.id, is_active=True)
    p2 = Project(name="Project 2", owner_id=user.id, is_active=True)
    test_db.add_all([p1, p2])
    await test_db.flush()

    projects = await repo.get_by_owner(user.id)
    assert len(projects) == 2


@pytest.mark.asyncio
async def test_project_repository_update(test_db: AsyncSession):
    """Test updating project."""
    repo = ProjectRepository(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Old Name", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    project.name = "New Name"
    updated = await repo.update(project)

    assert updated.name == "New Name"


@pytest.mark.asyncio
async def test_project_repository_soft_delete(test_db: AsyncSession):
    """Test soft delete of project."""
    repo = ProjectRepository(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    project = Project(name="Test Project", owner_id=user.id, is_active=True)
    test_db.add(project)
    await test_db.flush()

    await repo.delete(project.id)

    deleted_project = await repo.get_by_id(project.id)
    assert deleted_project.is_active is False


@pytest.mark.asyncio
async def test_project_repository_list_active(test_db: AsyncSession):
    """Test listing only active projects."""
    repo = ProjectRepository(test_db)

    user = User(email="owner@example.com", username="owner", password_hash="hash")
    test_db.add(user)
    await test_db.flush()

    active = Project(name="Active", owner_id=user.id, is_active=True)
    inactive = Project(name="Inactive", owner_id=user.id, is_active=False)
    test_db.add_all([active, inactive])
    await test_db.flush()

    projects = await repo.get_active_projects()
    assert len(projects) == 1
    assert projects[0].name == "Active"
