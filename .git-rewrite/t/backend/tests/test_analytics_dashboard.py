"""Tests for Phase 4 Task 2: Advanced Analytics Dashboard."""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import (
    Project, User, Execution, ExecutionResult, ExecutionStatus,
    TestCase, Metric, UserRole, TestFramework
)
from app.services.analytics_service import AnalyticsService


class TestAnalyticsDashboard:
    """Test suite for analytics dashboard functionality."""

    async def test_create_dashboard(self, test_db: AsyncSession):
        """Test creating a custom dashboard."""
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash="hashed",
            role=UserRole.ADMIN
        )
        test_db.add(user)
        await test_db.flush()

        project = Project(
            name="Test Project",
            owner_id=user.id,
            test_framework=TestFramework.PLAYWRIGHT
        )
        test_db.add(project)
        await test_db.commit()

        service = AnalyticsService(test_db)

        result = await service.create_dashboard(
            user_id=user.id,
            project_id=project.id,
            name="My Dashboard",
            description="Test dashboard",
            is_default=True
        )

        assert result.get("id") is not None
        assert result.get("name") == "My Dashboard"
        assert result.get("project_id") == project.id
        assert "created_at" in result

    async def test_add_widget_to_dashboard(self, test_db: AsyncSession):
        """Test adding widget to dashboard."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.commit()

        service = AnalyticsService(test_db)

        dashboard = await service.create_dashboard(
            user_id=user.id,
            project_id=project.id,
            name="Test Dashboard"
        )
        await test_db.commit()
        dashboard_id = dashboard.get("id")

        result = await service.add_widget(
            dashboard_id=dashboard_id,
            widget_type="line_chart",
            title="Pass Rate Trend",
            metric_keys=["pass_rate"],
            time_range="30d",
            config={"yAxis": {"min": 0, "max": 100}}
        )
        await test_db.commit()

        assert result.get("id") is not None
        assert result.get("widget_type") == "line_chart"
        assert result.get("title") == "Pass Rate Trend"

    async def test_trend_analysis(self, test_db: AsyncSession):
        """Test trend analysis calculation."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        for i in range(30):
            metric = Metric(
                project_id=project.id,
                metric_type="pass_rate",
                value=80 + (i % 20),
                timestamp=datetime.utcnow() - timedelta(days=30-i),
                tags={"source": "execution"}
            )
            test_db.add(metric)
        await test_db.commit()

        service = AnalyticsService(test_db)
        result = await service.get_trend_analysis(
            project_id=project.id,
            metric_type="pass_rate",
            period_days=30
        )

        assert result.get("metric_type") == "pass_rate"
        assert result.get("period_days") == 30
        assert "average" in result
        assert "trend" in result

    async def test_export_metrics_csv(self, test_db: AsyncSession):
        """Test exporting metrics as CSV."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        for i in range(10):
            metric = Metric(
                project_id=project.id,
                metric_type="pass_rate",
                value=85 + i,
                timestamp=datetime.utcnow() - timedelta(days=10-i),
                tags={"source": "execution"}
            )
            test_db.add(metric)
        await test_db.commit()

        service = AnalyticsService(test_db)
        csv_data = await service.export_metrics_csv(
            project_id=project.id,
            metric_type="pass_rate",
            days=30
        )

        assert csv_data is not None
        assert "timestamp,value,tags" in csv_data
        assert len(csv_data) > 0

    async def test_get_execution_stats(self, test_db: AsyncSession):
        """Test getting execution statistics."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        for i in range(5):
            execution = Execution(
                project_id=project.id,
                status=ExecutionStatus.PASSED if i % 2 == 0 else ExecutionStatus.FAILED,
                total_tests=10,
                passed=9 if i % 2 == 0 else 5,
                failed=1 if i % 2 == 0 else 5,
                duration_seconds=60.0,
                started_at=datetime.utcnow() - timedelta(days=5-i)
            )
            test_db.add(execution)
        await test_db.commit()

        service = AnalyticsService(test_db)
        result = await service.get_dashboard_stats(
            project_id=project.id
        )

        assert result.get("project_id") == project.id
        assert "total_executions" in result
        assert "average_pass_rate" in result
        assert result.get("total_executions") > 0

    async def test_record_metric(self, test_db: AsyncSession):
        """Test recording metrics."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.commit()

        service = AnalyticsService(test_db)

        result = await service.record_metric(
            project_id=project.id,
            metric_type="test_duration",
            value=5.5,
            tags={"test_type": "e2e"}
        )
        await test_db.commit()

        assert result.get("id") is not None
        assert "timestamp" in result
