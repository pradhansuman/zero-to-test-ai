"""Test data repository."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import TestData
from app.repositories.base import BaseRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TestDataRepository(BaseRepository[TestData]):
    """Repository for TestData model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, TestData)

    async def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[TestData]:
        """Get test data by project."""
        try:
            result = await self.session.execute(
                select(TestData)
                .where(TestData.project_id == project_id)
                .where(TestData.is_active == True)
                .offset(skip)
                .limit(limit)
            )
            test_data = result.scalars().all()
            logger.debug(
                "Retrieved test data by project",
                project_id=project_id,
                count=len(test_data)
            )
            return test_data
        except Exception as e:
            logger.error(
                f"Error retrieving test data by project: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def search_by_name(self, project_id: int, name: str) -> List[TestData]:
        """Search test data by name."""
        try:
            result = await self.session.execute(
                select(TestData)
                .where(TestData.project_id == project_id)
                .where(TestData.name.ilike(f"%{name}%"))
                .where(TestData.is_active == True)
            )
            test_data = result.scalars().all()
            logger.debug(
                "Searched test data by name",
                project_id=project_id,
                search_term=name,
                count=len(test_data)
            )
            return test_data
        except Exception as e:
            logger.error(
                f"Error searching test data by name: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise
