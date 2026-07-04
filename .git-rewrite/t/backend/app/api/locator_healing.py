"""API routes for smart locator healing."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.locator_healer import LocatorHealer
from pydantic import BaseModel, Field
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ai/healing", tags=["locator-healing"])
logger = StructuredLogger(__name__)


class HealLocatorRequest(BaseModel):
    """Request to heal a broken locator."""

    broken_selector: str = Field(..., description="Current broken CSS/XPath selector")
    element_description: str = Field(..., description="Description of element to find")
    html_snippet: str = Field("", description="HTML context around the element")
    test_case_id: int = Field(None, description="Associated test case ID")


class ApplyHealingRequest(BaseModel):
    """Request to apply a healed locator."""

    test_case_id: int = Field(..., description="Test case to update")
    original_selector: str = Field(..., description="Original broken selector")
    new_selector: str = Field(..., description="New healed selector")


class HealingResponse(BaseModel):
    """Response with healed locator."""

    original_selector: str
    suggested_selector: str
    explanation: str
    confidence: float
    test_case_id: int = None
    timestamp: str


@router.post("/suggest", response_model=HealingResponse)
async def suggest_healing(
    request: HealLocatorRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Suggest a fix for a broken CSS/XPath locator.

    Args:
        request: Locator healing request
        db: Database session
        current_user: Authenticated user

    Returns:
        Suggested selector with confidence score
    """
    try:
        healer = LocatorHealer(db)
        result = await healer.heal_locator(
            broken_selector=request.broken_selector,
            element_description=request.element_description,
            html_snippet=request.html_snippet,
            test_case_id=request.test_case_id,
        )

        if "error" in result:
            logger.error("healing_suggestion_failed", error=result["error"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "healing_suggested",
            user_id=current_user["id"],
            element=request.element_description,
            confidence=result.get("confidence"),
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("healing_suggestion_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Locator healing failed",
        )


@router.post("/apply")
async def apply_healing(
    request: ApplyHealingRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Apply a healed locator to a test case.

    Args:
        request: Apply healing request
        db: Database session
        current_user: Authenticated user

    Returns:
        Success confirmation
    """
    try:
        healer = LocatorHealer(db)
        result = await healer.apply_healing(
            test_case_id=request.test_case_id,
            original_selector=request.original_selector,
            new_selector=request.new_selector,
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to apply healing"),
            )

        logger.info(
            "healing_applied",
            user_id=current_user["id"],
            test_case_id=request.test_case_id,
            new_selector=request.new_selector,
        )

        return {"success": True, "test_case_id": request.test_case_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("healing_application_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to apply healing",
        )


@router.get("/statistics")
async def get_healing_statistics(
    hours: int = 24,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get healing statistics for monitoring.

    Args:
        hours: Time period to analyze (default: 24h)
        db: Database session
        current_user: Authenticated user

    Returns:
        Statistics dict with success rates and confidence
    """
    try:
        healer = LocatorHealer(db)
        stats = await healer.get_healing_statistics(hours=hours)

        logger.info("healing_statistics_retrieved", user_id=current_user["id"])

        return {
            "period_hours": hours,
            "statistics": stats,
            "timestamp": str(__import__("datetime").datetime.utcnow().isoformat()),
        }
    except Exception as e:
        logger.error("healing_statistics_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve healing statistics",
        )
