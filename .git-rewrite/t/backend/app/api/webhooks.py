"""Webhook API endpoints for GitHub, Jira, and Slack."""
from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional, Dict, Any
import hmac
import hashlib

from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


def verify_github_signature(payload_body: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature."""
    try:
        expected_signature = "sha256=" + hmac.new(
            secret.encode(),
            payload_body,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Error verifying GitHub signature: {str(e)}", error=str(e))
        return False


@router.post("/github")
async def github_webhook(
    request_body: Dict[str, Any],
    x_github_event: str = Header(None),
    x_hub_signature_256: Optional[str] = Header(None)
):
    """Handle GitHub webhook events."""
    try:
        # Log webhook event
        event_type = x_github_event or request_body.get("action", "unknown")
        logger.info(
            "GitHub webhook received",
            event_type=event_type,
            repository=request_body.get("repository", {}).get("name", "unknown")
        )

        # Process different GitHub events
        if event_type == "push":
            # TODO: Trigger test execution on push
            logger.info(
                "GitHub push event",
                ref=request_body.get("ref"),
                commits=len(request_body.get("commits", []))
            )
            return {"status": "received", "action": "scheduled_tests"}

        elif event_type == "pull_request":
            # TODO: Trigger tests for pull request
            logger.info(
                "GitHub pull request event",
                action=request_body.get("action"),
                pr_number=request_body.get("pull_request", {}).get("number")
            )
            return {"status": "received", "action": "scheduled_tests"}

        else:
            logger.debug(f"Unhandled GitHub event: {event_type}")
            return {"status": "received", "action": "ignored"}

    except Exception as e:
        logger.error(
            f"Error processing GitHub webhook: {str(e)}",
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )


@router.post("/jira")
async def jira_webhook(request_body: Dict[str, Any]):
    """Handle Jira webhook events."""
    try:
        # Log webhook event
        webhook_event = request_body.get("webhookEvent", "unknown")
        logger.info(
            "Jira webhook received",
            event_type=webhook_event,
            issue_key=request_body.get("issue", {}).get("key", "unknown")
        )

        # Process different Jira events
        if webhook_event == "jira:issue_created":
            # TODO: Create test case from Jira issue
            logger.info(
                "Jira issue created",
                issue_key=request_body.get("issue", {}).get("key"),
                summary=request_body.get("issue", {}).get("fields", {}).get("summary")
            )
            return {"status": "received", "action": "created_test_case"}

        elif webhook_event == "jira:issue_updated":
            # TODO: Update test case from Jira issue
            logger.info(
                "Jira issue updated",
                issue_key=request_body.get("issue", {}).get("key")
            )
            return {"status": "received", "action": "updated_test_case"}

        else:
            logger.debug(f"Unhandled Jira event: {webhook_event}")
            return {"status": "received", "action": "ignored"}

    except Exception as e:
        logger.error(
            f"Error processing Jira webhook: {str(e)}",
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )


@router.post("/slack")
async def slack_webhook(request_body: Dict[str, Any]):
    """Handle Slack webhook events and slash commands."""
    try:
        # Slack URL verification
        if request_body.get("type") == "url_verification":
            logger.info("Slack URL verification")
            return {"challenge": request_body.get("challenge")}

        # Log webhook event
        event_type = request_body.get("event", {}).get("type", "unknown")
        logger.info(
            "Slack webhook received",
            event_type=event_type,
            user=request_body.get("event", {}).get("user", "unknown")
        )

        # Process different Slack event types
        if event_type == "message":
            # TODO: Handle Slack messages (e.g., trigger tests)
            text = request_body.get("event", {}).get("text", "")
            logger.info(
                "Slack message received",
                text=text[:100],  # Log first 100 chars
                user=request_body.get("event", {}).get("user")
            )
            return {"status": "received", "action": "message_processed"}

        elif event_type == "app_mention":
            # TODO: Handle app mentions
            logger.info(
                "Slack app mention",
                user=request_body.get("event", {}).get("user")
            )
            return {"status": "received", "action": "mention_processed"}

        else:
            logger.debug(f"Unhandled Slack event: {event_type}")
            return {"status": "received", "action": "ignored"}

    except Exception as e:
        logger.error(
            f"Error processing Slack webhook: {str(e)}",
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )
