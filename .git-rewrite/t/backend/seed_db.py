"""Seed database with test data for development and testing."""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database.models.user import User
from app.database.models.project import Project
from app.database.models.test_case import TestCase
from app.database.models.execution import Execution
from app.database.models.test_data import TestData


async_engine = create_async_engine(settings.database_url, echo=False)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def seed_users(session: AsyncSession) -> User:
    """Create test users."""
    user = User(
        email="testuser@example.com",
        username="testuser",
        password_hash="$2b$12$fake_hash_12345678901234567890",  # Placeholder
        is_active=True,
    )
    session.add(user)
    await session.flush()
    return user


async def seed_projects(session: AsyncSession, user: User) -> Project:
    """Create test projects."""
    project = Project(
        name="QA Automation Suite",
        description="Main QA automation project for testing",
        owner_id=user.id,
        is_active=True,
    )
    session.add(project)
    await session.flush()
    return project


async def seed_test_cases(session: AsyncSession, project: Project) -> list[TestCase]:
    """Create test test cases."""
    test_cases = [
        TestCase(
            project_id=project.id,
            name="Login Test",
            description="Test user login functionality",
            test_type="functional",
            priority="high",
            tags=["auth", "login"],
            is_active=True,
        ),
        TestCase(
            project_id=project.id,
            name="API Authentication",
            description="Test API token validation",
            test_type="api",
            priority="critical",
            tags=["api", "auth"],
            is_active=True,
        ),
        TestCase(
            project_id=project.id,
            name="UI Responsiveness",
            description="Test responsive design across devices",
            test_type="ui",
            priority="medium",
            tags=["ui", "responsive"],
            is_active=True,
        ),
        TestCase(
            project_id=project.id,
            name="Performance Baseline",
            description="Test performance metrics against baseline",
            test_type="performance",
            priority="medium",
            tags=["performance"],
            is_active=True,
        ),
    ]
    session.add_all(test_cases)
    await session.flush()
    return test_cases


async def seed_executions(session: AsyncSession, project: Project, test_cases: list[TestCase]) -> None:
    """Create execution history."""
    now = datetime.utcnow()
    for i, test_case in enumerate(test_cases):
        execution = Execution(
            project_id=project.id,
            test_case_id=test_case.id,
            status="passed",
            duration_seconds=5.2 + i,
            pass_count=1,
            fail_count=0,
            skip_count=0,
            executed_at=now - timedelta(days=i),
            is_active=True,
        )
        session.add(execution)
    await session.flush()


async def seed_test_data(session: AsyncSession, project: Project) -> None:
    """Create reusable test data."""
    test_data = [
        TestData(
            project_id=project.id,
            name="Valid User Credentials",
            description="Standard user account for login tests",
            data={
                "email": "user@example.com",
                "password": "SecurePass123!",
                "name": "Test User",
            },
            is_active=True,
        ),
        TestData(
            project_id=project.id,
            name="Invalid Credentials",
            description="Invalid credentials for negative testing",
            data={
                "email": "invalid@example.com",
                "password": "wrong_password",
            },
            is_active=True,
        ),
        TestData(
            project_id=project.id,
            name="Edge Case Inputs",
            description="Boundary and edge case values for validation tests",
            data={
                "max_length_string": "a" * 1000,
                "empty_string": "",
                "special_chars": "!@#$%^&*()",
                "unicode": "こんにちは世界",
            },
            is_active=True,
        ),
    ]
    session.add_all(test_data)
    await session.flush()


async def seed_database() -> None:
    """Run all seeding operations in transaction."""
    async with async_session() as session:
        async with session.begin():
            try:
                print("🌱 Seeding database...")
                user = await seed_users(session)
                print(f"  ✓ Created user: {user.email}")

                project = await seed_projects(session, user)
                print(f"  ✓ Created project: {project.name}")

                test_cases = await seed_test_cases(session, project)
                print(f"  ✓ Created {len(test_cases)} test cases")

                await seed_executions(session, project, test_cases)
                print(f"  ✓ Created {len(test_cases)} executions")

                await seed_test_data(session, project)
                print(f"  ✓ Created 3 test data sets")

                print("✅ Database seeding completed successfully!")
            except Exception as e:
                print(f"❌ Database seeding failed: {e}")
                raise
            finally:
                await session.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
