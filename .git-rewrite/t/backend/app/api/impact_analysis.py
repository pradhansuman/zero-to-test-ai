"""API routes for test impact analysis."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List

from app.dependencies import get_db, get_current_user
from app.services.impact_analyzer import ImpactAnalyzer
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ai", tags=["impact-analysis"])
logger = StructuredLogger(__name__)


class CodeChangeRequest(BaseModel):
    """Request to analyze code changes."""

    project_id: int = Field(..., description="Project ID")
    files_changed: List[str] = Field(..., description="List of changed file paths")
    branch: str = Field("main", description="Git branch being analyzed")


class TestSelectionRequest(BaseModel):
    """Request to select tests for CI."""

    project_id: int = Field(..., description="Project ID")
    pr_files: List[str] = Field(..., description="Changed files in PR")
    strategy: str = Field("affected", description="Test selection strategy")


class ImpactAnalysisResponse(BaseModel):
    """Response with impact analysis."""

    project_id: int
    branch: str
    total_tests: int
    affected_tests: int
    unaffected_tests: int
    affected_test_ids: List[int]
    savings_percent: float
    files_changed: List[str]
    analysis_timestamp: str


class TestSelectionResponse(BaseModel):
    """Response with test selection."""

    project_id: int
    strategy: str
    selected_test_count: int
    selected_test_ids: List[int]
    total_tests: int
    estimated_duration_seconds: int
    time_saved_seconds: int
    ci_efficiency: float


@router.post("/impact-analysis", response_model=ImpactAnalysisResponse)
async def analyze_impact(
    request: CodeChangeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Analyze which tests are impacted by code changes.

    Args:
        request: Code change details
        db: Database session
        current_user: Authenticated user

    Returns:
        Impact analysis with affected test IDs
    """
    try:
        analyzer = ImpactAnalyzer(db)
        result = await analyzer.analyze_code_changes(
            project_id=request.project_id,
            files_changed=request.files_changed,
            branch=request.branch,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "impact_analysis_endpoint",
            user_id=current_user["id"],
            project_id=request.project_id,
            files_changed=len(request.files_changed),
            affected_tests=result["affected_tests"],
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("impact_analysis_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Impact analysis failed",
        )


@router.post("/select-tests", response_model=TestSelectionResponse)
async def select_tests(
    request: TestSelectionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Select optimal test subset for CI execution.

    Args:
        request: Test selection request
        db: Database session
        current_user: Authenticated user

    Returns:
        Selected test IDs and execution estimate
    """
    try:
        analyzer = ImpactAnalyzer(db)
        result = await analyzer.select_tests_for_ci(
            project_id=request.project_id,
            pr_files=request.pr_files,
            strategy=request.strategy,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "tests_selected_endpoint",
            user_id=current_user["id"],
            project_id=request.project_id,
            strategy=request.strategy,
            selected_count=result["selected_test_count"],
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("test_selection_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Test selection failed",
        )


@router.get("/test-dependencies/{project_id}/{test_id}")
async def get_dependencies(
    project_id: int,
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get dependencies for a specific test.

    Args:
        project_id: Project ID
        test_id: Test case ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Test dependencies (imports, fixtures)
    """
    try:
        analyzer = ImpactAnalyzer(db)
        result = await analyzer.get_test_dependencies(project_id, test_id)

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "dependencies_retrieved",
            user_id=current_user["id"],
            test_id=test_id,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("dependency_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dependencies",
        )


@router.get("/impact-statistics/{project_id}")
async def get_statistics(
    project_id: int,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get impact analysis statistics for a project.

    Args:
        project_id: Project ID
        days: Period to analyze (default: 7 days)
        db: Database session
        current_user: Authenticated user

    Returns:
        Impact statistics
    """
    try:
        analyzer = ImpactAnalyzer(db)
        stats = await analyzer.get_impact_statistics(project_id, days)

        if "error" in stats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=stats["error"],
            )

        logger.info(
            "impact_statistics_retrieved",
            user_id=current_user["id"],
            project_id=project_id,
        )

        return stats

    except HTTPException:
        raise
    except Exception as e:
        logger.error("statistics_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve statistics",
        )
