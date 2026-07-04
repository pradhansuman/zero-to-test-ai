"""Smart retry manager with exponential backoff and flaky test detection."""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import TestCase, Execution
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class RetryManager:
    """Manages test retries with intelligent strategies."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.retry_history = {}
        self.flaky_tests = set()

    async def execute_with_retry(
        self,
        test_case_id: int,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0,
    ) -> Dict:
        """Execute test with exponential backoff retry.

        Args:
            test_case_id: Test case ID to execute
            max_retries: Maximum number of retries (default: 3)
            backoff_factor: Exponential backoff multiplier (default: 2.0)
            initial_delay: Initial delay in seconds (default: 1.0)

        Returns:
            Dictionary with execution result and retry info
        """
        try:
            # Get test case
            result = await self.db.execute(
                select(TestCase).where(TestCase.id == test_case_id)
            )
            test_case = result.scalar_one_or_none()

            if not test_case:
                return {"error": f"Test case {test_case_id} not found"}

            delay = initial_delay
            last_error = None
            attempt = 0

            for attempt in range(max_retries + 1):
                try:
                    # Simulate test execution
                    execution_result = await self._execute_test(test_case_id)

                    if execution_result.get("passed"):
                        # Test passed
                        return {
                            "success": True,
                            "test_case_id": test_case_id,
                            "test_name": test_case.name,
                            "attempt": attempt + 1,
                            "result": execution_result,
                            "retries_used": attempt,
                            "timestamp": datetime.utcnow().isoformat(),
                        }

                    # Test failed, will retry
                    last_error = execution_result.get("error")

                except Exception as e:
                    last_error = str(e)

                # Don't wait after final attempt
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

            # All retries exhausted
            await self._record_flaky_test(test_case_id, attempt + 1)

            return {
                "success": False,
                "test_case_id": test_case_id,
                "test_name": test_case.name,
                "attempts": attempt + 1,
                "error": last_error,
                "flaky": True,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error("retry_execution_error", error=str(e))
            return {"error": str(e)}

    async def _execute_test(self, test_case_id: int) -> Dict:
        """Simulate test execution (in production, would call real executor).

        Args:
            test_case_id: Test case ID

        Returns:
            Execution result
        """
        # This would be replaced with actual test execution
        # For now, return a mock result
        return {
            "passed": True,
            "duration": 0.5,
            "output": "Test passed",
        }

    async def _record_flaky_test(self, test_case_id: int, attempts: int):
        """Record a test as flaky after failed retries.

        Args:
            test_case_id: Test case ID
            attempts: Number of attempts made
        """
        self.flaky_tests.add(test_case_id)
        logger.info(
            "flaky_test_recorded",
            test_case_id=test_case_id,
            attempts=attempts,
        )

    async def detect_flaky_tests(
        self,
        project_id: int,
        run_count: int = 5
    ) -> Dict:
        """Detect flaky tests by running them multiple times.

        Args:
            project_id: Project ID
            run_count: Number of times to run each test (default: 5)

        Returns:
            Dictionary with flaky test classifications
        """
        try:
            # Get all test cases for project
            result = await self.db.execute(
                select(TestCase).where(TestCase.project_id == project_id)
            )
            test_cases = result.scalars().all()

            flaky_tests = []
            stable_tests = []
            broken_tests = []

            for test in test_cases:
                # Run test multiple times
                passes = 0

                for _ in range(run_count):
                    exec_result = await self._execute_test(test.id)
                    if exec_result.get("passed"):
                        passes += 1

                pass_rate = (passes / run_count) * 100

                # Classify based on pass rate
                if pass_rate >= 80:
                    stable_tests.append(test.id)
                elif pass_rate >= 20:
                    flaky_tests.append({
                        "test_id": test.id,
                        "test_name": test.name,
                        "pass_rate": pass_rate,
                    })
                else:
                    broken_tests.append(test.id)

            return {
                "project_id": project_id,
                "run_count": run_count,
                "stable_tests": len(stable_tests),
                "flaky_tests": len(flaky_tests),
                "broken_tests": len(broken_tests),
                "flaky_list": flaky_tests,
                "analysis_timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error("flaky_detection_error", error=str(e))
            return {"error": str(e)}

    async def get_retry_statistics(self) -> Dict:
        """Get statistics on retry operations.

        Returns:
            Retry statistics
        """
        return {
            "total_flaky_tests": len(self.flaky_tests),
            "flaky_test_ids": list(self.flaky_tests),
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def configure_retry_policy(
        self,
        project_id: int,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0,
    ) -> Dict:
        """Configure retry policy for a project.

        Args:
            project_id: Project ID
            max_retries: Max retries per test
            backoff_factor: Exponential backoff multiplier
            initial_delay: Initial delay in seconds

        Returns:
            Configuration confirmation
        """
        config = {
            "project_id": project_id,
            "max_retries": max_retries,
            "backoff_factor": backoff_factor,
            "initial_delay": initial_delay,
            "max_delay": initial_delay * (backoff_factor ** (max_retries - 1)),
            "configured_at": datetime.utcnow().isoformat(),
        }

        logger.info(
            "retry_policy_configured",
            project_id=project_id,
            max_retries=max_retries,
        )

        return config

    def calculate_retry_delay(
        self,
        attempt: int,
        initial_delay: float,
        backoff_factor: float,
        max_delay: float = 60.0
    ) -> float:
        """Calculate delay for a given retry attempt.

        Args:
            attempt: Attempt number (0-based)
            initial_delay: Initial delay
            backoff_factor: Backoff multiplier
            max_delay: Maximum delay cap

        Returns:
            Delay in seconds
        """
        delay = initial_delay * (backoff_factor ** attempt)
        return min(delay, max_delay)
