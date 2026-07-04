"""Test impact analysis service for smart test selection in CI/CD."""
import re
from datetime import datetime
from typing import List, Set, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import TestCase, Project
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class ImpactAnalyzer:
    """Analyzes code changes to determine which tests are affected."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.import_cache = {}

    async def analyze_code_changes(
        self,
        project_id: int,
        files_changed: List[str],
        branch: str = "main"
    ) -> Dict:
        """Determine which tests are affected by code changes.

        Args:
            project_id: Project ID to analyze
            files_changed: List of changed file paths
            branch: Git branch being analyzed

        Returns:
            Dictionary with affected tests and impact metrics
        """
        try:
            # Step 1: Get all test files for project
            result = await self.db.execute(
                select(TestCase).where(TestCase.project_id == project_id)
            )
            all_tests = result.scalars().all()
            all_test_ids = {tc.id for tc in all_tests}

            # Step 2: Find affected tests
            affected_test_ids = set()

            for test in all_tests:
                if test.test_code and self._test_imports_files(
                    test.test_code, files_changed
                ):
                    affected_test_ids.add(test.id)

            # Step 3: Calculate impact metrics
            total_tests = len(all_test_ids)
            affected_count = len(affected_test_ids)
            unaffected_count = total_tests - affected_count

            savings_percent = (
                100 * (unaffected_count / total_tests) if total_tests > 0 else 0
            )

            impact_analysis = {
                "project_id": project_id,
                "branch": branch,
                "total_tests": total_tests,
                "affected_tests": affected_count,
                "unaffected_tests": unaffected_count,
                "affected_test_ids": list(affected_test_ids),
                "savings_percent": round(savings_percent, 2),
                "files_changed": files_changed,
                "analysis_timestamp": datetime.utcnow().isoformat(),
            }

            logger.info(
                "impact_analysis_complete",
                project_id=project_id,
                total_tests=total_tests,
                affected_tests=affected_count,
                savings_percent=savings_percent,
            )

            return impact_analysis

        except Exception as e:
            logger.error("impact_analysis_error", error=str(e))
            return {"error": str(e), "project_id": project_id}

    def _test_imports_files(
        self,
        test_code: str,
        files_changed: List[str]
    ) -> bool:
        """Check if test imports any of the changed files.

        Args:
            test_code: Test code to analyze
            files_changed: List of changed file paths

        Returns:
            True if test imports any changed files
        """
        test_code_lower = test_code.lower()

        for changed_file in files_changed:
            # Normalize file path for matching
            module_name = self._file_to_module(changed_file)

            # Check various import patterns
            import_patterns = [
                f"from {module_name}",
                f"import {module_name}",
                f"from {changed_file}",
                f"import {changed_file}",
            ]

            for pattern in import_patterns:
                if pattern.lower() in test_code_lower:
                    return True

        return False

    def _file_to_module(self, file_path: str) -> str:
        """Convert file path to Python module name.

        Args:
            file_path: File path (e.g., "app/services/auth.py")

        Returns:
            Module name (e.g., "app.services.auth")
        """
        # Remove .py extension
        if file_path.endswith(".py"):
            file_path = file_path[:-3]

        # Replace path separators with dots
        module_name = file_path.replace("/", ".").replace("\\", ".")

        return module_name

    async def select_tests_for_ci(
        self,
        project_id: int,
        pr_files: List[str],
        strategy: str = "affected"
    ) -> Dict:
        """Select minimal test subset for CI execution.

        Args:
            project_id: Project ID
            pr_files: List of changed files in PR
            strategy: "affected" or "all"
                - affected: Run only affected tests
                - all: Run all tests (for final verification)

        Returns:
            Dictionary with test selection and timing estimates
        """
        try:
            # Get impact analysis
            analysis = await self.analyze_code_changes(project_id, pr_files)

            if "error" in analysis:
                return analysis

            if strategy == "affected":
                selected_ids = analysis["affected_test_ids"]
            else:
                # Get all test IDs
                result = await self.db.execute(
                    select(TestCase).where(TestCase.project_id == project_id)
                )
                all_tests = result.scalars().all()
                selected_ids = [tc.id for tc in all_tests]

            # Estimate execution time
            estimated_time = self._estimate_execution_time(
                len(selected_ids)
            )

            selection_result = {
                "project_id": project_id,
                "strategy": strategy,
                "selected_test_count": len(selected_ids),
                "selected_test_ids": selected_ids,
                "total_tests": analysis["total_tests"],
                "estimated_duration_seconds": estimated_time,
                "time_saved_seconds": self._estimate_execution_time(
                    analysis["total_tests"]
                ) - estimated_time,
                "ci_efficiency": round(
                    100 * (1 - len(selected_ids) / analysis["total_tests"]),
                    2
                ) if analysis["total_tests"] > 0 else 0,
            }

            logger.info(
                "tests_selected",
                project_id=project_id,
                strategy=strategy,
                selected_count=len(selected_ids),
                efficiency=selection_result["ci_efficiency"],
            )

            return selection_result

        except Exception as e:
            logger.error("test_selection_error", error=str(e))
            return {"error": str(e)}

    def _estimate_execution_time(self, test_count: int) -> int:
        """Estimate test execution time in seconds.

        Args:
            test_count: Number of tests to run

        Returns:
            Estimated time in seconds
        """
        # Rough estimate: ~2 seconds per test
        # Plus 30 seconds for setup/teardown
        return (test_count * 2) + 30

    async def get_test_dependencies(
        self,
        project_id: int,
        test_id: int
    ) -> Dict:
        """Get dependencies for a specific test.

        Args:
            project_id: Project ID
            test_id: Test case ID

        Returns:
            Dictionary with dependencies
        """
        try:
            result = await self.db.execute(
                select(TestCase).where(
                    TestCase.id == test_id,
                    TestCase.project_id == project_id
                )
            )
            test_case = result.scalar_one_or_none()

            if not test_case:
                return {"error": "Test case not found", "test_id": test_id}

            dependencies = self._extract_dependencies(test_case.test_code)

            return {
                "test_id": test_id,
                "test_name": test_case.name,
                "imports": dependencies.get("imports", []),
                "fixtures": dependencies.get("fixtures", []),
                "dependency_count": len(
                    dependencies.get("imports", []) +
                    dependencies.get("fixtures", [])
                ),
            }

        except Exception as e:
            logger.error("dependency_extraction_error", error=str(e))
            return {"error": str(e)}

    def _extract_dependencies(self, test_code: str) -> Dict[str, List[str]]:
        """Extract import and fixture dependencies from test code.

        Args:
            test_code: Test code to analyze

        Returns:
            Dictionary with imports and fixtures
        """
        imports = []
        fixtures = []

        # Extract imports
        import_pattern = r"(?:from|import)\s+([\w\.]+)"
        imports = re.findall(import_pattern, test_code)

        # Extract pytest fixtures (parameters in function definition)
        fixture_pattern = r"def\s+test_\w+\([^)]*(\w+)[^)]*\):"
        fixtures = re.findall(fixture_pattern, test_code)

        return {
            "imports": list(set(imports)),
            "fixtures": list(set(fixtures)),
        }

    async def get_impact_statistics(
        self,
        project_id: int,
        days: int = 7
    ) -> Dict:
        """Get impact analysis statistics for a project.

        Args:
            project_id: Project ID
            days: Number of days to analyze

        Returns:
            Statistics on test impact
        """
        try:
            result = await self.db.execute(
                select(TestCase).where(TestCase.project_id == project_id)
            )
            test_cases = result.scalars().all()

            total = len(test_cases)
            with_dependencies = sum(
                1 for tc in test_cases
                if tc.test_code and len(
                    self._extract_dependencies(tc.test_code)["imports"]
                ) > 0
            )

            return {
                "project_id": project_id,
                "period_days": days,
                "total_tests": total,
                "tests_with_dependencies": with_dependencies,
                "independent_tests": total - with_dependencies,
                "avg_dependencies": round(
                    with_dependencies / total, 2
                ) if total > 0 else 0,
                "analysis_timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error("impact_statistics_error", error=str(e))
            return {"error": str(e)}
