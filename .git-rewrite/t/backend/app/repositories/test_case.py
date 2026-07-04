"""Test case repository."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database.models import TestCase
from app.repositories.base import BaseRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TestCaseRepository(BaseRepository[TestCase]):
    """Repository for TestCase model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, TestCase)

    async def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[TestCase]:
        """Get all test cases for project."""
        try:
            result = await self.session.execute(
                select(TestCase)
                .where(TestCase.project_id == project_id)
                .where(TestCase.is_active == True)
                .offset(skip)
                .limit(limit)
            )
            test_cases = result.scalars().all()
            logger.info(
                "Retrieved test cases by project",
                project_id=project_id,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error retrieving test cases by project: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def get_by_type(self, project_id: int, test_type: str) -> List[TestCase]:
        """Get test cases by type."""
        try:
            result = await self.session.execute(
                select(TestCase)
                .where(and_(
                    TestCase.project_id == project_id,
                    TestCase.test_type == test_type,
                    TestCase.is_active == True
                ))
            )
            test_cases = result.scalars().all()
            logger.debug(
                "Retrieved test cases by type",
                project_id=project_id,
                test_type=test_type,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error retrieving test cases by type: {str(e)}",
                project_id=project_id,
                test_type=test_type,
                error=str(e)
            )
            raise

    async def get_by_tags(self, project_id: int, tags: List[str]) -> List[TestCase]:
        """Get test cases by tags."""
        try:
            result = await self.session.execute(
                select(TestCase)
                .where(TestCase.project_id == project_id)
                .where(TestCase.is_active == True)
            )
            test_cases = result.scalars().all()
            # Filter by tags (stored as JSON list)
            filtered = [
                tc for tc in test_cases
                if tc.tags and any(tag in tc.tags for tag in tags)
            ]
            logger.debug(
                "Retrieved test cases by tags",
                project_id=project_id,
                tags=tags,
                count=len(filtered)
            )
            return filtered
        except Exception as e:
            logger.error(
                f"Error retrieving test cases by tags: {str(e)}",
                project_id=project_id,
                tags=tags,
                error=str(e)
            )
            raise

    async def search_by_name(self, project_id: int, name: str) -> List[TestCase]:
        """Search test cases by name."""
        try:
            result = await self.session.execute(
                select(TestCase)
                .where(and_(
                    TestCase.project_id == project_id,
                    TestCase.name.ilike(f"%{name}%"),
                    TestCase.is_active == True
                ))
            )
            test_cases = result.scalars().all()
            logger.debug(
                "Searched test cases by name",
                project_id=project_id,
                search_term=name,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error searching test cases by name: {str(e)}",
                project_id=project_id,
                search_term=name,
                error=str(e)
            )
            raise

    async def get_bulk(self, test_case_ids: List[int]) -> List[TestCase]:
        """Get multiple test cases by IDs."""
        try:
            result = await self.session.execute(
                select(TestCase)
                .where(TestCase.id.in_(test_case_ids))
                .where(TestCase.is_active == True)
            )
            test_cases = result.scalars().all()
            logger.debug(
                "Retrieved bulk test cases",
                count=len(test_cases),
                requested=len(test_case_ids)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error retrieving bulk test cases: {str(e)}",
                error=str(e)
            )
            raise
