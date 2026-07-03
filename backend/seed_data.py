"""Seed data for database initialization."""
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.app.database.base import Base
from backend.app.database.models import (
    User, Project, TestCase, Execution, ExecutionResult, Report, AuditLog,
    UserRole, TestFramework, ExecutionStatus
)


async def init_db(database_url: str = "postgresql+asyncpg://user:password@localhost/qa_db"):
    """Initialize database and seed data."""
    engine = create_async_engine(database_url, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        # Create admin user
        admin = User(
            email="admin@example.com",
            username="admin",
            password_hash="hashed_password",
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin)
        await session.flush()

        # Create sample project
        project = Project(
            name="Demo QA Project",
            description="Sample project for testing",
            owner_id=admin.id,
            test_framework=TestFramework.PLAYWRIGHT,
            is_active=True,
        )
        session.add(project)
        await session.flush()

        # Create sample test case
        test_case = TestCase(
            project_id=project.id,
            name="Login Test",
            description="Test user login functionality",
            test_code="// Playwright test code here",
            test_type="e2e",
            tags=["smoke", "login"],
            is_active=True,
        )
        session.add(test_case)
        await session.flush()

        # Create sample execution
        execution = Execution(
            project_id=project.id,
            status=ExecutionStatus.PASSED,
            total_tests=1,
            passed=1,
            failed=0,
            skipped=0,
            duration_seconds=5.23,
            started_at=datetime.utcnow(),
            ended_at=datetime.utcnow(),
        )
        session.add(execution)
        await session.flush()

        # Create execution result
        result = ExecutionResult(
            execution_id=execution.id,
            test_case_id=test_case.id,
            status=ExecutionStatus.PASSED,
            duration_seconds=5.23,
        )
        session.add(result)

        # Create report
        report = Report(
            execution_id=execution.id,
            title="Execution Report - Demo QA Project",
            summary="All tests passed",
            html_content="<html><body>Report</body></html>",
        )
        session.add(report)

        # Create audit log
        audit = AuditLog(
            user_id=admin.id,
            action="CREATE",
            resource_type="Project",
            resource_id=project.id,
            details={"name": "Demo QA Project"},
        )
        session.add(audit)

        await session.commit()
        print("✅ Database initialized with seed data")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
