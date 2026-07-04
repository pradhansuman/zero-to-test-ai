"""Test data management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.services.test_data_service import TestDataService
from app.models.test_data_schema import TestDataCreate, TestDataResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/projects", tags=["test-data"])


@router.get("/{project_id}/test-data", response_model=list[TestDataResponse])
async def list_test_data(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List test data sets for project."""
    try:
        service = TestDataService(db)
        test_data = await service.list_test_data(project_id, skip=skip, limit=limit)
        logger.info(
            "Test data listed",
            project_id=project_id,
            user_id=current_user["id"],
            count=len(test_data)
        )
        return test_data
    except Exception as e:
        logger.error(
            f"Error listing test data: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list test data"
        )


@router.post("/{project_id}/test-data", response_model=TestDataResponse)
async def create_test_data(
    project_id: int,
    request: TestDataCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new test data set."""
    try:
        service = TestDataService(db)
        test_data = await service.create_test_data(
            project_id=project_id,
            user_id=current_user["id"],
            name=request.name,
            data=request.data,
            description=request.description
        )
        logger.info(
            "Test data created",
            project_id=project_id,
            user_id=current_user["id"],
            test_data_id=test_data.id
        )
        return test_data
    except Exception as e:
        logger.error(
            f"Error creating test data: {str(e)}",
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create test data"
        )


@router.get("/{project_id}/test-data/{test_data_id}", response_model=TestDataResponse)
async def get_test_data(
    project_id: int,
    test_data_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get test data by ID."""
    try:
        service = TestDataService(db)
        test_data = await service.get_test_data(test_data_id, project_id)
        logger.info(
            "Test data retrieved",
            project_id=project_id,
            test_data_id=test_data_id,
            user_id=current_user["id"]
        )
        return test_data
    except Exception as e:
        logger.error(
            f"Error getting test data: {str(e)}",
            test_data_id=test_data_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test data not found"
        )


@router.delete("/{project_id}/test-data/{test_data_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_data(
    project_id: int,
    test_data_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete test data."""
    try:
        service = TestDataService(db)
        await service.delete_test_data(test_data_id, project_id, current_user["id"])
        logger.info(
            "Test data deleted",
            project_id=project_id,
            test_data_id=test_data_id,
            user_id=current_user["id"]
        )
    except Exception as e:
        logger.error(
            f"Error deleting test data: {str(e)}",
            test_data_id=test_data_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete test data"
        )
