"""API routes for advanced test scheduling."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from app.dependencies import get_db, get_current_user
from app.services.scheduler import TestScheduler
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/scheduler", tags=["scheduling"])
logger = StructuredLogger(__name__)


class ScheduleRequest(BaseModel):
    test_ids: List[int]
    priority: str = "normal"
    resource_constraints: Optional[Dict] = None


@router.post("/schedule-tests")
async def schedule_tests(
    request: ScheduleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Schedule tests for execution."""
    try:
        scheduler = TestScheduler(db)
        result = await scheduler.schedule_tests(
            test_ids=request.test_ids,
            priority=request.priority,
            resource_constraints=request.resource_constraints,
        )
        logger.info("tests_scheduled", user_id=current_user["id"], count=len(request.test_ids))
        return result
    except Exception as e:
        logger.error("scheduling_error", error=str(e))
        raise HTTPException(status_code=500, detail="Scheduling failed")


@router.put("/reschedule/{schedule_id}")
async def reschedule(
    schedule_id: str,
    priority: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Reschedule existing schedule."""
    try:
        scheduler = TestScheduler(db)
        result = await scheduler.reschedule_tests(schedule_id, priority)
        logger.info("schedule_rescheduled", user_id=current_user["id"], schedule_id=schedule_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Rescheduling failed")


@router.delete("/cancel/{schedule_id}")
async def cancel_schedule(
    schedule_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Cancel a schedule."""
    try:
        scheduler = TestScheduler(db)
        result = await scheduler.cancel_schedule(schedule_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Cancellation failed")


@router.get("/status/{schedule_id}")
async def get_status(
    schedule_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get schedule status."""
    try:
        scheduler = TestScheduler(db)
        return await scheduler.get_schedule_status(schedule_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Status check failed")
