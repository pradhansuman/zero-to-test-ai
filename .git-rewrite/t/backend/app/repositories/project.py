"""Project repository."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import Project
from app.repositories.base import BaseRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Project)

    async def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects owned by user."""
        try:
            result = await self.session.execute(
                select(Project)
                .where(Project.owner_id == owner_id)
                .where(Project.is_active == True)
                .offset(skip)
                .limit(limit)
            )
            projects = result.scalars().all()
            logger.info(
                "Retrieved projects by owner",
                owner_id=owner_id,
                count=len(projects)
            )
            return projects
        except Exception as e:
            logger.error(
                f"Error retrieving projects by owner: {str(e)}",
                owner_id=owner_id,
                error=str(e)
            )
            raise

    async def get_active_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all active projects."""
        try:
            result = await self.session.execute(
                select(Project)
                .where(Project.is_active == True)
                .offset(skip)
                .limit(limit)
            )
            projects = result.scalars().all()
            logger.debug(
                "Retrieved active projects",
                count=len(projects)
            )
            return projects
        except Exception as e:
            logger.error(
                f"Error retrieving active projects: {str(e)}",
                error=str(e)
            )
            raise

    async def search_by_name(self, name: str) -> List[Project]:
        """Search projects by name."""
        try:
            result = await self.session.execute(
                select(Project)
                .where(Project.name.ilike(f"%{name}%"))
                .where(Project.is_active == True)
            )
            projects = result.scalars().all()
            logger.debug(
                "Searched projects by name",
                search_term=name,
                count=len(projects)
            )
            return projects
        except Exception as e:
            logger.error(
                f"Error searching projects by name: {str(e)}",
                search_term=name,
                error=str(e)
            )
            raise
