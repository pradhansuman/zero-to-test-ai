"""API test executor - orchestrates REST and GraphQL test execution."""
import asyncio
import logging
from typing import List, Union

from shared.contracts.engine_schemas import (
    APITestCase, GraphQLTestCase, APIExecutionSummary, APITestResult, TestStatus
)
from .rest_client import RestClient
from .graphql_client import GraphQLClient

logger = logging.getLogger(__name__)


class APITestExecutor:
    """Orchestrates API test execution."""

    def __init__(
        self,
        base_url: str = None,
        timeout: int = 30,
        parallel: bool = False,
        max_workers: int = 4,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.parallel = parallel
        self.max_workers = max_workers

    async def execute(
        self,
        test_cases: List[Union[APITestCase, GraphQLTestCase]]
    ) -> APIExecutionSummary:
        """Execute API test suite."""
        logger.info(f"Starting API test execution: {len(test_cases)} tests")

        if self.parallel:
            results = await self._execute_parallel(test_cases)
        else:
            results = await self._execute_sequential(test_cases)

        return self._summarize(results)

    async def _execute_sequential(self, test_cases) -> List[APITestResult]:
        """Execute tests sequentially."""
        results = []
        async with RestClient(base_url=self.base_url, timeout=self.timeout) as client:
            for tc in test_cases:
                if isinstance(tc, APITestCase):
                    result = await client.execute(tc)
                else:
                    async with GraphQLClient(tc.endpoint) as gql:
                        result = await gql.execute(tc)
                results.append(result)
        return results

    async def _execute_parallel(self, test_cases) -> List[APITestResult]:
        """Execute tests in parallel."""
        semaphore = asyncio.Semaphore(self.max_workers)

        async def bounded_execute(tc):
            async with semaphore:
                if isinstance(tc, APITestCase):
                    async with RestClient(
                        base_url=self.base_url,
                        timeout=self.timeout
                    ) as client:
                        return await client.execute(tc)
                else:
                    async with GraphQLClient(tc.endpoint) as gql:
                        return await gql.execute(tc)

        return await asyncio.gather(*[bounded_execute(tc) for tc in test_cases])

    def _summarize(self, results: List[APITestResult]) -> APIExecutionSummary:
        """Summarize test results."""
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        total = len(results)

        avg_time = (
            sum(r.response_time_ms for r in results) / len(results)
            if results else 0
        )

        error_rate = (
            sum(1 for r in results if r.status == TestStatus.ERROR) / total * 100
            if total > 0 else 0
        )

        total_time = sum(r.response_time_ms for r in results) / 1000

        return APIExecutionSummary(
            total_tests=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            error_rate=error_rate,
            average_response_time_ms=avg_time,
            execution_time_seconds=total_time,
            results=results,
        )


async def run_api_tests(
    test_cases: List[Union[APITestCase, GraphQLTestCase]],
    base_url: str = None,
    **kwargs
) -> APIExecutionSummary:
    """Convenience function to run API tests."""
    executor = APITestExecutor(base_url=base_url, **kwargs)
    return await executor.execute(test_cases)
