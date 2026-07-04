"""Analytics API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.services.analytics_service import AnalyticsService
from app.models.analytics_schema import (
    DashboardStats,
    TrendsResponse,
    TrendPoint,
    CoverageResponse,
    CoverageStats,
    FlakyTestsResponse,
    FlakyTest
)
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    project_id: int = Query(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get execution dashboard statistics for project."""
    try:
        service = AnalyticsService(db)
        stats = await service.get_dashboard_stats(project_id)
        logger.info(
            "Dashboard stats retrieved",
            project_id=project_id,
            user_id=current_user["id"]
        )
        return stats
    except Exception as e:
        logger.error(
            f"Error getting dashboard stats: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard stats"
        )


@router.get("/trends", response_model=TrendsResponse)
async def get_trends(
    project_id: int = Query(..., description="Project ID"),
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get execution trends over time."""
    try:
        service = AnalyticsService(db)
        trends = await service.get_trends(project_id, days=days)
        logger.info(
            "Trends retrieved",
            project_id=project_id,
            days=days,
            user_id=current_user["id"],
            trend_points=len(trends)
        )
        return {
            "project_id": project_id,
            "days": days,
            "trends": trends
        }
    except Exception as e:
        logger.error(
            f"Error getting trends: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trends"
        )


@router.get("/coverage", response_model=CoverageResponse)
async def get_coverage(
    project_id: int = Query(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get test coverage by type."""
    try:
        service = AnalyticsService(db)
        coverage_data = await service.get_coverage(project_id)
        logger.info(
            "Coverage retrieved",
            project_id=project_id,
            user_id=current_user["id"],
            total_tests=coverage_data["total"]
        )

        coverage = CoverageStats(
            e2e=coverage_data["e2e"],
            unit=coverage_data["unit"],
            integration=coverage_data["integration"],
            performance=coverage_data["performance"],
            total=coverage_data["total"]
        )

        return {
            "project_id": project_id,
            "coverage": coverage
        }
    except Exception as e:
        logger.error(
            f"Error getting coverage: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get coverage"
        )


@router.get("/flaky-tests", response_model=FlakyTestsResponse)
async def get_flaky_tests(
    project_id: int = Query(..., description="Project ID"),
    threshold: float = Query(0.7, description="Failure rate threshold", ge=0.0, le=1.0),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get flaky tests (high failure rate)."""
    try:
        service = AnalyticsService(db)
        flaky_tests = await service.get_flaky_tests(project_id, threshold=threshold)
        logger.info(
            "Flaky tests retrieved",
            project_id=project_id,
            user_id=current_user["id"],
            flaky_count=len(flaky_tests),
            threshold=threshold
        )
        return {
            "project_id": project_id,
            "threshold": threshold,
            "flaky_tests": flaky_tests,
            "count": len(flaky_tests)
        }
    except Exception as e:
        logger.error(
            f"Error getting flaky tests: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get flaky tests"
        )
