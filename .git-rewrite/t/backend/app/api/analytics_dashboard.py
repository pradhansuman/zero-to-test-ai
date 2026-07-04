"""Analytics dashboard API endpoints."""
from fastapi import APIRouter, Depends, WebSocket, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.analytics_aggregator import AnalyticsAggregator
from app.services.analytics_service import AnalyticsService
from app.utils.logger import StructuredLogger
import asyncio
import json
from datetime import datetime

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
logger = StructuredLogger(__name__)


class WidgetConfig(BaseModel):
    """Widget configuration."""
    widget_type: str
    title: str
    metric_keys: list
    time_range: str = "30d"
    config: dict = None


class DashboardCreate(BaseModel):
    """Dashboard creation request."""
    name: str
    description: str = None
    is_default: bool = False

@router.get("/dashboard/{project_id}")
async def get_dashboard(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get dashboard metrics."""
    aggregator = AnalyticsAggregator(db)
    metrics = await aggregator.get_dashboard_metrics(project_id)
    logger.info("dashboard_retrieved", project_id=project_id, user_id=current_user["id"])
    return metrics

@router.get("/real-time/{project_id}")
async def get_realtime(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get real-time metrics."""
    aggregator = AnalyticsAggregator(db)
    metrics = await aggregator.get_real_time_metrics(project_id)
    logger.info("realtime_metrics_retrieved", project_id=project_id)
    return metrics

@router.websocket("/ws/dashboard/{project_id}")
async def websocket_dashboard(websocket: WebSocket, project_id: int):
    """WebSocket for real-time dashboard updates."""
    await websocket.accept()
    aggregator = AnalyticsAggregator(None)
    try:
        while True:
            metrics = await aggregator.get_dashboard_metrics(project_id)
            await websocket.send_json(metrics)
            import asyncio
            await asyncio.sleep(5)
    except Exception as e:
        logger.error("websocket_error", error=str(e))


# ===== Phase 4 Task 2: Advanced Analytics Dashboard Endpoints =====

@router.post("/dashboards/{project_id}")
async def create_dashboard(
    project_id: int,
    request: DashboardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a custom analytics dashboard."""
    try:
        service = AnalyticsService(db)
        result = await service.create_dashboard(
            user_id=current_user["id"],
            project_id=project_id,
            name=request.name,
            description=request.description,
            is_default=request.is_default
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        await db.commit()
        logger.info("dashboard_created", project_id=project_id, user_id=current_user["id"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create dashboard")


@router.get("/dashboards/{dashboard_id}")
async def get_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get dashboard configuration with widgets."""
    try:
        service = AnalyticsService(db)
        result = await service.get_dashboard(dashboard_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        logger.info("dashboard_retrieved", dashboard_id=dashboard_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard")


@router.post("/dashboards/{dashboard_id}/widgets")
async def add_widget(
    dashboard_id: int,
    widget: WidgetConfig,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Add a widget to a dashboard."""
    try:
        service = AnalyticsService(db)
        result = await service.add_widget(
            dashboard_id=dashboard_id,
            widget_type=widget.widget_type,
            title=widget.title,
            metric_keys=widget.metric_keys,
            time_range=widget.time_range,
            config=widget.config
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        await db.commit()
        logger.info("widget_added", dashboard_id=dashboard_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add widget")


@router.get("/metrics/{project_id}/{metric_type}")
async def get_realtime_metrics(
    project_id: int,
    metric_type: str,
    minutes: int = 60,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get real-time metrics aggregated over time window."""
    try:
        service = AnalyticsService(db)
        result = await service.get_realtime_metrics(project_id, metric_type, minutes)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


@router.get("/trends/{project_id}/{metric_type}")
async def get_trends(
    project_id: int,
    metric_type: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Calculate trend analysis for metric."""
    try:
        service = AnalyticsService(db)
        result = await service.get_trend_analysis(project_id, metric_type, days)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to calculate trends")


@router.get("/export/metrics/{project_id}/{metric_type}")
async def export_metrics_csv(
    project_id: int,
    metric_type: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Export metrics as CSV."""
    try:
        service = AnalyticsService(db)
        csv_data = await service.export_metrics_csv(project_id, metric_type, days)
        if not csv_data:
            raise HTTPException(status_code=400, detail="Failed to export metrics")
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=metrics_{metric_type}_{days}d.csv"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to export metrics")


@router.get("/export/report/{project_id}")
async def export_report(
    project_id: int,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Export detailed execution report."""
    try:
        service = AnalyticsService(db)
        result = await service.export_execution_report(project_id, days)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to export report")


@router.get("/flakiness/{project_id}")
async def get_flakiness_report(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get flaky tests report."""
    try:
        service = AnalyticsService(db)
        result = await service.get_flaky_tests(project_id)
        logger.info("flakiness_report_retrieved", project_id=project_id)
        return {"flaky_tests": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve flakiness report")


@router.websocket("/ws/realtime/{project_id}/{metric_type}")
async def websocket_realtime_metrics(
    websocket: WebSocket,
    project_id: int,
    metric_type: str,
):
    """WebSocket for real-time metric streaming."""
    await websocket.accept()
    try:
        while True:
            # In a real implementation, this would stream metrics from Redis/message queue
            data = {
                "project_id": project_id,
                "metric_type": metric_type,
                "timestamp": datetime.utcnow().isoformat(),
                "value": 0.85,  # Placeholder
            }
            await websocket.send_json(data)
            await asyncio.sleep(2)
    except Exception as e:
        logger.error("realtime_websocket_error", error=str(e))
