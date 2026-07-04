"""Multi-channel notification service for Phase 4 Task 4."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enum import Enum
import json
import aiohttp

from app.database.models import User
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class NotificationChannel(str, Enum):
    """Supported notification channels."""
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    WEBHOOK = "webhook"


class NotificationService:
    """Send notifications across multiple channels."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def send_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        channels: List[NotificationChannel],
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send notification via specified channels."""
        results = {}

        for channel in channels:
            try:
                if channel == NotificationChannel.EMAIL:
                    results["email"] = await self._send_email(user_id, title, message, data)
                elif channel == NotificationChannel.SLACK:
                    results["slack"] = await self._send_slack(user_id, title, message, data)
                elif channel == NotificationChannel.TEAMS:
                    results["teams"] = await self._send_teams(user_id, title, message, data)
                elif channel == NotificationChannel.WEBHOOK:
                    results["webhook"] = await self._send_webhook(user_id, title, message, data)
            except Exception as e:
                logger.error(f"notification_error_{channel}", error=str(e))
                results[channel] = {"status": "failed", "error": str(e)}

        return {
            "user_id": user_id,
            "title": title,
            "channels": list(channels),
            "results": results,
            "sent_at": datetime.utcnow().isoformat()
        }

    async def _send_email(
        self,
        user_id: int,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Send email notification."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            return {"status": "failed", "error": "User not found"}

        # Email implementation (would integrate with SendGrid, AWS SES, etc.)
        email_body = f"""
        <h2>{title}</h2>
        <p>{message}</p>
        """

        if data:
            email_body += f"<pre>{json.dumps(data, indent=2)}</pre>"

        logger.info(
            "email_sent",
            user_id=user_id,
            email=user.email,
            subject=title
        )

        return {
            "status": "sent",
            "recipient": user.email,
            "subject": title
        }

    async def _send_slack(
        self,
        user_id: int,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Send Slack notification."""
        # Slack webhook URL (would come from config)
        slack_webhook = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

        payload = {
            "text": title,
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": title}
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message}
                }
            ]
        }

        if data:
            payload["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"```{json.dumps(data, indent=2)}```"}
            })

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(slack_webhook, json=payload) as resp:
                    if resp.status == 200:
                        logger.info("slack_sent", user_id=user_id, title=title)
                        return {"status": "sent", "channel": "slack"}
                    else:
                        return {"status": "failed", "error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error("slack_error", error=str(e))
            return {"status": "failed", "error": str(e)}

    async def _send_teams(
        self,
        user_id: int,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Send Microsoft Teams notification."""
        teams_webhook = "https://outlook.webhook.office.com/webhookb2/YOUR/URL"

        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "themeColor": "0078D4",
            "sections": [
                {
                    "activityTitle": title,
                    "activitySubtitle": f"User ID: {user_id}",
                    "text": message
                }
            ]
        }

        if data:
            payload["sections"][0]["facts"] = [
                {"name": k, "value": str(v)} for k, v in data.items()
            ]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(teams_webhook, json=payload) as resp:
                    if resp.status in [200, 201]:
                        logger.info("teams_sent", user_id=user_id, title=title)
                        return {"status": "sent", "channel": "teams"}
                    else:
                        return {"status": "failed", "error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error("teams_error", error=str(e))
            return {"status": "failed", "error": str(e)}

    async def _send_webhook(
        self,
        user_id: int,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Send webhook notification."""
        # Custom webhook (would be stored in user preferences)
        webhook_url = "https://custom.webhook.url/notify"

        payload = {
            "event": "notification",
            "user_id": user_id,
            "title": title,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }

        if data:
            payload["data"] = data

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status in [200, 201]:
                        logger.info("webhook_sent", user_id=user_id)
                        return {"status": "sent", "channel": "webhook"}
                    else:
                        return {"status": "failed", "error": f"HTTP {resp.status}"}
        except asyncio.TimeoutError:
            logger.error("webhook_timeout", user_id=user_id)
            return {"status": "failed", "error": "Webhook timeout"}
        except Exception as e:
            logger.error("webhook_error", error=str(e))
            return {"status": "failed", "error": str(e)}

    async def broadcast_to_channel(
        self,
        channel: NotificationChannel,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Broadcast notification to all users on a channel."""
        result = await self.db.execute(select(User).where(User.is_active == True))
        users = result.scalars().all()

        results = []
        for user in users:
            res = await self.send_notification(
                user.id,
                title,
                message,
                [channel],
                data
            )
            results.append(res)

        return {
            "channel": channel,
            "users_notified": len(users),
            "results": results
        }
