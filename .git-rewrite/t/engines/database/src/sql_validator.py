"""SQL query validator and executor for database testing."""
import logging
import time
from typing import List, Dict, Any, Optional

import asyncpg

from shared.contracts.engine_schemas import SQLTestCase, SQLTestResult, TestStatus

logger = logging.getLogger(__name__)


class SQLValidator:
    """Executes and validates SQL queries."""

    def __init__(
        self,
        host: str,
        port: int = 5432,
        database: str = "postgres",
        username: str = "postgres",
        password: str = "",
        ssl: bool = False,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.ssl = ssl
        self.pool = None

    async def connect(self):
        """Create connection pool."""
        self.pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password,
            ssl=self.ssl,
            min_size=5,
            max_size=20,
        )

    async def disconnect(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()

    async def execute_test(self, test_case: SQLTestCase) -> SQLTestResult:
        """Execute a SQL test case."""
        if test_case.skip:
            return self._create_skipped_result(test_case)

        start_time = time.time()

        try:
            async with self.pool.acquire() as conn:
                # Setup
                if test_case.setup_sql:
                    await conn.execute(test_case.setup_sql)

                # Execute
                result = await conn.fetch(test_case.sql, *test_case.parameters.values())

                # Teardown
                if test_case.teardown_sql:
                    await conn.execute(test_case.teardown_sql)

            execution_time = (time.time() - start_time) * 1000

            # Evaluate assertions
            assertions_passed, assertions_failed = self._evaluate_assertions(
                test_case.assertions, result
            )

            status = (
                TestStatus.PASSED
                if assertions_failed == 0 and not test_case.setup_sql
                else TestStatus.FAILED
            )

            return SQLTestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                status=status,
                query=test_case.sql,
                rows_returned=len(result),
                rows_affected=len(result),
                execution_time_ms=execution_time,
                has_error=False,
                columns_returned=[k for k in result[0].keys()] if result else [],
                sample_data=[dict(r) for r in result[:5]],
                assertions_passed=assertions_passed,
                assertions_failed=assertions_failed,
                tags=test_case.tags,
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"SQL error: {e}", exc_info=True)

            return SQLTestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                status=TestStatus.ERROR,
                query=test_case.sql,
                rows_returned=0,
                rows_affected=0,
                execution_time_ms=execution_time,
                has_error=True,
                error_message=str(e),
                error_code=getattr(e, "code", None),
                assertions_passed=0,
                assertions_failed=len(test_case.assertions),
                stack_trace=str(e),
                tags=test_case.tags,
            )

    def _evaluate_assertions(self, assertions, result: List[Dict]) -> tuple[int, int]:
        """Evaluate assertions against result."""
        passed = 0
        failed = 0

        for assertion in assertions:
            try:
                if assertion.type.value == "equals":
                    passed += 1 if len(result) == assertion.expected else 0
                    failed += 0 if len(result) == assertion.expected else 1
                # Add more assertion types as needed
                else:
                    failed += 1
            except Exception:
                failed += 1

        return passed, failed

    @staticmethod
    def _create_skipped_result(test_case: SQLTestCase) -> SQLTestResult:
        """Create skipped result."""
        return SQLTestResult(
            test_id=test_case.id,
            test_name=test_case.name,
            status=TestStatus.SKIPPED,
            query=test_case.sql,
            rows_returned=0,
            rows_affected=0,
            execution_time_ms=0,
            has_error=False,
            assertions_passed=0,
            assertions_failed=0,
            tags=test_case.tags,
        )
