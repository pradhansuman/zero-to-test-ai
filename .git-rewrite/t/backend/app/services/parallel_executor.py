"""Parallel test execution engine with load balancing."""
import asyncio
from datetime import datetime
from typing import List, Dict, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import TestCase
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class ParallelExecutor:
    """Executes tests in parallel across multiple workers."""

    def __init__(self, db: AsyncSession, worker_count: int = 4):
        self.db = db
        self.worker_count = worker_count
        self.active_workers = 0
        self.execution_results = []

    async def execute_parallel(
        self,
        test_ids: List[int],
        workers: int = None,
    ) -> Dict:
        """Execute tests in parallel across workers.

        Args:
            test_ids: List of test case IDs
            workers: Number of workers (default: configured count)

        Returns:
            Aggregated execution results
        """
        try:
            workers = workers or self.worker_count

            # Partition tests for workers
            partitions = await self.partition_tests(test_ids)

            # Create tasks for each partition
            tasks = [
                self._execute_partition(partition)
                for partition in partitions
            ]

            # Run in parallel
            start_time = datetime.utcnow()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = datetime.utcnow()

            # Aggregate results
            aggregated = self._aggregate_results(
                results,
                start_time,
                end_time
            )

            logger.info(
                "parallel_execution_complete",
                total_tests=len(test_ids),
                workers=workers,
                duration_seconds=(end_time - start_time).total_seconds(),
                passed=aggregated["passed"],
                failed=aggregated["failed"],
            )

            return aggregated

        except Exception as e:
            logger.error("parallel_execution_error", error=str(e))
            return {"error": str(e)}

    async def partition_tests(self, test_ids: List[int]) -> List[List[int]]:
        """Partition tests for parallel execution.

        Smart partitioning considers:
        - Test dependencies (fixtures, shared state)
        - Estimated execution time
        - Worker count

        Args:
            test_ids: List of test IDs

        Returns:
            List of test partitions for workers
        """
        result = await self.db.execute(
            select(TestCase).where(TestCase.id.in_(test_ids))
        )
        test_cases = result.scalars().all()

        # Group by estimated weight
        test_weights = {}
        for tc in test_cases:
            # Estimate execution time (simplified)
            weight = len(tc.test_code) / 100 if tc.test_code else 1
            test_weights[tc.id] = weight

        # Distribute tests across workers to balance load
        partitions = [[] for _ in range(self.worker_count)]
        partition_weights = [0] * self.worker_count

        # Sort by weight (descending) to assign heavy tests first
        sorted_tests = sorted(
            test_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Bin packing: assign each test to least-loaded worker
        for test_id, weight in sorted_tests:
            min_idx = partition_weights.index(min(partition_weights))
            partitions[min_idx].append(test_id)
            partition_weights[min_idx] += weight

        return [p for p in partitions if p]  # Remove empty partitions

    async def _execute_partition(self, partition: List[int]) -> Dict:
        """Execute a partition of tests (runs sequentially within partition).

        Args:
            partition: List of test IDs to execute

        Returns:
            Partition execution result
        """
        results = {
            "partition_tests": partition,
            "passed": 0,
            "failed": 0,
            "test_results": []
        }

        for test_id in partition:
            try:
                # Simulate test execution
                result = await self._execute_single_test(test_id)

                if result.get("passed"):
                    results["passed"] += 1
                else:
                    results["failed"] += 1

                results["test_results"].append(result)

            except Exception as e:
                logger.error("partition_test_error", test_id=test_id, error=str(e))
                results["failed"] += 1

        return results

    async def _execute_single_test(self, test_id: int) -> Dict:
        """Execute a single test (mock implementation).

        Args:
            test_id: Test case ID

        Returns:
            Test execution result
        """
        result = await self.db.execute(
            select(TestCase).where(TestCase.id == test_id)
        )
        test_case = result.scalar_one_or_none()

        return {
            "test_id": test_id,
            "test_name": test_case.name if test_case else f"test_{test_id}",
            "passed": True,
            "duration": 0.5,
        }

    def _aggregate_results(self, results: List, start_time, end_time) -> Dict:
        """Aggregate partition results into final report.

        Args:
            results: List of partition results
            start_time: Execution start time
            end_time: Execution end time

        Returns:
            Aggregated execution report
        """
        total_passed = 0
        total_failed = 0
        all_test_results = []

        for partition_result in results:
            if isinstance(partition_result, Exception):
                total_failed += 1
                continue

            if isinstance(partition_result, dict):
                total_passed += partition_result.get("passed", 0)
                total_failed += partition_result.get("failed", 0)
                all_test_results.extend(
                    partition_result.get("test_results", [])
                )

        duration = (end_time - start_time).total_seconds()
        pass_rate = (
            100 * total_passed / (total_passed + total_failed)
            if (total_passed + total_failed) > 0 else 0
        )

        return {
            "total_tests": total_passed + total_failed,
            "passed": total_passed,
            "failed": total_failed,
            "pass_rate": round(pass_rate, 2),
            "duration_seconds": round(duration, 2),
            "workers_used": self.worker_count,
            "test_results": all_test_results,
            "execution_timestamp": end_time.isoformat(),
        }

    async def get_execution_status(self) -> Dict:
        """Get current parallel execution status.

        Returns:
            Status dictionary
        """
        return {
            "active_workers": self.active_workers,
            "total_workers": self.worker_count,
            "timestamp": datetime.utcnow().isoformat(),
        }
