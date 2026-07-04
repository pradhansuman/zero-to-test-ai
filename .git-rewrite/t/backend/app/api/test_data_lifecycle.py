"""Test data lifecycle API."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.dependencies import get_db, get_current_user
from app.services.test_data_manager import TestDataManager
from app.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/test-data", tags=["test-data"])
logger = StructuredLogger(__name__)

class TestDataRequest(BaseModel):
    test_id: int
    data_config: dict

@router.post("/setup")
async def setup_data(
    request: TestDataRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        manager = TestDataManager(db)
        result = await manager.setup_test_data(request.test_id, request.data_config)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        logger.info("data_setup", user_id=current_user["id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Setup failed")

@router.post("/cleanup/{transaction_id}")
async def cleanup_data(
    transaction_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        manager = TestDataManager(db)
        result = await manager.cleanup_test_data(transaction_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Cleanup failed")
