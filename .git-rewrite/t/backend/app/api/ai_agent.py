"""AI Agent API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.services.ai_service import AIService
from app.models.ai_schema import (
    GenerateTestsRequest,
    GenerateTestsResponse,
    GeneratedTest,
    HealLocatorsRequest,
    HealLocatorsResponse,
    AnalyzeFailureRequest,
    AnalyzeFailureResponse
)
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/projects", tags=["ai-agent"])


@router.post("/{project_id}/ai/generate-tests", response_model=GenerateTestsResponse)
async def generate_tests(
    project_id: int,
    request: GenerateTestsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Generate test cases using AI."""
    try:
        service = AIService(db)
        generated = await service.generate_tests(
            project_id=project_id,
            description=request.description,
            count=request.count
        )
        logger.info(
            "Tests generated",
            project_id=project_id,
            user_id=current_user["id"],
            count=len(generated)
        )
        return {
            "project_id": project_id,
            "generated_tests": generated,
            "count": len(generated)
        }
    except Exception as e:
        logger.error(
            f"Error generating tests: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate tests"
        )


@router.post("/{project_id}/ai/heal-locators", response_model=HealLocatorsResponse)
async def heal_locators(
    project_id: int,
    request: HealLocatorsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Heal broken selectors using AI."""
    try:
        service = AIService(db)
        results = await service.heal_locators(
            project_id=project_id,
            execution_id=request.execution_id,
            screenshot=request.screenshot
        )
        logger.info(
            "Locators healed",
            project_id=project_id,
            execution_id=request.execution_id,
            user_id=current_user["id"],
            healed_count=results["healed_count"]
        )
        return results
    except Exception as e:
        logger.error(
            f"Error healing locators: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to heal locators"
        )


@router.post("/{project_id}/ai/analyze-failure", response_model=AnalyzeFailureResponse)
async def analyze_failure(
    project_id: int,
    request: AnalyzeFailureRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Analyze test failure using AI."""
    try:
        service = AIService(db)
        analysis = await service.analyze_failure(
            project_id=project_id,
            execution_id=request.execution_id,
            test_case_id=request.test_case_id
        )
        logger.info(
            "Failure analyzed",
            project_id=project_id,
            execution_id=request.execution_id,
            test_case_id=request.test_case_id,
            user_id=current_user["id"]
        )
        return analysis
    except Exception as e:
        logger.error(
            f"Error analyzing failure: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze failure"
        )
