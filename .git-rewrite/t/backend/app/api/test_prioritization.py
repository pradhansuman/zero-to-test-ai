"""Test prioritization API endpoints for Phase 4 Task 3."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.test_prioritization_service import TestPrioritizationService
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/prioritization", tags=["prioritization"])
logger = StructuredLogger(__name__)


class CodeChange(BaseModel):
    """Code change information."""
    file: str
    module: str = ""


class PrioritizationRequest(BaseModel):
    """Request to prioritize tests."""
    test_ids: list[int]
    code_changes: list[CodeChange]


class TestPrioritizationResponse(BaseModel):
    """Prioritized test with scores."""
    test_id: int
    test_name: str
    priority_score: float
    risk_score: float
    impact_score: float
    duration_score: float
    stability_score: float
    order: int
    reasons: list[str]


@router.post("/prioritize/{project_id}")
async def prioritize_tests(
    project_id: int,
    request: PrioritizationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Prioritize tests based on risk, impact, and performance.
    Returns tests ordered by priority score (highest first).
    """
    try:
        service = TestPrioritizationService(db)

        # Convert code changes to dict format
        code_changes = [{"file": c.file, "module": c.module} for c in request.code_changes]

        result = await service.prioritize_tests(
            project_id=project_id,
            test_ids=request.test_ids,
            code_changes=code_changes
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info(
            "tests_prioritized_api",
            project_id=project_id,
            user_id=current_user["id"],
            test_count=len(request.test_ids)
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("prioritization_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to prioritize tests")


@router.get("/performance-profile/{test_id}")
async def get_performance_profile(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get performance profile for a test."""
    try:
        service = TestPrioritizationService(db)
        result = await service.get_performance_profile(test_id)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        logger.info("performance_profile_retrieved", test_id=test_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("performance_profile_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve performance profile")


@router.post("/performance-profile/{project_id}/{test_id}")
async def record_test_duration(
    project_id: int,
    test_id: int,
    duration: float,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Record actual test execution duration for profiling."""
    try:
        service = TestPrioritizationService(db)
        result = await service.update_performance_profile(
            project_id=project_id,
            test_case_id=test_id,
            duration=duration
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        await db.commit()

        logger.info(
            "test_duration_recorded",
            test_id=test_id,
            duration=duration
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error("duration_recording_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to record test duration")


@router.get("/recommendations/{project_id}")
async def get_prioritization_recommendations(
    project_id: int,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get prioritization recommendations for a project.
    Based on recent code changes and historical data.
    """
    try:
        service = TestPrioritizationService(db)

        # For now, return stub recommendations
        # In production, this would analyze recent commits and failures
        result = {
            "project_id": project_id,
            "recommendations": [
                {
                    "test_id": 1,
                    "test_name": "test_api_users",
                    "priority_score": 0.92,
                    "reason": "Recent API changes + high failure impact"
                },
                {
                    "test_id": 5,
                    "test_name": "test_database_migration",
                    "priority_score": 0.88,
                    "reason": "Database schema changes detected"
                },
                {
                    "test_id": 12,
                    "test_name": "test_ui_login",
                    "priority_score": 0.75,
                    "reason": "UI changes + moderate flakiness"
                },
            ],
            "generated_at": "2026-07-03T15:00:00Z"
        }

        logger.info("recommendations_retrieved", project_id=project_id)
        return result
    except Exception as e:
        logger.error("recommendations_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve recommendations")
