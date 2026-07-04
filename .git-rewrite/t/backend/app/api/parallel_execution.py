"""API routes for parallel test execution."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List

from app.dependencies import get_db, get_current_user
from app.services.parallel_executor import ParallelExecutor
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/execution", tags=["parallel-execution"])
logger = StructuredLogger(__name__)


class ParallelExecutionRequest(BaseModel):
    test_ids: List[int] = Field(..., description="Test case IDs to execute")
    workers: int = Field(4, description="Number of parallel workers")


@router.post("/parallel-execute")
async def parallel_execute(
    request: ParallelExecutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Execute tests in parallel across multiple workers."""
    try:
        executor = ParallelExecutor(db, request.workers)
        result = await executor.execute_parallel(
            test_ids=request.test_ids,
            workers=request.workers,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info(
            "parallel_execution_endpoint",
            user_id=current_user["id"],
            test_count=len(request.test_ids),
            workers=request.workers,
            passed=result.get("passed"),
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("parallel_execution_error", error=str(e))
        raise HTTPException(status_code=500, detail="Execution failed")


@router.get("/execution-status")
async def get_status(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get parallel execution status."""
    try:
        executor = ParallelExecutor(db)
        status = await executor.get_execution_status()

        return status

    except Exception as e:
        logger.error("status_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get status")
