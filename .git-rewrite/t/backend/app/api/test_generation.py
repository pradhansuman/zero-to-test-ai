"""API routes for AI-powered test generation."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.test_generation_service import TestGenerationService
from app.models.ai_schemas import (
    GenerateTestRequest,
    GenerateAPITestRequest,
    GenerateUITestRequest,
    HealLocatorRequest,
    AnalyzeFailureRequest,
    OptimizeTestRequest,
    BatchGenerateRequest,
    GeneratedTestResponse,
    TestImprovementResponse,
    LocatorHealResponse,
    FailureAnalysisResponse,
)
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/ai", tags=["ai-generation"])
logger = StructuredLogger(__name__)


@router.post("/generate-test", response_model=GeneratedTestResponse)
async def generate_test(
    request: GenerateTestRequest,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate a test case from user story using AI.

    Args:
        request: Test generation request with story description
        project_id: Project ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Generated test code and metadata
    """
    try:
        service = TestGenerationService(db)
        result = await service.generate_test_from_story(
            project_id=project_id,
            user_id=current_user["id"],
            story_description=request.story_description,
            acceptance_criteria=request.acceptance_criteria,
            framework=request.framework,
        )

        if "error" in result:
            logger.error("test_generation_failed", error=result["error"])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "test_generated_via_api",
            user_id=current_user["id"],
            project_id=project_id,
            framework=request.framework,
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("test_generation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Test generation failed",
        )


@router.post("/generate-api-test", response_model=GeneratedTestResponse)
async def generate_api_test(
    request: GenerateAPITestRequest,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate an API test case.

    Args:
        request: API test generation request
        project_id: Project ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Generated API test code
    """
    try:
        service = TestGenerationService(db)
        result = await service.generate_api_test(
            project_id=project_id,
            user_id=current_user["id"],
            endpoint=request.endpoint,
            method=request.method,
            expected_response=request.expected_response,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "api_test_generated_via_api",
            user_id=current_user["id"],
            endpoint=request.endpoint,
            method=request.method,
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("api_test_generation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API test generation failed",
        )


@router.post("/generate-ui-test", response_model=GeneratedTestResponse)
async def generate_ui_test(
    request: GenerateUITestRequest,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate a UI test case using Playwright.

    Args:
        request: UI test generation request
        project_id: Project ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Generated Playwright test code
    """
    try:
        service = TestGenerationService(db)
        result = await service.generate_ui_test(
            project_id=project_id,
            user_id=current_user["id"],
            user_flow=request.user_flow,
            page_url=request.page_url,
            elements_to_interact=request.elements_to_interact,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "ui_test_generated_via_api",
            user_id=current_user["id"],
            url=request.page_url,
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("ui_test_generation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UI test generation failed",
        )


@router.post("/heal-locator", response_model=LocatorHealResponse)
async def heal_locator(
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
        service = TestGenerationService(db)
        claude = service.claude

        result = await claude.suggest_locator_fix(
            broken_selector=request.broken_selector,
            element_description=request.element_description,
            html_snippet=request.html_snippet,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "locator_healed_via_api",
            user_id=current_user["id"],
            element=request.element_description,
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("locator_healing_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Locator healing failed",
        )


@router.post("/analyze-failure", response_model=FailureAnalysisResponse)
async def analyze_failure(
    request: AnalyzeFailureRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Analyze a test failure and suggest causes/fixes.

    Args:
        request: Failure analysis request
        db: Database session
        current_user: Authenticated user

    Returns:
        Failure analysis with suggested fixes
    """
    try:
        service = TestGenerationService(db)
        claude = service.claude

        result = await claude.analyze_test_failure(
            error_message=request.error_message,
            test_name=request.test_name,
            stack_trace=request.stack_trace,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "failure_analyzed_via_api",
            user_id=current_user["id"],
            test_name=request.test_name,
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


@router.post("/optimize-test", response_model=TestImprovementResponse)
async def optimize_test(
    request: OptimizeTestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Suggest improvements to test code.

    Args:
        request: Test code optimization request
        db: Database session
        current_user: Authenticated user

    Returns:
        Optimization suggestions
    """
    try:
        service = TestGenerationService(db)
        result = await service.suggest_test_improvements(
            test_code=request.test_code,
            framework=request.framework,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        logger.info(
            "test_optimized_via_api",
            user_id=current_user["id"],
            framework=request.framework,
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("test_optimization_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Test optimization failed",
        )


@router.post("/batch-generate")
async def batch_generate(
    request: BatchGenerateRequest,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate multiple test cases in batch.

    Args:
        request: Batch generation request with list of stories
        project_id: Project ID
        db: Database session
        current_user: Authenticated user

    Returns:
        List of generated tests with success/failure status
    """
    try:
        service = TestGenerationService(db)
        results = await service.batch_generate_tests(
            project_id=project_id,
            user_id=current_user["id"],
            stories=request.stories,
            framework=request.framework,
        )

        logger.info(
            "batch_generation_completed_via_api",
            user_id=current_user["id"],
            project_id=project_id,
            count=len(results),
        )

        return {
            "total": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "results": results,
        }
    except Exception as e:
        logger.error("batch_generation_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch generation failed",
        )
