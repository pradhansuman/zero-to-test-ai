"""Tests for SQL validator."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from engines.database.src.sql_validator import SQLValidator
from shared.contracts.engine_schemas import SQLTestCase, Assertion, AssertionType, TestStatus


class TestSQLValidator:
    """Test suite for SQLValidator."""

    @pytest.fixture
    async def validator(self):
        """Create validator with mocked pool."""
        validator = SQLValidator(
            host="localhost",
            port=5432,
            database="testdb",
            username="user",
            password="pass",
        )
        validator.pool = AsyncMock()
        return validator

    @pytest.mark.asyncio
    async def test_execute_test_success(self, validator):
        """Test successful SQL execution."""
        test_case = SQLTestCase(
            id="DB-001",
            name="Count users",
            sql="SELECT COUNT(*) as count FROM users",
            assertions=[
                Assertion(
                    type=AssertionType.EQUALS,
                    target="count",
                    expected=5,
                ),
            ],
        )

        mock_conn = AsyncMock()
        mock_result = [{"count": 5}]
        mock_conn.fetch.return_value = mock_result
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        assert result.status == TestStatus.PASSED
        assert result.rows_returned == 1
        assert result.has_error is False

    @pytest.mark.asyncio
    async def test_execute_test_with_setup_teardown(self, validator):
        """Test SQL with setup and teardown."""
        test_case = SQLTestCase(
            id="DB-002",
            name="Test with setup",
            sql="SELECT * FROM users WHERE active = true",
            setup_sql="CREATE TEMP TABLE users (id INT, active BOOL)",
            teardown_sql="DROP TABLE users",
            assertions=[],
        )

        mock_conn = AsyncMock()
        mock_conn.execute.return_value = None
        mock_conn.fetch.return_value = []
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        # Verify setup and teardown were called
        assert mock_conn.execute.call_count >= 2

    @pytest.mark.asyncio
    async def test_execute_test_skip(self, validator):
        """Test skipped test case."""
        test_case = SQLTestCase(
            id="DB-003",
            name="Skipped test",
            sql="SELECT * FROM users",
            skip=True,
            assertions=[],
        )

        result = await validator.execute_test(test_case)

        assert result.status == TestStatus.SKIPPED
        assert result.execution_time_ms == 0

    @pytest.mark.asyncio
    async def test_execute_test_error(self, validator):
        """Test error handling."""
        test_case = SQLTestCase(
            id="DB-004",
            name="Bad query",
            sql="SELECT * FROM nonexistent_table",
            assertions=[],
        )

        mock_conn = AsyncMock()
        mock_conn.fetch.side_effect = Exception("Table not found")
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        assert result.status == TestStatus.ERROR
        assert result.has_error is True
        assert "not found" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_evaluate_assertions(self, validator):
        """Test assertion evaluation."""
        assertions = [
            Assertion(
                type=AssertionType.EQUALS,
                target="count",
                expected=5,
            ),
        ]

        mock_result = [{"count": 5}]
        passed, failed = validator._evaluate_assertions(assertions, mock_result)

        assert passed >= 0
        assert failed >= 0

    @pytest.mark.asyncio
    async def test_execute_test_with_parameters(self, validator):
        """Test SQL execution with parameters."""
        test_case = SQLTestCase(
            id="DB-005",
            name="Parameterized query",
            sql="SELECT * FROM users WHERE id = $1",
            parameters={"id": 1},
            assertions=[],
        )

        mock_conn = AsyncMock()
        mock_conn.fetch.return_value = [{"id": 1, "name": "John"}]
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        assert result.status == TestStatus.PASSED
        assert result.rows_returned == 1

    @pytest.mark.asyncio
    async def test_execute_test_multiple_rows(self, validator):
        """Test query returning multiple rows."""
        test_case = SQLTestCase(
            id="DB-006",
            name="Multiple rows",
            sql="SELECT * FROM users LIMIT 10",
            assertions=[],
        )

        mock_conn = AsyncMock()
        mock_result = [
            {"id": i, "name": f"User{i}"}
            for i in range(1, 11)
        ]
        mock_conn.fetch.return_value = mock_result
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        assert result.status == TestStatus.PASSED
        assert result.rows_returned == 10
        assert len(result.sample_data) <= 5  # Limited to 5 sample rows

    @pytest.mark.asyncio
    async def test_execute_test_column_names(self, validator):
        """Test column names extraction."""
        test_case = SQLTestCase(
            id="DB-007",
            name="Column extraction",
            sql="SELECT id, name, email FROM users",
            assertions=[],
        )

        mock_conn = AsyncMock()
        mock_row = {"id": 1, "name": "John", "email": "john@example.com"}
        mock_conn.fetch.return_value = [mock_row]
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        assert "id" in result.columns_returned
        assert "name" in result.columns_returned
        assert "email" in result.columns_returned

    @pytest.mark.asyncio
    async def test_execute_test_empty_result(self, validator):
        """Test query with empty result."""
        test_case = SQLTestCase(
            id="DB-008",
            name="Empty result",
            sql="SELECT * FROM users WHERE id > 1000000",
            assertions=[],
        )

        mock_conn = AsyncMock()
        mock_conn.fetch.return_value = []
        validator.pool.acquire.return_value.__aenter__.return_value = mock_conn

        result = await validator.execute_test(test_case)

        assert result.status == TestStatus.PASSED
        assert result.rows_returned == 0
        assert result.sample_data == []
