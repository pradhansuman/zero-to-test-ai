"""AI agent service for test generation and healing."""
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import TestCase, Execution
from app.repositories.test_case import TestCaseRepository
from app.repositories.project import ProjectRepository
from app.exceptions import ProjectNotFound, ExecutionNotFound
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AIService:
    """Service for AI-powered test generation and healing."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.test_repo = TestCaseRepository(session)
        self.project_repo = ProjectRepository(session)

    async def generate_tests(
        self,
        project_id: int,
        description: str,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate test cases using AI (stub - will integrate Phase 1 later)."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # TODO: Integrate with Phase 1 test generation engine
            # For now, return mock generated tests
            generated_tests = []
            for i in range(min(count, 5)):
                generated_tests.append({
                    "name": f"Generated Test {i+1} - {description[:30]}",
                    "description": f"AI-generated test case #{i+1}",
                    "test_code": f"# Generated test case\n# Description: {description}",
                    "test_type": "e2e",
                    "tags": ["ai-generated", "auto"],
                    "confidence": 0.85 - (i * 0.05)  # Decreasing confidence
                })

            logger.info(
                "Generated tests (stub)",
                project_id=project_id,
                count=len(generated_tests),
                description=description[:50]
            )
            return generated_tests
        except ProjectNotFound:
            raise
        except Exception as e:
            logger.error(
                f"Error generating tests: {str(e)}",
                project_id=project_id,
                error=str(e)
            )
            raise

    async def heal_locators(
        self,
        project_id: int,
        execution_id: int,
        screenshot: Optional[str] = None
    ) -> Dict[str, Any]:
        """Heal broken locators using AI (stub - will integrate Phase 1 later)."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # Verify execution exists
            result = await self.session.execute(
                f"SELECT * FROM executions WHERE id = {execution_id} AND project_id = {project_id}"
            )
            execution = result.scalar_one_or_none()
            if not execution:
                raise ExecutionNotFound()

            # TODO: Integrate with Phase 1 locator healing engine
            # For now, return mock healing results
            healing_results = {
                "execution_id": execution_id,
                "healed_count": 3,
                "healing_attempts": [
                    {
                        "test_case_id": 101,
                        "old_selector": "button.submit",
                        "new_selector": "button[type='submit']",
                        "confidence": 0.92,
                        "success": True,
                        "reason": "Button selector pattern changed"
                    },
                    {
                        "test_case_id": 102,
                        "old_selector": "#loginForm input",
                        "new_selector": "form#auth input[type='email']",
                        "confidence": 0.88,
                        "success": True,
                        "reason": "Form restructure detected"
                    },
                    {
                        "test_case_id": 103,
                        "old_selector": ".nav-item:nth-child(2)",
                        "new_selector": "[data-testid='nav-products']",
                        "confidence": 0.95,
                        "success": True,
                        "reason": "Navigation item uses data-testid"
                    }
                ]
            }

            logger.info(
                "Healed locators (stub)",
                execution_id=execution_id,
                project_id=project_id,
                healed_count=healing_results["healed_count"]
            )
            return healing_results
        except (ProjectNotFound, ExecutionNotFound):
            raise
        except Exception as e:
            logger.error(
                f"Error healing locators: {str(e)}",
                execution_id=execution_id,
                error=str(e)
            )
            raise

    async def analyze_failure(
        self,
        project_id: int,
        execution_id: int,
        test_case_id: int
    ) -> Dict[str, Any]:
        """Analyze test failure using AI (stub - will integrate Phase 1 later)."""
        try:
            # Verify project exists
            project = await self.project_repo.get(project_id)
            if not project:
                raise ProjectNotFound()

            # Verify test case exists
            test_case = await self.test_repo.get(test_case_id)
            if not test_case or test_case.project_id != project_id:
                raise Exception("Test case not found")

            # TODO: Integrate with Phase 1 failure analysis engine
            # For now, return mock analysis
            analysis = {
                "execution_id": execution_id,
                "test_case_id": test_case_id,
                "failure_type": "assertion_failure",
                "root_cause": "Expected element not found after timeout",
                "suggestions": [
                    "Increase timeout for element lookup",
                    "Check if DOM has changed (use data-testid attributes)",
                    "Verify network requests completed before assertion"
                ],
                "confidence": 0.78,
                "related_failures": [
                    {
                        "test_case_id": 101,
                        "test_case_name": "Similar login test",
                        "failure_type": "assertion_failure",
                        "similarity_score": 0.85
                    }
                ]
            }

            logger.info(
                "Analyzed failure (stub)",
                execution_id=execution_id,
                test_case_id=test_case_id,
                project_id=project_id,
                failure_type=analysis["failure_type"]
            )
            return analysis
        except (ProjectNotFound, Exception) as e:
            logger.error(
                f"Error analyzing failure: {str(e)}",
                execution_id=execution_id,
                test_case_id=test_case_id,
                error=str(e)
            )
            raise
