"""API routes for failure analysis engine."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from datetime import datetime

from app.dependencies import get_db, get_current_user
from app.services.failure_analyzer import FailureAnalyzer
from app.services.claude_client import ClaudeClient
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ai", tags=["failure-analysis"])
logger = StructuredLogger(__name__)


class AnalyzeFailureRequest(BaseModel):
    """Request to analyze a test failure."""

    error_message: str = Field(..., description="Error message from test failure")
    test_name: str = Field(..., description="Name of the test that failed")
    stack_trace: str = Field("", description="Full stack trace if available")
    test_case_id: int = Field(None, description="Associated test case ID")


class FailureAnalysisResponse(BaseModel):
    """Response with failure analysis."""

    test_name: str
    failure_type: str
    failure_type_description: str
    error_message: str
    root_cause: str
    suggested_fixes: list
    priority: str
    similar_failures_count: int
    test_case_id: int = None
    timestamp: str


class FailurePatternResponse(BaseModel):
    """Response with failure patterns."""

    project_id: int
    total_tests: int
    patterns: dict
    top_pattern: str = None
    analysis_timestamp: str


@router.post("/analyze-failure", response_model=FailureAnalysisResponse)
async def analyze_failure(
    request: AnalyzeFailureRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Analyze a test failure to identify root cause and suggest fixes.

    Args:
        request: Failure analysis request with error details
        db: Database session
        current_user: Authenticated user

    Returns:
        Analysis with failure classification and suggested fixes
    """
    try:
        claude_client = ClaudeClient()
        analyzer = FailureAnalyzer(db, claude_client)

        result = await analyzer.analyze_failure(
            error_msg=request.error_message,
            test_name=request.test_name,
            stack_trace=request.stack_trace,
            test_case_id=request.test_case_id,
        )

        if "error" in result:
            logger.error("failure_analysis_failed", error=result["error"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "failure_analyzed",
            user_id=current_user["id"],
            test_name=request.test_name,
            failure_type=result.get("failure_type"),
            priority=result.get("priority"),
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("failure_analysis_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failure analysis failed",
        )


@router.get("/failure-patterns/{project_id}", response_model=FailurePatternResponse)
async def get_failure_patterns(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get common failure patterns for a project.

    Args:
        project_id: Project ID to analyze
        db: Database session
        current_user: Authenticated user

    Returns:
        Dictionary with failure pattern frequencies
    """
    try:
        analyzer = FailureAnalyzer(db)
        patterns = await analyzer.get_failure_patterns(project_id)

        if "error" in patterns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=patterns["error"],
            )

        logger.info(
            "failure_patterns_retrieved",
            user_id=current_user["id"],
            project_id=project_id,
            top_pattern=patterns.get("top_pattern"),
        )

        return patterns

    except HTTPException:
        raise
    except Exception as e:
        logger.error("failure_patterns_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve failure patterns",
        )


@router.get("/failure-statistics")
async def get_failure_statistics(
    hours: int = 24,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get failure analysis statistics.

    Args:
        hours: Time period to analyze (default: 24h)
        db: Database session
        current_user: Authenticated user

    Returns:
        Statistics on analyzed failures
    """
    try:
        analyzer = FailureAnalyzer(db)
        stats = await analyzer.get_analysis_statistics(hours=hours)

        logger.info(
            "failure_statistics_retrieved",
            user_id=current_user["id"],
            period_hours=hours,
        )

        return {
            "period_hours": hours,
            "statistics": stats,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error("failure_statistics_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve failure statistics",
        )
