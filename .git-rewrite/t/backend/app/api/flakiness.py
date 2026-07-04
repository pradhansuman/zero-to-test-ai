"""Flakiness detection API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.flakiness_detector import FlakinessDetector
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/flakiness", tags=["flakiness"])
logger = StructuredLogger(__name__)

@router.post("/detect/{project_id}")
async def detect_flaky(
    project_id: int,
    run_count: int = 5,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Detect flaky tests in project."""
    try:
        detector = FlakinessDetector(db)
        result = await detector.detect_flaky_tests(project_id, run_count)
        logger.info("flaky_detection_run", project_id=project_id, runs=run_count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Detection failed")

@router.get("/statistics/{project_id}")
async def get_flaky_stats(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get flakiness statistics."""
    try:
        detector = FlakinessDetector(db)
        stats = await detector.get_flaky_statistics(project_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")
