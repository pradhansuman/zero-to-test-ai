"""Real-time execution streaming service with WebSocket support."""
import asyncio
import json
from datetime import datetime
from typing import Dict, Set, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Execution, TestCase
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class ExecutionStreamManager:
    """Manages real-time execution streaming via WebSocket."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.active_connections: Dict[str, list] = {}
        self.execution_updates: Dict[str, list] = {}
        self.execution_status: Dict[str, Dict] = {}

    async def connect(self, execution_id: str, websocket):
        """Register WebSocket connection for execution.

        Args:
            execution_id: Execution ID
            websocket: WebSocket connection
        """
        await websocket.accept()

        if execution_id not in self.active_connections:
            self.active_connections[execution_id] = []
            self.execution_updates[execution_id] = []

        self.active_connections[execution_id].append(websocket)

        logger.info(
            "websocket_connected",
            execution_id=execution_id,
            connection_count=len(self.active_connections[execution_id]),
        )

    async def disconnect(self, execution_id: str, websocket):
        """Unregister WebSocket connection.

        Args:
            execution_id: Execution ID
            websocket: WebSocket connection
        """
        if execution_id in self.active_connections:
            self.active_connections[execution_id].remove(websocket)

            if not self.active_connections[execution_id]:
                del self.active_connections[execution_id]
                del self.execution_updates[execution_id]

        logger.info(
            "websocket_disconnected",
            execution_id=execution_id,
        )

    async def broadcast_execution_update(
        self,
        execution_id: str,
        update: Dict
    ):
        """Broadcast execution update to all connected clients.

        Args:
            execution_id: Execution ID
            update: Update data (status, progress, test results, etc.)
        """
        if execution_id not in self.active_connections:
            return

        # Add timestamp
        update["timestamp"] = datetime.utcnow().isoformat()
        update["execution_id"] = execution_id

        # Store update
        if execution_id in self.execution_updates:
            self.execution_updates[execution_id].append(update)
            # Keep only last 100 updates
            if len(self.execution_updates[execution_id]) > 100:
                self.execution_updates[execution_id] = (
                    self.execution_updates[execution_id][-100:]
                )

        # Broadcast to all connected clients
        disconnected = []

        for websocket in self.active_connections[execution_id]:
            try:
                await websocket.send_json(update)
            except Exception as e:
                logger.error(
                    "broadcast_error",
                    execution_id=execution_id,
                    error=str(e),
                )
                disconnected.append(websocket)

        # Clean up disconnected clients
        for ws in disconnected:
            await self.disconnect(execution_id, ws)

    async def stream_execution(self, execution_id: str, websocket):
        """Stream execution progress to client.

        Args:
            execution_id: Execution ID
            websocket: WebSocket connection
        """
        await self.connect(execution_id, websocket)

        try:
            # Send initial status
            await self.broadcast_execution_update(
                execution_id,
                {
                    "type": "execution_start",
                    "status": "running",
                    "progress": 0,
                    "total_tests": 0,
                    "completed_tests": 0,
                },
            )

            # Keep connection alive and receive heartbeats
            while True:
                try:
                    # Wait for client message (heartbeat or control command)
                    data = await asyncio.wait_for(
                        websocket.receive_json(),
                        timeout=30.0  # 30 second heartbeat timeout
                    )

                    if data.get("type") == "heartbeat":
                        # Respond to heartbeat
                        await websocket.send_json({"type": "heartbeat_ack"})

                except asyncio.TimeoutError:
                    # Send heartbeat request
                    await websocket.send_json({"type": "heartbeat_request"})

        except Exception as e:
            logger.error(
                "stream_error",
                execution_id=execution_id,
                error=str(e),
            )
        finally:
            await self.disconnect(execution_id, websocket)

    async def update_test_progress(
        self,
        execution_id: str,
        test_id: int,
        status: str,
        duration: float = None,
        output: str = None,
    ):
        """Update progress for a single test.

        Args:
            execution_id: Execution ID
            test_id: Test case ID
            status: Test status (running, passed, failed)
            duration: Test execution duration in seconds
            output: Test output/logs
        """
        update = {
            "type": "test_update",
            "test_id": test_id,
            "status": status,
        }

        if duration is not None:
            update["duration"] = duration

        if output:
            update["output"] = output

        await self.broadcast_execution_update(execution_id, update)

    async def update_execution_status(
        self,
        execution_id: str,
        status: str,
        progress: int = None,
        total_tests: int = None,
        completed_tests: int = None,
        passed: int = None,
        failed: int = None,
    ):
        """Update overall execution status.

        Args:
            execution_id: Execution ID
            status: Execution status (running, completed, failed)
            progress: Progress percentage (0-100)
            total_tests: Total tests to run
            completed_tests: Tests completed so far
            passed: Tests passed
            failed: Tests failed
        """
        update = {
            "type": "execution_update",
            "status": status,
        }

        if progress is not None:
            update["progress"] = progress

        if total_tests is not None:
            update["total_tests"] = total_tests

        if completed_tests is not None:
            update["completed_tests"] = completed_tests

        if passed is not None:
            update["passed"] = passed

        if failed is not None:
            update["failed"] = failed

        self.execution_status[execution_id] = update

        await self.broadcast_execution_update(execution_id, update)

    async def send_execution_log(
        self,
        execution_id: str,
        log_line: str,
        level: str = "info",
    ):
        """Send log line to execution stream.

        Args:
            execution_id: Execution ID
            log_line: Log message
            level: Log level (debug, info, warning, error)
        """
        update = {
            "type": "log",
            "message": log_line,
            "level": level,
        }

        await self.broadcast_execution_update(execution_id, update)

    async def send_test_failure(
        self,
        execution_id: str,
        test_id: int,
        test_name: str,
        error_message: str,
        screenshot: str = None,
        stack_trace: str = None,
    ):
        """Send test failure details.

        Args:
            execution_id: Execution ID
            test_id: Test case ID
            test_name: Test name
            error_message: Error message
            screenshot: Screenshot data (base64)
            stack_trace: Full stack trace
        """
        update = {
            "type": "test_failure",
            "test_id": test_id,
            "test_name": test_name,
            "error_message": error_message,
        }

        if screenshot:
            update["screenshot"] = screenshot

        if stack_trace:
            update["stack_trace"] = stack_trace

        await self.broadcast_execution_update(execution_id, update)

    async def send_execution_complete(
        self,
        execution_id: str,
        duration: float,
        total_tests: int,
        passed: int,
        failed: int,
        pass_rate: float,
    ):
        """Send execution completion notification.

        Args:
            execution_id: Execution ID
            duration: Total execution duration
            total_tests: Total tests run
            passed: Tests passed
            failed: Tests failed
            pass_rate: Pass rate percentage
        """
        update = {
            "type": "execution_complete",
            "status": "completed",
            "duration": duration,
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "pass_rate": pass_rate,
        }

        await self.broadcast_execution_update(execution_id, update)

    async def get_execution_history(
        self,
        execution_id: str,
        limit: int = 50,
    ) -> list:
        """Get recent execution updates.

        Args:
            execution_id: Execution ID
            limit: Maximum updates to return

        Returns:
            List of recent updates
        """
        if execution_id not in self.execution_updates:
            return []

        updates = self.execution_updates[execution_id]
        return updates[-limit:] if len(updates) > limit else updates

    def get_active_executions(self) -> Dict[str, int]:
        """Get count of active connections per execution.

        Returns:
            Dictionary mapping execution_id to connection count
        """
        return {
            exec_id: len(connections)
            for exec_id, connections in self.active_connections.items()
        }

    def get_connection_count(self, execution_id: str) -> int:
        """Get connection count for specific execution.

        Args:
            execution_id: Execution ID

        Returns:
            Number of active connections
        """
        return len(self.active_connections.get(execution_id, []))
