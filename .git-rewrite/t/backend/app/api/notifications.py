"""Notification API endpoints for Phase 4 Task 4."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.notification_service import NotificationService, NotificationChannel
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
logger = StructuredLogger(__name__)


class NotificationRequest(BaseModel):
    """Send notification request."""
    title: str
    message: str
    channels: list[str]
    data: dict = None


@router.post("/send")
async def send_notification(
    request: NotificationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Send notification via specified channels."""
    try:
        channels = [NotificationChannel(ch) for ch in request.channels]
        service = NotificationService(db)
        result = await service.send_notification(
            current_user["id"],
            request.title,
            request.message,
            channels,
            request.data
        )
        logger.info("notification_sent", user_id=current_user["id"], channels=request.channels)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send notification")


@router.post("/broadcast/{channel}")
async def broadcast_notification(
    channel: str,
    request: NotificationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Broadcast notification to all users on channel."""
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin required")

        service = NotificationService(db)
        result = await service.broadcast_to_channel(
            NotificationChannel(channel),
            request.title,
            request.message,
            request.data
        )
        logger.info("broadcast_sent", channel=channel)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to broadcast")
