"""Code coverage analysis API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.coverage_analyzer import CoverageAnalyzer
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/coverage", tags=["coverage"])
logger = StructuredLogger(__name__)

@router.get("/analyze/{project_id}")
async def analyze_coverage(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Analyze code coverage for project."""
    try:
        analyzer = CoverageAnalyzer(db)
        result = await analyzer.analyze_coverage(project_id)
        logger.info("coverage_analyzed", project_id=project_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Analysis failed")

@router.get("/report/{project_id}")
async def get_coverage_report(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get detailed coverage report."""
    try:
        analyzer = CoverageAnalyzer(db)
        report = await analyzer.get_coverage_report(project_id)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve report")
