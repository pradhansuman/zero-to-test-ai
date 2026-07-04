"""WebSocket routes for real-time execution streaming."""
from fastapi import APIRouter, WebSocket, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
from app.services.execution_streamer import ExecutionStreamManager
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/stream", tags=["execution-streaming"])
logger = StructuredLogger(__name__)

stream_manager = ExecutionStreamManager(None)


class ExecutionUpdateRequest(BaseModel):
    test_id: int = None
    status: str
    duration: float = None
    output: str = None


@router.websocket("/ws/execution/{execution_id}")
async def websocket_execution_stream(
    execution_id: str,
    websocket: WebSocket,
):
    """WebSocket endpoint for execution streaming."""
    stream_manager = ExecutionStreamManager(None)
    await stream_manager.stream_execution(execution_id, websocket)


@router.post("/update-test/{execution_id}")
async def update_test_progress(
    execution_id: str,
    request: ExecutionUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update test progress for streaming."""
    try:
        manager = ExecutionStreamManager(db)
        await manager.update_test_progress(
            execution_id=execution_id,
            test_id=request.test_id,
            status=request.status,
            duration=request.duration,
            output=request.output,
        )

        logger.info(
            "test_progress_updated",
            user_id=current_user["id"],
            execution_id=execution_id,
            test_id=request.test_id,
            status=request.status,
        )

        return {"success": True, "execution_id": execution_id}

    except Exception as e:
        logger.error("update_error", error=str(e))
        raise HTTPException(status_code=500, detail="Update failed")


@router.get("/execution-history/{execution_id}")
async def get_execution_history(
    execution_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get execution update history."""
    try:
        manager = ExecutionStreamManager(db)
        history = await manager.get_execution_history(execution_id, limit)

        return {
            "execution_id": execution_id,
            "updates": history,
            "count": len(history),
        }

    except Exception as e:
        logger.error("history_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get history")


@router.get("/active-executions")
async def get_active_executions(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get active execution streams."""
    try:
        manager = ExecutionStreamManager(db)
        active = manager.get_active_executions()

        return {
            "active_executions": active,
            "total_streams": len(active),
        }

    except Exception as e:
        logger.error("active_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get active executions")
