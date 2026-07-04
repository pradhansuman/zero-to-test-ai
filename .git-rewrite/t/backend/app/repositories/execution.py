"""Execution repository."""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database.models import Execution, ExecutionStatus
from app.repositories.base import BaseRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionRepository(BaseRepository[Execution]):
    """Repository for Execution model."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Execution)

    async def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100) -> List[Execution]:
        """Get executions for project with pagination."""
        try:
            result = await self.session.execute(
                select(Execution)
                .where(Execution.project_id == project_id)
                .order_by(Execution.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            executions = result.scalars().all()
            logger.info(
                "Retrieved executions by project",
                project_id=project_id,
                count=len(executions)
            )
            return executions
        except Exception as e:
            logger.error(
                f"Error retrieving executions by project: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def get_by_status(self, project_id: int, status: str) -> List[Execution]:
        """Get executions by status."""
        try:
            result = await self.session.execute(
                select(Execution)
                .where(and_(
                    Execution.project_id == project_id,
                    Execution.status == status
                ))
                .order_by(Execution.created_at.desc())
            )
            executions = result.scalars().all()
            logger.debug(
                "Retrieved executions by status",
                project_id=project_id,
                status=status,
                count=len(executions)
            )
            return executions
        except Exception as e:
            logger.error(
                f"Error retrieving executions by status: {str(e)}",
                project_id=project_id,
                status=status,
                error=str(e)
            )
            raise

    async def get_recent(self, project_id: int, limit: int = 10) -> List[Execution]:
        """Get recent executions."""
        try:
            result = await self.session.execute(
                select(Execution)
                .where(Execution.project_id == project_id)
                .order_by(Execution.created_at.desc())
                .limit(limit)
            )
            executions = result.scalars().all()
            logger.debug(
                "Retrieved recent executions",
                project_id=project_id,
                count=len(executions)
            )
            return executions
        except Exception as e:
            logger.error(
                f"Error retrieving recent executions: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def update_status(self, execution_id: int, status: str) -> Optional[Execution]:
        """Update execution status."""
        try:
            result = await self.session.execute(
                select(Execution).where(Execution.id == execution_id)
            )
            execution = result.scalar_one_or_none()
            if not execution:
                return None

            execution.status = status
            if status == ExecutionStatus.RUNNING:
                execution.started_at = datetime.utcnow()
            elif status in (ExecutionStatus.PASSED, ExecutionStatus.FAILED, ExecutionStatus.ERROR):
                execution.ended_at = datetime.utcnow()

            self.session.add(execution)
            await self.session.flush()
            logger.info(
                "Updated execution status",
                execution_id=execution_id,
                new_status=status
            )
            return execution
        except Exception as e:
            logger.error(
                f"Error updating execution status: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            await self.session.rollback()
            raise

    async def update_results(self, execution_id: int, passed: int, failed: int, skipped: int, duration: float) -> Optional[Execution]:
        """Update execution results."""
        try:
            result = await self.session.execute(
                select(Execution).where(Execution.id == execution_id)
            )
            execution = result.scalar_one_or_none()
            if not execution:
                return None

            execution.passed = passed
            execution.failed = failed
            execution.skipped = skipped
            execution.duration_seconds = duration
            execution.error_count = failed

            self.session.add(execution)
            await self.session.flush()
            logger.info(
                "Updated execution results",
                execution_id=execution_id,
                passed=passed,
                failed=failed,
                skipped=skipped,
                duration=duration
            )
            return execution
        except Exception as e:
            logger.error(
                f"Error updating execution results: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            await self.session.rollback()
            raise

    async def count_by_status(self, project_id: int, status: str) -> int:
        """Count executions by status."""
        try:
            executions = await self.get_by_status(project_id, status)
            count = len(executions)
            logger.debug(
                "Counted executions by status",
                project_id=project_id,
                status=status,
                count=count
            )
            return count
        except Exception as e:
            logger.error(
                f"Error counting executions by status: {str(e)}",
                error=str(e)
            )
            raise
