"""Event system & webhooks for Phase 4 Tasks 5-6."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enum import Enum
import json
import hashlib
import aiohttp
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class EventType(str, Enum):
    """Event types."""
    TEST_STARTED = "test.started"
    TEST_PASSED = "test.passed"
    TEST_FAILED = "test.failed"
    EXECUTION_COMPLETED = "execution.completed"
    DASHBOARD_CREATED = "dashboard.created"
    WEBHOOK_TRIGGERED = "webhook.triggered"


class EventService:
    """Event streaming and webhook management."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_queue = []

    async def emit_event(
        self,
        event_type: EventType,
        project_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Emit an event."""
        event = {
            "id": f"{project_id}_{int(datetime.utcnow().timestamp() * 1000)}",
            "type": event_type,
            "project_id": project_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0"
        }

        self.event_queue.append(event)
        logger.info("event_emitted", event_type=event_type, project_id=project_id)

        # Trigger webhooks for this event
        await self._trigger_webhooks(event)

        return event

    async def _trigger_webhooks(self, event: Dict[str, Any]) -> None:
        """Trigger all webhooks for event."""
        # Get registered webhooks for project
        webhooks = await self._get_webhooks(event["project_id"])

        for webhook in webhooks:
            if event["type"] in webhook["events"]:
                await self._send_webhook_with_retry(webhook, event)

    async def _send_webhook_with_retry(
        self,
        webhook: Dict[str, Any],
        event: Dict[str, Any],
        retries: int = 3
    ) -> None:
        """Send webhook with exponential backoff retry."""
        for attempt in range(retries):
            try:
                # Add signature for security
                signature = self._generate_signature(webhook["secret"], json.dumps(event))

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        webhook["url"],
                        json=event,
                        headers={"X-QA-Signature": signature},
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as resp:
                        if resp.status in [200, 201, 202]:
                            logger.info("webhook_delivered", webhook_id=webhook["id"])
                            return

            except Exception as e:
                wait_time = 2 ** attempt
                logger.warning(f"webhook_retry_{attempt}", error=str(e), wait_seconds=wait_time)
                if attempt < retries - 1:
                    await asyncio.sleep(wait_time)

    def _generate_signature(self, secret: str, payload: str) -> str:
        """Generate HMAC signature for webhook."""
        return hashlib.sha256(f"{secret}{payload}".encode()).hexdigest()

    async def _get_webhooks(self, project_id: int) -> List[Dict[str, Any]]:
        """Get registered webhooks for project."""
        # Would query webhooks table
        return []

    async def get_events(
        self,
        project_id: int,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get events for project."""
        events = [e for e in self.event_queue if e["project_id"] == project_id]
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        return events[-limit:]

    async def create_webhook(
        self,
        project_id: int,
        url: str,
        events: List[EventType],
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register webhook for project."""
        webhook = {
            "id": f"wh_{project_id}_{int(datetime.utcnow().timestamp())}",
            "project_id": project_id,
            "url": url,
            "events": events,
            "secret": secret or "default-secret",
            "active": True,
            "created_at": datetime.utcnow().isoformat()
        }

        logger.info("webhook_created", webhook_id=webhook["id"], url=url)
        return webhook


import asyncio
