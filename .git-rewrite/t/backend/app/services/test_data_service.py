"""Test data service."""
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import TestData
from app.repositories.test_data import TestDataRepository
from app.repositories.project import ProjectRepository
from app.exceptions import ValidationError, ProjectNotFound
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TestDataService:
    """Service for test data management."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TestDataRepository(session)
        self.project_repo = ProjectRepository(session)

    async def create_test_data(
        self,
        project_id: int,
        user_id: int,
        name: str,
        data: Dict[str, Any],
        description: Optional[str] = None
    ) -> TestData:
        """Create new test data set."""
        # Verify project exists and user owns it
        project = await self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFound()
        if project.owner_id != user_id:
            raise ValidationError("You do not own this project")

        # Validate input
        if not name or not name.strip():
            raise ValidationError("Test data name is required")
        if len(name) > 255:
            raise ValidationError("Test data name must be less than 255 characters")

        if not data or not isinstance(data, dict):
            raise ValidationError("Test data must be a non-empty dictionary")

        try:
            test_data_obj = await self.repo.create({
                "project_id": project_id,
                "name": name.strip(),
                "description": description,
                "data": data,
                "is_active": True
            })
            await self.session.commit()
            logger.info(
                "Test data created successfully",
                test_data_id=test_data_obj.id,
                project_id=project_id,
                user_id=user_id,
                name=name
            )
            return test_data_obj
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error creating test data: {str(e)}",
                project_id=project_id,
                user_id=user_id,
                error=str(e)
            )
            raise

    async def get_test_data(self, test_data_id: int, project_id: int) -> TestData:
        """Get test data by ID."""
        test_data = await self.repo.get(test_data_id)
        if not test_data or test_data.project_id != project_id:
            raise ValidationError("Test data not found")
        return test_data

    async def list_test_data(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestData]:
        """List test data for project."""
        try:
            test_data = await self.repo.get_by_project(project_id, skip=skip, limit=limit)
            logger.info(
                "Listed test data",
                project_id=project_id,
                skip=skip,
                limit=limit,
                count=len(test_data)
            )
            return test_data
        except Exception as e:
            logger.error(
                f"Error listing test data: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def search_test_data(self, project_id: int, name: str) -> List[TestData]:
        """Search test data by name."""
        if not name or not name.strip():
            raise ValidationError("Search term is required")

        try:
            test_data = await self.repo.search_by_name(project_id, name)
            logger.info(
                "Searched test data",
                project_id=project_id,
                search_term=name,
                count=len(test_data)
            )
            return test_data
        except Exception as e:
            logger.error(
                f"Error searching test data: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def delete_test_data(
        self,
        test_data_id: int,
        project_id: int,
        user_id: int
    ) -> bool:
        """Soft delete test data."""
        # Verify project ownership
        project = await self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFound()
        if project.owner_id != user_id:
            raise ValidationError("You do not own this project")

        # Verify test data belongs to project
        test_data = await self.get_test_data(test_data_id, project_id)

        try:
            await self.repo.update(test_data_id, {"is_active": False})
            await self.session.commit()
            logger.info(
                "Test data deleted",
                test_data_id=test_data_id,
                project_id=project_id,
                user_id=user_id
            )
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error deleting test data: {str(e)}",
                test_data_id=test_data_id,
                error=str(e)
            )
            raise
