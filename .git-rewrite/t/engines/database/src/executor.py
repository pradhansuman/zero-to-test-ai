"""Database test executor."""
import asyncio
import logging
from typing import List

from shared.contracts.engine_schemas import (
    SQLTestCase, DatabaseExecutionSummary, SQLTestResult, TestStatus
)
from .sql_validator import SQLValidator

logger = logging.getLogger(__name__)


class DatabaseTestExecutor:
    """Orchestrates database test execution."""

    def __init__(
        self,
        host: str,
        port: int = 5432,
        database: str = "postgres",
        username: str = "postgres",
        password: str = "",
        ssl: bool = False,
        parallel: bool = False,
        max_workers: int = 4,
    ):
        self.validator = SQLValidator(
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
            ssl=ssl,
        )
        self.parallel = parallel
        self.max_workers = max_workers

    async def execute(self, test_cases: List[SQLTestCase]) -> DatabaseExecutionSummary:
        """Execute database test suite."""
        logger.info(f"Starting database test execution: {len(test_cases)} tests")

        await self.validator.connect()

        try:
            if self.parallel:
                results = await self._execute_parallel(test_cases)
            else:
                results = await self._execute_sequential(test_cases)

            return self._summarize(results)

        finally:
            await self.validator.disconnect()

    async def _execute_sequential(self, test_cases: List[SQLTestCase]) -> List[SQLTestResult]:
        """Execute tests sequentially."""
        results = []
        for tc in test_cases:
            result = await self.validator.execute_test(tc)
            results.append(result)
        return results

    async def _execute_parallel(self, test_cases: List[SQLTestCase]) -> List[SQLTestResult]:
        """Execute tests in parallel."""
        semaphore = asyncio.Semaphore(self.max_workers)

        async def bounded_execute(tc):
            async with semaphore:
                return await self.validator.execute_test(tc)

        return await asyncio.gather(*[bounded_execute(tc) for tc in test_cases])

    def _summarize(self, results: List[SQLTestResult]) -> DatabaseExecutionSummary:
        """Summarize test results."""
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        total = len(results)

        avg_time = (
            sum(r.execution_time_ms for r in results) / len(results)
            if results else 0
        )

        error_rate = (
            sum(1 for r in results if r.status == TestStatus.ERROR) / total * 100
            if total > 0 else 0
        )

        slow_queries = [
            r.query for r in results
            if r.execution_time_ms > r.execution_time_ms * 1.5
        ]

        total_time = sum(r.execution_time_ms for r in results) / 1000

        return DatabaseExecutionSummary(
            total_tests=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            error_rate=error_rate,
            average_execution_time_ms=avg_time,
            slow_queries=slow_queries,
            execution_time_seconds=total_time,
            results=results,
        )


async def run_database_tests(
    test_cases: List[SQLTestCase],
    host: str,
    **kwargs
) -> DatabaseExecutionSummary:
    """Convenience function to run database tests."""
    executor = DatabaseTestExecutor(host=host, **kwargs)
    return await executor.execute(test_cases)
