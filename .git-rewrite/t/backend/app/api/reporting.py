"""Advanced reporting API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.report_generator import ReportGenerator
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/reports", tags=["reporting"])
logger = StructuredLogger(__name__)

@router.get("/generate/{project_id}")
async def generate_report(
    project_id: int,
    report_type: str = "html",
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Generate test report in specified format (html/pdf/csv)."""
    try:
        generator = ReportGenerator(db)
        report = await generator.generate_report(project_id, report_type)
        if "error" in report:
            raise HTTPException(status_code=400, detail=report["error"])
        logger.info("report_generated", project_id=project_id, format=report_type)
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.error("report_generation_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Report generation failed")
