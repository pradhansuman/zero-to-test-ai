"""Test case service with business logic."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import TestCase
from app.repositories.test_case import TestCaseRepository
from app.repositories.project import ProjectRepository
from app.exceptions import ValidationError, TestCaseNotFound, ProjectNotFound, Unauthorized
from app.utils.logger import get_logger
from app.constants import VALID_TEST_TYPES

logger = get_logger(__name__)


class TestCaseService:
    """Service for test case management."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TestCaseRepository(session)
        self.project_repo = ProjectRepository(session)

    async def create_test_case(
        self,
        project_id: int,
        user_id: int,
        name: str,
        test_code: str,
        description: Optional[str] = None,
        test_type: str = "e2e",
        tags: Optional[List[str]] = None
    ) -> TestCase:
        """Create new test case with validation."""
        # Verify project exists and user owns it
        project = await self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFound()
        if project.owner_id != user_id:
            raise Unauthorized("You do not own this project")

        # Validate input
        if not name or not name.strip():
            raise ValidationError("Test case name is required")
        if len(name) > 255:
            raise ValidationError("Test case name must be less than 255 characters")

        if not test_code or not test_code.strip():
            raise ValidationError("Test code is required")

        if test_type not in VALID_TEST_TYPES:
            raise ValidationError(f"Invalid test type: {test_type}")

        try:
            test_case_data = {
                "project_id": project_id,
                "name": name.strip(),
                "description": description,
                "test_code": test_code,
                "test_type": test_type,
                "tags": tags or [],
                "is_active": True
            }
            test_case = await self.repo.create(test_case_data)
            await self.session.commit()
            logger.info(
                "Test case created successfully",
                test_case_id=test_case.id,
                project_id=project_id,
                user_id=user_id,
                test_type=test_type
            )
            return test_case
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error creating test case: {str(e)}",
                project_id=project_id,
                user_id=user_id,
                error=str(e)
            )
            raise

    async def get_test_case(self, test_case_id: int, project_id: Optional[int] = None) -> TestCase:
        """Get test case by ID."""
        test_case = await self.repo.get(test_case_id)
        if not test_case:
            logger.warning(
                "Test case not found",
                test_case_id=test_case_id,
                project_id=project_id
            )
            raise TestCaseNotFound()

        if project_id and test_case.project_id != project_id:
            raise TestCaseNotFound()

        return test_case

    async def list_test_cases(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestCase]:
        """List test cases for project."""
        try:
            test_cases = await self.repo.get_by_project(project_id, skip=skip, limit=limit)
            logger.info(
                "Listed test cases",
                project_id=project_id,
                skip=skip,
                limit=limit,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error listing test cases: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def list_by_type(
        self,
        project_id: int,
        test_type: str
    ) -> List[TestCase]:
        """List test cases by type."""
        if test_type not in VALID_TEST_TYPES:
            raise ValidationError(f"Invalid test type: {test_type}")

        try:
            test_cases = await self.repo.get_by_type(project_id, test_type)
            logger.info(
                "Listed test cases by type",
                project_id=project_id,
                test_type=test_type,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error listing test cases by type: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def list_by_tags(
        self,
        project_id: int,
        tags: List[str]
    ) -> List[TestCase]:
        """List test cases by tags."""
        if not tags or not any(tags):
            raise ValidationError("At least one tag is required")

        try:
            test_cases = await self.repo.get_by_tags(project_id, tags)
            logger.info(
                "Listed test cases by tags",
                project_id=project_id,
                tags=tags,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error listing test cases by tags: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def search_test_cases(
        self,
        project_id: int,
        name: str
    ) -> List[TestCase]:
        """Search test cases by name."""
        if not name or not name.strip():
            raise ValidationError("Search term is required")

        try:
            test_cases = await self.repo.search_by_name(project_id, name)
            logger.info(
                "Searched test cases",
                project_id=project_id,
                search_term=name,
                count=len(test_cases)
            )
            return test_cases
        except Exception as e:
            logger.error(
                f"Error searching test cases: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def update_test_case(
        self,
        test_case_id: int,
        project_id: int,
        user_id: int,
        name: Optional[str] = None,
        test_code: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> TestCase:
        """Update test case with validation."""
        # Verify project ownership
        project = await self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFound()
        if project.owner_id != user_id:
            raise Unauthorized("You do not own this project")

        # Verify test case belongs to project
        test_case = await self.get_test_case(test_case_id, project_id)

        # Validate updates
        if name is not None:
            if not name.strip():
                raise ValidationError("Test case name cannot be empty")
            if len(name) > 255:
                raise ValidationError("Test case name must be less than 255 characters")

        if test_code is not None:
            if not test_code.strip():
                raise ValidationError("Test code cannot be empty")

        try:
            update_data = {}
            if name is not None:
                update_data["name"] = name.strip()
            if test_code is not None:
                update_data["test_code"] = test_code
            if description is not None:
                update_data["description"] = description
            if tags is not None:
                update_data["tags"] = tags

            test_case = await self.repo.update(test_case_id, update_data)
            await self.session.commit()
            logger.info(
                "Test case updated successfully",
                test_case_id=test_case_id,
                project_id=project_id,
                user_id=user_id,
                fields_updated=list(update_data.keys())
            )
            return test_case
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error updating test case: {str(e)}",
                test_case_id=test_case_id,
                error=str(e)
            )
            raise

    async def delete_test_case(self, test_case_id: int, project_id: int, user_id: int) -> bool:
        """Soft delete test case (deactivate)."""
        # Verify project ownership
        project = await self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFound()
        if project.owner_id != user_id:
            raise Unauthorized("You do not own this project")

        # Verify test case belongs to project
        test_case = await self.get_test_case(test_case_id, project_id)

        try:
            # Soft delete: mark as inactive
            await self.repo.update(test_case_id, {"is_active": False})
            await self.session.commit()
            logger.info(
                "Test case deleted (deactivated)",
                test_case_id=test_case_id,
                project_id=project_id,
                user_id=user_id
            )
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error deleting test case: {str(e)}",
                test_case_id=test_case_id,
                error=str(e)
            )
            raise

    async def get_bulk(self, test_case_ids: List[int], project_id: int) -> List[TestCase]:
        """Get multiple test cases by IDs."""
        if not test_case_ids:
            raise ValidationError("At least one test case ID is required")

        try:
            test_cases = await self.repo.get_bulk(test_case_ids)
            # Verify all belong to same project
            if not all(tc.project_id == project_id for tc in test_cases):
                raise ValidationError("Not all test cases belong to the specified project")

            logger.info(
                "Retrieved bulk test cases",
                project_id=project_id,
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
