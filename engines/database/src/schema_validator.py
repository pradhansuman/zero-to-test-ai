"""Database schema validation."""
import logging
from typing import List

import asyncpg

from shared.contracts.engine_schemas import (
    SchemaValidationCase, SchemaValidationResult, DatabaseColumn, ConstraintType
)

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validates database schema structure."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def validate(self, test_case: SchemaValidationCase) -> SchemaValidationResult:
        """Validate schema against expected structure."""
        try:
            actual_columns = await self._get_columns(test_case.table_name)
            expected_names = {col.name for col in test_case.expected_columns}
            actual_names = {col.name for col in actual_columns}

            missing = expected_names - actual_names
            extra = actual_names - expected_names

            columns_valid = len(missing) == 0 and len(extra) == 0
            issues = []

            if missing:
                issues.append(f"Missing columns: {missing}")
            if extra:
                issues.append(f"Extra columns: {extra}")

            return SchemaValidationResult(
                table_name=test_case.table_name,
                valid=columns_valid,
                columns_valid=columns_valid,
                actual_columns=actual_columns,
                missing_columns=list(missing),
                extra_columns=list(extra),
                issues=issues,
            )

        except Exception as e:
            logger.error(f"Schema validation error: {e}")
            return SchemaValidationResult(
                table_name=test_case.table_name,
                valid=False,
                columns_valid=False,
                actual_columns=[],
                missing_columns=[],
                extra_columns=[],
                issues=[str(e)],
            )

    async def _get_columns(self, table_name: str) -> List[DatabaseColumn]:
        """Fetch column definitions for a table."""
        query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position
        """

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, table_name)

        return [
            DatabaseColumn(
                name=row["column_name"],
                type=row["data_type"],
                nullable=row["is_nullable"] == "YES",
            )
            for row in rows
        ]
