"""WebSocket API for live execution streaming."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
import json
import asyncio
from typing import Dict, List

from app.database.session import SessionLocal
from app.services.execution_service import ExecutionService
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["websocket"])

# Track active WebSocket connections
class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, execution_id: int, websocket: WebSocket):
        """Accept new connection."""
        await websocket.accept()
        if execution_id not in self.active_connections:
            self.active_connections[execution_id] = []
        self.active_connections[execution_id].append(websocket)
        logger.info(
            "WebSocket connection established",
            execution_id=execution_id,
            total_connections=len(self.active_connections[execution_id])
        )

    async def disconnect(self, execution_id: int, websocket: WebSocket):
        """Remove disconnected connection."""
        if execution_id in self.active_connections:
            self.active_connections[execution_id].remove(websocket)
            if not self.active_connections[execution_id]:
                del self.active_connections[execution_id]
            logger.info(
                "WebSocket disconnected",
                execution_id=execution_id,
                remaining=len(self.active_connections.get(execution_id, []))
            )

    async def broadcast(self, execution_id: int, message: dict):
        """Broadcast message to all connections for execution."""
        if execution_id not in self.active_connections:
            return

        disconnected = []
        for connection in self.active_connections[execution_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(
                    f"Error sending WebSocket message: {str(e)}",
                    execution_id=execution_id,
                    error=str(e)
                )
                disconnected.append(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            await self.disconnect(execution_id, connection)

    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send message to single connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(
                f"Error sending personal message: {str(e)}",
                error=str(e)
            )


manager = ConnectionManager()


@router.websocket("/ws/execution/{execution_id}")
async def websocket_endpoint(websocket: WebSocket, execution_id: int):
    """WebSocket endpoint for live execution streaming."""
    try:
        await manager.connect(execution_id, websocket)

        async with SessionLocal() as session:
            service = ExecutionService(session)

            # Send initial execution state
            try:
                execution = await service.get_execution(execution_id)
                initial_message = {
                    "type": "execution_started",
                    "execution_id": execution_id,
                    "status": execution.status,
                    "total_tests": execution.total_tests,
                    "passed": execution.passed,
                    "failed": execution.failed,
                    "skipped": execution.skipped,
                    "duration": execution.duration_seconds,
                    "started_at": execution.started_at.isoformat() if execution.started_at else None
                }
                await manager.send_personal(websocket, initial_message)
            except Exception as e:
                logger.error(
                    f"Error sending initial state: {str(e)}",
                    execution_id=execution_id,
                    error=str(e)
                )
                await websocket.send_json({
                    "type": "error",
                    "message": "Execution not found"
                })
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return

        # Listen for incoming messages (heartbeat/keep-alive)
        while True:
            try:
                # Wait for heartbeat/keep-alive message with 60 second timeout
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=300.0  # 5 minute timeout
                )

                if data.get("type") == "ping":
                    await manager.send_personal(websocket, {
                        "type": "pong",
                        "execution_id": execution_id
                    })

            except asyncio.TimeoutError:
                # Connection idle - send keep-alive
                await manager.send_personal(websocket, {
                    "type": "keep_alive",
                    "execution_id": execution_id
                })
            except WebSocketDisconnect:
                await manager.disconnect(execution_id, websocket)
                logger.info(
                    "WebSocket closed",
                    execution_id=execution_id,
                    code=status.WS_1000_NORMAL_CLOSURE
                )
                break
            except Exception as e:
                logger.error(
                    f"WebSocket error: {str(e)}",
                    execution_id=execution_id,
                    error=str(e)
                )
                await manager.disconnect(execution_id, websocket)
                break

    except Exception as e:
        logger.error(
            f"WebSocket connection error: {str(e)}",
            execution_id=execution_id,
            error=str(e)
        )
        try:
            await websocket.close(code=status.WS_1011_SERVER_ERROR)
        except Exception:
            pass


async def broadcast_execution_update(
    execution_id: int,
    status: str,
    passed: int = 0,
    failed: int = 0,
    skipped: int = 0,
    duration: float = 0.0,
    message: str = ""
):
    """Broadcast execution update to all connected clients."""
    update = {
        "type": "execution_update",
        "execution_id": execution_id,
        "status": status,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration": duration,
        "message": message
    }
    await manager.broadcast(execution_id, update)
    logger.debug(
        "Broadcasted execution update",
        execution_id=execution_id,
        status=status,
        passed=passed,
        failed=failed
    )


async def broadcast_execution_complete(
    execution_id: int,
    status: str,
    passed: int,
    failed: int,
    skipped: int,
    duration: float
):
    """Broadcast execution completion to all connected clients."""
    completion = {
        "type": "execution_complete",
        "execution_id": execution_id,
        "status": status,
        "total_tests": passed + failed + skipped,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration": duration,
        "pass_rate": round((passed / (passed + failed + skipped) * 100) if (passed + failed + skipped) > 0 else 0, 2)
    }
    await manager.broadcast(execution_id, completion)
    logger.info(
        "Broadcasted execution completion",
        execution_id=execution_id,
        status=status,
        passed=passed,
        failed=failed
    )
