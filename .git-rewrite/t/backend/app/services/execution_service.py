"""Execution service with test orchestration logic."""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Execution, ExecutionStatus, ExecutionResult
from app.repositories.execution import ExecutionRepository
from app.repositories.project import ProjectRepository
from app.repositories.test_case import TestCaseRepository
from app.exceptions import ValidationError, ExecutionNotFound, ProjectNotFound, Unauthorized
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionService:
    """Service for test execution orchestration."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ExecutionRepository(session)
        self.project_repo = ProjectRepository(session)
        self.test_case_repo = TestCaseRepository(session)

    async def create_execution(
        self,
        project_id: int,
        user_id: int,
        test_case_ids: Optional[List[int]] = None
    ) -> Execution:
        """Create new execution."""
        # Verify project exists and user owns it
        project = await self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFound()
        if project.owner_id != user_id:
            raise Unauthorized("You do not own this project")

        # Get test cases
        test_cases = []
        if test_case_ids:
            if not any(test_case_ids):
                raise ValidationError("At least one test case ID is required")
            test_cases = await self.test_case_repo.get_bulk(test_case_ids)
            if len(test_cases) != len(test_case_ids):
                raise ValidationError("Some test cases not found")
        else:
            # If no specific test cases provided, get all active test cases for project
            test_cases = await self.test_case_repo.get_by_project(project_id)

        try:
            execution_data = {
                "project_id": project_id,
                "status": ExecutionStatus.PENDING,
                "total_tests": len(test_cases),
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "error_count": 0,
                "duration_seconds": 0.0
            }
            execution = await self.repo.create(execution_data)
            await self.session.commit()
            logger.info(
                "Execution created successfully",
                execution_id=execution.id,
                project_id=project_id,
                user_id=user_id,
                total_tests=len(test_cases)
            )
            return execution
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error creating execution: {str(e)}",
                project_id=project_id,
                user_id=user_id,
                error=str(e)
            )
            raise

    async def get_execution(self, execution_id: int, project_id: Optional[int] = None) -> Execution:
        """Get execution by ID."""
        execution = await self.repo.get(execution_id)
        if not execution:
            logger.warning(
                "Execution not found",
                execution_id=execution_id,
                project_id=project_id
            )
            raise ExecutionNotFound()

        if project_id and execution.project_id != project_id:
            raise ExecutionNotFound()

        return execution

    async def list_executions(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Execution]:
        """List executions for project."""
        try:
            executions = await self.repo.get_by_project(project_id, skip=skip, limit=limit)
            logger.info(
                "Listed executions",
                project_id=project_id,
                skip=skip,
                limit=limit,
                count=len(executions)
            )
            return executions
        except Exception as e:
            logger.error(
                f"Error listing executions: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def list_by_status(
        self,
        project_id: int,
        status: str
    ) -> List[Execution]:
        """List executions by status."""
        if status not in [s.value for s in ExecutionStatus]:
            raise ValidationError(f"Invalid status: {status}")

        try:
            executions = await self.repo.get_by_status(project_id, status)
            logger.info(
                "Listed executions by status",
                project_id=project_id,
                status=status,
                count=len(executions)
            )
            return executions
        except Exception as e:
            logger.error(
                f"Error listing executions by status: {str(e)}",
                project_id=project_id,
                status=status,
                error=str(e)
            )
            raise

    async def get_recent_executions(
        self,
        project_id: int,
        limit: int = 10
    ) -> List[Execution]:
        """Get recent executions."""
        if limit < 1 or limit > 100:
            raise ValidationError("Limit must be between 1 and 100")

        try:
            executions = await self.repo.get_recent(project_id, limit=limit)
            logger.info(
                "Retrieved recent executions",
                project_id=project_id,
                limit=limit,
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

    async def start_execution(self, execution_id: int, project_id: int) -> Execution:
        """Mark execution as running."""
        execution = await self.get_execution(execution_id, project_id)

        if execution.status != ExecutionStatus.PENDING:
            raise ValidationError(f"Cannot start execution with status {execution.status}")

        try:
            execution = await self.repo.update_status(execution_id, ExecutionStatus.RUNNING)
            await self.session.commit()
            logger.info(
                "Execution started",
                execution_id=execution_id,
                project_id=project_id
            )
            return execution
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error starting execution: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            raise

    async def complete_execution(
        self,
        execution_id: int,
        project_id: int,
        passed: int,
        failed: int,
        skipped: int,
        duration: float
    ) -> Execution:
        """Complete execution and update results."""
        execution = await self.get_execution(execution_id, project_id)

        # Validate results
        if passed < 0 or failed < 0 or skipped < 0:
            raise ValidationError("Test counts cannot be negative")

        total = passed + failed + skipped
        if total > execution.total_tests:
            raise ValidationError("Test count exceeds total tests")

        if duration < 0:
            raise ValidationError("Duration cannot be negative")

        try:
            execution = await self.repo.update_results(
                execution_id,
                passed=passed,
                failed=failed,
                skipped=skipped,
                duration=duration
            )
            # Set status based on results
            status = ExecutionStatus.PASSED if failed == 0 else ExecutionStatus.FAILED
            execution = await self.repo.update_status(execution_id, status)
            await self.session.commit()
            logger.info(
                "Execution completed",
                execution_id=execution_id,
                project_id=project_id,
                status=status,
                passed=passed,
                failed=failed,
                skipped=skipped,
                duration=duration
            )
            return execution
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error completing execution: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            raise

    async def fail_execution(self, execution_id: int, project_id: int, error_message: str) -> Execution:
        """Mark execution as failed with error."""
        execution = await self.get_execution(execution_id, project_id)

        try:
            execution = await self.repo.update_status(execution_id, ExecutionStatus.ERROR)
            await self.session.commit()
            logger.error(
                "Execution failed with error",
                execution_id=execution_id,
                project_id=project_id,
                error_message=error_message
            )
            return execution
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Error failing execution: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            raise

    async def get_execution_summary(self, execution_id: int) -> dict:
        """Get execution summary with statistics."""
        execution = await self.repo.get(execution_id)
        if not execution:
            raise ExecutionNotFound()

        try:
            total = execution.total_tests
            passed = execution.passed
            failed = execution.failed
            skipped = execution.skipped

            summary = {
                "execution_id": execution.id,
                "project_id": execution.project_id,
                "status": execution.status,
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "pass_rate": (passed / total * 100) if total > 0 else 0,
                "failure_rate": (failed / total * 100) if total > 0 else 0,
                "duration_seconds": execution.duration_seconds,
                "started_at": execution.started_at,
                "ended_at": execution.ended_at,
                "created_at": execution.created_at
            }
            logger.debug(
                "Generated execution summary",
                execution_id=execution_id
            )
            return summary
        except Exception as e:
            logger.error(
                f"Error generating execution summary: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            raise

    async def get_project_statistics(self, project_id: int) -> dict:
        """Get execution statistics for project."""
        try:
            all_executions = await self.repo.get_by_project(project_id, skip=0, limit=1000)
            if not all_executions:
                return {
                    "project_id": project_id,
                    "total_executions": 0,
                    "passed_executions": 0,
                    "failed_executions": 0,
                    "average_duration": 0,
                    "average_pass_rate": 0
                }

            passed_count = sum(1 for e in all_executions if e.status == ExecutionStatus.PASSED)
            failed_count = sum(1 for e in all_executions if e.status == ExecutionStatus.FAILED)
            avg_duration = sum(e.duration_seconds for e in all_executions) / len(all_executions)
            avg_pass_rate = sum(
                (e.passed / e.total_tests * 100) if e.total_tests > 0 else 0
                for e in all_executions
            ) / len(all_executions)

            stats = {
                "project_id": project_id,
                "total_executions": len(all_executions),
                "passed_executions": passed_count,
                "failed_executions": failed_count,
                "average_duration": avg_duration,
                "average_pass_rate": avg_pass_rate
            }
            logger.info(
                "Generated project statistics",
                project_id=project_id,
                total_executions=len(all_executions)
            )
            return stats
        except Exception as e:
            logger.error(
                f"Error generating project statistics: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise
