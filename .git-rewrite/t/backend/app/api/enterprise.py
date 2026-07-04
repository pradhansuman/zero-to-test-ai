"""Enterprise API endpoints for Phase 4 Tasks 4-10."""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.notification_service import NotificationService
from app.services.event_system_service import EventService, EventType
from app.services.enterprise_services import (
    RateLimitService, ReportingService, PluginService, PerformanceMonitoringService
)
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/enterprise", tags=["enterprise"])
logger = StructuredLogger(__name__)


# Task 4: Notifications
@router.post("/notifications/send")
async def send_notification(
    title: str,
    message: str,
    channels: list[str],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Send notification via Email, Slack, Teams, or Webhook."""
    service = NotificationService(db)
    return await service.send_notification(current_user["id"], title, message, channels)


# Task 5-6: Events & Webhooks
@router.get("/events/{project_id}")
async def get_events(
    project_id: int,
    event_type: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get events for project."""
    service = EventService(db)
    return await service.get_events(project_id, event_type, limit=100)


@router.post("/webhooks/{project_id}")
async def create_webhook(
    project_id: int,
    url: str,
    events: list[str],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Register webhook for project."""
    service = EventService(db)
    return await service.create_webhook(project_id, url, events)


# Task 7: Rate Limiting & Quotas
@router.get("/quotas/usage")
async def get_quota_usage(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get current quota usage."""
    service = RateLimitService(db)
    return await service.get_quota_usage(current_user["id"])


@router.get("/rate-limit/{endpoint}")
async def check_rate_limit(
    endpoint: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Check rate limit for endpoint."""
    service = RateLimitService(db)
    limit_status = await service.check_rate_limit(current_user["id"], endpoint)
    if not limit_status["allowed"]:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return limit_status


# Task 8: Custom Reporting
@router.post("/reports/generate/{project_id}")
async def generate_report(
    project_id: int,
    report_type: str = Query("executive"),
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate custom report."""
    service = ReportingService(db)
    return await service.generate_report(
        project_id,
        report_type,
        {"start": start_date, "end": end_date}
    )


@router.post("/reports/schedule/{project_id}")
async def schedule_report(
    project_id: int,
    report_type: str,
    frequency: str,
    recipients: list[str],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Schedule recurring report delivery."""
    service = ReportingService(db)
    return await service.schedule_report(project_id, report_type, frequency, recipients)


# Task 9: Plugins & Extensions
@router.get("/plugins")
async def list_plugins(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """List all installed plugins."""
    service = PluginService(db)
    return await service.get_plugins()


@router.post("/plugins/register")
async def register_plugin(
    name: str,
    version: str,
    entry_point: str,
    permissions: list[str],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Register new plugin."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin required")

    service = PluginService(db)
    return await service.register_plugin(name, version, entry_point, permissions)


# Task 10: Performance Monitoring
@router.get("/monitoring/metrics")
async def get_performance_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get current performance metrics."""
    service = PerformanceMonitoringService(db)
    return await service.collect_metrics()


@router.get("/monitoring/report")
async def get_performance_report(
    hours: int = Query(24),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get performance report."""
    service = PerformanceMonitoringService(db)
    return await service.get_performance_report(hours)


@router.get("/monitoring/slow-queries")
async def get_slow_queries(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get slowest database queries."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin required")

    service = PerformanceMonitoringService(db)
    return await service.get_slow_queries()


@router.post("/monitoring/optimize")
async def optimize_database(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Run database optimization."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin required")

    service = PerformanceMonitoringService(db)
    return await service.optimize_database()
