"""Health check endpoints for monitoring and readiness probes."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/health", tags=["health"])
logger = StructuredLogger(__name__)


@router.get("")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "qa-automation-backend",
        "version": "1.0.0",
    }


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Readiness probe - checks if service is ready to serve traffic."""
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
            "timestamp": None,
        }
    except Exception as e:
        logger.error(
            "readiness_check_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        return {
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e),
        }, 503


@router.get("/live")
async def liveness_check(db: AsyncSession = Depends(get_db)):
    """Liveness probe - checks if service is running."""
    try:
        result = await db.execute(select(1))
        result.scalar()
        return {
            "status": "alive",
            "timestamp": None,
        }
    except Exception as e:
        logger.error(
            "liveness_check_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        return {
            "status": "dead",
            "error": str(e),
        }, 503


@router.get("/db")
async def database_health(db: AsyncSession = Depends(get_db)):
    """Detailed database health check."""
    try:
        await db.execute(text("SELECT 1"))
        result = await db.execute(text("SELECT version()"))
        version = result.scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "postgres_version": version,
        }
    except Exception as e:
        logger.error(
            "database_health_check_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }, 503
