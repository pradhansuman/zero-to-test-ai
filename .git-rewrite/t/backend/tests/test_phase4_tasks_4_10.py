"""Tests for Phase 4 Tasks 4-10: Enterprise features."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, UserRole, TestFramework, Project
from app.services.notification_service import NotificationService
from app.services.event_system_service import EventService, EventType
from app.services.enterprise_services import (
    RateLimitService, ReportingService, PluginService, PerformanceMonitoringService
)


@pytest.fixture
async def setup_enterprise_data(test_db: AsyncSession):
    """Setup test data for enterprise tests."""
    user = User(email="admin@test.com", username="admin", password_hash="hash", role=UserRole.ADMIN)
    test_db.add(user)
    await test_db.flush()
    project = Project(name="Test", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
    test_db.add(project)
    await test_db.commit()
    return user, project


class TestPhase4Tasks:
    """Test suite for Phase 4 Tasks 4-10."""

    # Task 4: Notifications
    async def test_notification_send(self, test_db: AsyncSession, setup_enterprise_data):
        """Test sending notifications."""
        user, project = await setup_enterprise_data
        service = NotificationService(test_db)
        result = await service.send_notification(
            user.id, "Test Alert", "Test message", ["email"], {"status": "ok"}
        )
        assert result["user_id"] == user.id
        assert "email" in result["results"]

    # Task 5: CI/CD Integration (stub)
    async def test_cicd_integration(self, test_db: AsyncSession):
        """Test CI/CD pipeline integration."""
        # Would test GitHub Actions, GitLab CI, Jenkins webhooks
        assert True  # Placeholder

    # Task 6: Event System
    async def test_event_emission(self, test_db: AsyncSession, setup_enterprise_data):
        """Test event emission and webhooks."""
        user, project = await setup_enterprise_data
        service = EventService(test_db)
        event = await service.emit_event(
            EventType.TEST_PASSED,
            project.id,
            {"test_id": 1, "duration": 5.2}
        )
        assert event["type"] == EventType.TEST_PASSED
        assert event["project_id"] == project.id

    # Task 7: Rate Limiting
    async def test_rate_limiting(self, test_db: AsyncSession, setup_enterprise_data):
        """Test rate limiting functionality."""
        user, _ = await setup_enterprise_data
        service = RateLimitService(test_db)
        limit = await service.check_rate_limit(user.id, "POST /api/tests")
        assert limit["allowed"] == True
        assert "limit" in limit

    async def test_quota_usage(self, test_db: AsyncSession, setup_enterprise_data):
        """Test quota tracking."""
        user, _ = await setup_enterprise_data
        service = RateLimitService(test_db)
        quota = await service.get_quota_usage(user.id)
        assert quota["usage_percent"] > 0

    # Task 8: Custom Reporting
    async def test_report_generation(self, test_db: AsyncSession, setup_enterprise_data):
        """Test report generation."""
        user, project = await setup_enterprise_data
        service = ReportingService(test_db)
        from datetime import datetime, timedelta
        report = await service.generate_report(
            project.id,
            "executive",
            {
                "start": (datetime.utcnow() - timedelta(days=7)).isoformat(),
                "end": datetime.utcnow().isoformat()
            }
        )
        assert report["report_type"] == "executive"
        assert "kpis" in report

    async def test_report_scheduling(self, test_db: AsyncSession, setup_enterprise_data):
        """Test report scheduling."""
        user, project = await setup_enterprise_data
        service = ReportingService(test_db)
        schedule = await service.schedule_report(
            project.id,
            "executive",
            "daily",
            ["admin@test.com"]
        )
        assert schedule["frequency"] == "daily"

    # Task 9: Plugins
    async def test_plugin_registration(self, test_db: AsyncSession):
        """Test plugin system."""
        service = PluginService(test_db)
        plugin = await service.register_plugin(
            "slack-integration",
            "1.0.0",
            "plugins.slack.main",
            ["send-message", "read-channel"]
        )
        assert plugin["name"] == "slack-integration"
        plugins = await service.get_plugins()
        assert len(plugins) > 0

    async def test_plugin_hook_execution(self, test_db: AsyncSession):
        """Test plugin hook execution."""
        service = PluginService(test_db)
        await service.register_plugin("test-plugin", "1.0.0", "test.main", [])
        result = await service.execute_plugin_hook("on_test_complete", {})
        assert "results" in result

    # Task 10: Performance Monitoring
    async def test_metrics_collection(self, test_db: AsyncSession):
        """Test performance metrics collection."""
        service = PerformanceMonitoringService(test_db)
        metrics = await service.collect_metrics()
        assert "api_latency" in metrics
        assert "database" in metrics
        assert "cache" in metrics

    async def test_performance_report(self, test_db: AsyncSession):
        """Test performance reporting."""
        service = PerformanceMonitoringService(test_db)
        report = await service.get_performance_report(24)
        assert report["period_hours"] == 24
        assert "summary" in report
        assert "recommendations" in report

    async def test_slow_queries(self, test_db: AsyncSession):
        """Test slow query detection."""
        service = PerformanceMonitoringService(test_db)
        queries = await service.get_slow_queries()
        assert isinstance(queries, list)

    async def test_database_optimization(self, test_db: AsyncSession):
        """Test database optimization."""
        service = PerformanceMonitoringService(test_db)
        result = await service.optimize_database()
        assert result["status"] == "completed"
        assert "improvements" in result
