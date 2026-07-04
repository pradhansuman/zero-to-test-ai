"""API routes for test code review."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.dependencies import get_db, get_current_user
from app.services.test_reviewer import TestReviewer
from app.services.claude_client import ClaudeClient
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ai", tags=["test-review"])
logger = StructuredLogger(__name__)


class ReviewTestRequest(BaseModel):
    test_code: str = Field(..., description="Test code to review")
    framework: str = Field("pytest", description="Test framework")


class SuggestImprovementsRequest(BaseModel):
    test_code: str = Field(..., description="Test code")
    framework: str = Field("pytest", description="Test framework")


@router.post("/review-test")
async def review_test(
    request: ReviewTestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Review test code for quality and completeness."""
    try:
        claude_client = ClaudeClient()
        reviewer = TestReviewer(db, claude_client)

        result = await reviewer.review_test_code(
            test_code=request.test_code,
            framework=request.framework,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info(
            "test_reviewed",
            user_id=current_user["id"],
            framework=request.framework,
            score=result.get("overall_score"),
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("test_review_error", error=str(e))
        raise HTTPException(status_code=500, detail="Review failed")


@router.post("/suggest-test-improvements")
async def suggest_improvements(
    request: SuggestImprovementsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Suggest improvements for test code."""
    try:
        reviewer = TestReviewer(db)
        result = await reviewer.suggest_test_improvements(
            test_code=request.test_code,
            framework=request.framework,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info(
            "improvements_suggested",
            user_id=current_user["id"],
            improvement_count=result.get("improvement_count"),
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("suggestions_error", error=str(e))
        raise HTTPException(status_code=500, detail="Suggestion failed")
