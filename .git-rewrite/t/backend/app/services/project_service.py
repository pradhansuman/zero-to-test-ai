"""Project service with business logic."""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Project, TestFramework
from app.repositories.project import ProjectRepository
from app.exceptions import ValidationError, ProjectNotFound, Unauthorized
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProjectService:
    """Service for project management."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ProjectRepository(session)

    async def create_project(
        self,
        name: str,
        owner_id: int,
        description: Optional[str] = None,
        test_framework: str = "playwright"
    ) -> Project:
        """Create new project with validation."""
        # Validate input
        if not name or not name.strip():
            raise ValidationError("Project name is required")
        if len(name) > 255:
            raise ValidationError("Project name must be less than 255 characters")

        if test_framework not in [tf.value for tf in TestFramework]:
            raise ValidationError(f"Invalid test framework: {test_framework}")

        try:
            project_data = {
                "name": name.strip(),
                "description": description,
                "owner_id": owner_id,
                "test_framework": test_framework,
                "is_active": True
            }
            project = await self.repo.create(project_data)
            await self.session.commit()
            logger.info(
                "Project created successfully",
                project_id=project.id,
                owner_id=owner_id,
                name=name
            )
            return project
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error creating project: {str(e)}",
                owner_id=owner_id,
                error=str(e)
            )
            raise

    async def get_project(self, project_id: int, user_id: Optional[int] = None) -> Project:
        """Get project by ID with optional ownership check."""
        project = await self.repo.get(project_id)
        if not project:
            logger.warning(
                "Project not found",
                project_id=project_id,
                user_id=user_id
            )
            raise ProjectNotFound()

        # Check ownership if user_id provided
        if user_id and project.owner_id != user_id:
            logger.warning(
                "Unauthorized access to project",
                project_id=project_id,
                user_id=user_id,
                owner_id=project.owner_id
            )
            raise Unauthorized("You do not own this project")

        return project

    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """List all projects."""
        try:
            projects = await self.repo.get_active_projects(skip=skip, limit=limit)
            logger.info(
                "Listed projects",
                skip=skip,
                limit=limit,
                count=len(projects)
            )
            return projects
        except Exception as e:
            logger.error(
                f"Error listing projects: {str(e)}",
                error=str(e)
            )
            raise

    async def list_user_projects(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """List projects owned by user."""
        try:
            projects = await self.repo.get_by_owner(user_id, skip=skip, limit=limit)
            logger.info(
                "Listed user projects",
                user_id=user_id,
                skip=skip,
                limit=limit,
                count=len(projects)
            )
            return projects
        except Exception as e:
            logger.error(
                f"Error listing user projects: {str(e)}",
                user_id=user_id,
                error=str(e)
            )
            raise

    async def update_project(
        self,
        project_id: int,
        user_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        test_framework: Optional[str] = None
    ) -> Project:
        """Update project with validation."""
        # Verify ownership
        project = await self.get_project(project_id, user_id=user_id)

        # Validate updates
        if name is not None:
            if not name.strip():
                raise ValidationError("Project name cannot be empty")
            if len(name) > 255:
                raise ValidationError("Project name must be less than 255 characters")

        if test_framework is not None:
            if test_framework not in [tf.value for tf in TestFramework]:
                raise ValidationError(f"Invalid test framework: {test_framework}")

        try:
            update_data = {}
            if name is not None:
                update_data["name"] = name.strip()
            if description is not None:
                update_data["description"] = description
            if test_framework is not None:
                update_data["test_framework"] = test_framework

            project = await self.repo.update(project_id, update_data)
            await self.session.commit()
            logger.info(
                "Project updated successfully",
                project_id=project_id,
                user_id=user_id,
                fields_updated=list(update_data.keys())
            )
            return project
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error updating project: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def delete_project(self, project_id: int, user_id: int) -> bool:
        """Soft delete project (deactivate)."""
        # Verify ownership
        project = await self.get_project(project_id, user_id=user_id)

        try:
            # Soft delete: mark as inactive
            await self.repo.update(project_id, {"is_active": False})
            await self.session.commit()
            logger.info(
                "Project deleted (deactivated)",
                project_id=project_id,
                user_id=user_id
            )
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error deleting project: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def search_projects(self, name: str) -> List[Project]:
        """Search projects by name."""
        if not name or not name.strip():
            raise ValidationError("Search term is required")

        try:
            projects = await self.repo.search_by_name(name)
            logger.info(
                "Searched projects",
                search_term=name,
                count=len(projects)
            )
            return projects
        except Exception as e:
            logger.error(
                f"Error searching projects: {str(e)}",
                search_term=name,
                error=str(e)
            )
            raise
