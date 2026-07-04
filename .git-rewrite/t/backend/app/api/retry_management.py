"""API routes for smart retry management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.dependencies import get_db, get_current_user
from app.services.retry_manager import RetryManager
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ai", tags=["retry-management"])
logger = StructuredLogger(__name__)


class RetryExecutionRequest(BaseModel):
    test_case_id: int
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay: float = 1.0


class FlakyDetectionRequest(BaseModel):
    project_id: int
    run_count: int = 5


class RetryPolicyRequest(BaseModel):
    project_id: int
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay: float = 1.0


@router.post("/execute-with-retry")
async def execute_with_retry(
    request: RetryExecutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Execute test with exponential backoff retry."""
    try:
        manager = RetryManager(db)
        result = await manager.execute_with_retry(
            test_case_id=request.test_case_id,
            max_retries=request.max_retries,
            backoff_factor=request.backoff_factor,
            initial_delay=request.initial_delay,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info(
            "test_executed_with_retry",
            user_id=current_user["id"],
            test_id=request.test_case_id,
            attempts=result.get("attempt"),
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("retry_execution_error", error=str(e))
        raise HTTPException(status_code=500, detail="Retry execution failed")


@router.post("/detect-flaky-tests")
async def detect_flaky(
    request: FlakyDetectionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Detect flaky tests by running them multiple times."""
    try:
        manager = RetryManager(db)
        result = await manager.detect_flaky_tests(
            project_id=request.project_id,
            run_count=request.run_count,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info(
            "flaky_tests_detected",
            user_id=current_user["id"],
            project_id=request.project_id,
            flaky_count=result.get("flaky_tests"),
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("flaky_detection_error", error=str(e))
        raise HTTPException(status_code=500, detail="Flaky detection failed")


@router.post("/configure-retry-policy")
async def configure_policy(
    request: RetryPolicyRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Configure retry policy for a project."""
    try:
        manager = RetryManager(db)
        result = await manager.configure_retry_policy(
            project_id=request.project_id,
            max_retries=request.max_retries,
            backoff_factor=request.backoff_factor,
            initial_delay=request.initial_delay,
        )

        logger.info(
            "retry_policy_configured",
            user_id=current_user["id"],
            project_id=request.project_id,
        )

        return result
    except Exception as e:
        logger.error("policy_configuration_error", error=str(e))
        raise HTTPException(status_code=500, detail="Configuration failed")


@router.get("/retry-statistics")
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get retry statistics."""
    try:
        manager = RetryManager(db)
        stats = await manager.get_retry_statistics()

        logger.info("retry_statistics_retrieved", user_id=current_user["id"])

        return stats
    except Exception as e:
        logger.error("statistics_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")
