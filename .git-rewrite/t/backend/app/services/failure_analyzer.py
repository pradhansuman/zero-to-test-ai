"""Failure analysis service using Claude AI for test failure root cause detection."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.claude_client import ClaudeClient
from app.utils.logger import StructuredLogger
from app.database.models import TestCase
from collections import defaultdict

logger = StructuredLogger(__name__)


class FailureAnalyzer:
    """Analyzes test failures to classify types and suggest fixes."""

    FAILURE_TYPES = {
        "assertion": "Expected vs actual mismatch - test logic validation failure",
        "timeout": "Operation took too long - performance or wait issue",
        "network": "Connection/API failure - external service unreachable",
        "locator": "Element not found - selector drift or UI change",
        "environment": "Missing config/resource - test environment issue",
        "unknown": "Other failure type",
    }

    def __init__(self, db: AsyncSession, claude_client: ClaudeClient = None):
        self.db = db
        self.claude = claude_client or ClaudeClient()
        self.failure_history = defaultdict(list)

    async def analyze_failure(
        self,
        error_msg: str,
        test_name: str,
        stack_trace: str = "",
        test_case_id: int = None,
    ) -> dict:
        """Analyze test failure and suggest root cause and fixes.

        Args:
            error_msg: Error message from test failure
            test_name: Name of the test that failed
            stack_trace: Full stack trace if available
            test_case_id: Associated test case ID for context

        Returns:
            Analysis with failure type, root cause, and fix suggestions
        """
        try:
            # Step 1: Classify failure type
            failure_type = self._classify_failure(error_msg, stack_trace)
            logger.info(
                "failure_classified",
                test_name=test_name,
                failure_type=failure_type,
            )

            # Step 2: Check history for similar failures
            similar_failures = await self._check_failure_history(
                error_msg, failure_type
            )

            # Step 3: Use Claude to analyze failure deeply
            analysis = await self.claude.analyze_test_failure(
                error_message=error_msg,
                test_name=test_name,
                stack_trace=stack_trace,
            )

            # Step 4: Enhance with context-aware suggestions
            enhanced_analysis = {
                "test_name": test_name,
                "failure_type": failure_type,
                "failure_type_description": self.FAILURE_TYPES.get(
                    failure_type, "Unknown"
                ),
                "error_message": error_msg,
                "root_cause": analysis.get("analysis", ""),
                "suggested_fixes": analysis.get("fixes", []),
                "priority": self._calculate_priority(failure_type),
                "similar_failures_count": len(similar_failures),
                "test_case_id": test_case_id,
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Step 5: Store in history
            await self._store_failure_analysis(enhanced_analysis)

            return enhanced_analysis

        except Exception as e:
            logger.error(
                "failure_analysis_error",
                error=str(e),
                test_name=test_name,
            )
            return {
                "error": f"Analysis failed: {str(e)}",
                "test_name": test_name,
                "failure_type": "unknown",
            }

    def _classify_failure(self, error_msg: str, stack_trace: str = "") -> str:
        """Classify failure type based on error message and stack trace.

        Args:
            error_msg: Error message text
            stack_trace: Stack trace if available

        Returns:
            Failure type key from FAILURE_TYPES
        """
        error_lower = error_msg.lower()
        trace_lower = stack_trace.lower() if stack_trace else ""

        # Priority-ordered classification rules (environment first to avoid "api" confusion)
        if any(
            word in error_lower
            for word in [
                "environment",
                "environmenterror",
                "env",
                "config",
                "missing",
                "undefined",
                "not set",
            ]
        ):
            return "environment"

        if any(
            word in error_lower
            for word in [
                "timeout",
                "timed out",
                "wait timeout",
                "maximum timeout",
            ]
        ):
            return "timeout"

        if any(
            word in error_lower
            for word in [
                "assert",
                "assertion",
                "expect",
                "expected",
                "should",
            ]
        ):
            return "assertion"

        if any(
            word in error_lower
            for word in [
                "locator",
                "selector",
                "element",
                "not found",
                "cannot find",
                "no such element",
            ]
        ):
            return "locator"

        if any(
            word in error_lower
            for word in ["connection", "network", "http", "request"]
        ):
            return "network"

        return "unknown"

    async def _check_failure_history(
        self, error_msg: str, failure_type: str
    ) -> list:
        """Check if similar failures have occurred before.

        Args:
            error_msg: Error message to match
            failure_type: Classified failure type

        Returns:
            List of similar failures from history
        """
        similar = []
        error_key = failure_type

        if error_key in self.failure_history:
            for previous in self.failure_history[error_key]:
                # Simple similarity check - same type + keyword overlap
                if any(
                    word in error_msg.lower()
                    for word in previous["error_message"].lower().split()
                ):
                    similar.append(previous)

        return similar[:5]  # Return top 5 similar failures

    async def _store_failure_analysis(self, analysis: dict):
        """Store failure analysis in history for learning.

        Args:
            analysis: Analysis result dict
        """
        failure_type = analysis.get("failure_type", "unknown")

        # Store in memory history (production would use database)
        self.failure_history[failure_type].append(
            {
                "error_message": analysis.get("error_message", ""),
                "root_cause": analysis.get("root_cause", ""),
                "suggested_fixes": analysis.get("suggested_fixes", []),
                "timestamp": analysis.get("timestamp", ""),
            }
        )

        # Keep only last 100 failures per type for memory efficiency
        if len(self.failure_history[failure_type]) > 100:
            self.failure_history[failure_type] = (
                self.failure_history[failure_type][-100:]
            )

        logger.info(
            "failure_stored",
            failure_type=failure_type,
            total_stored=len(self.failure_history[failure_type]),
        )

    def _calculate_priority(self, failure_type: str) -> str:
        """Calculate priority for fixing based on failure type.

        Args:
            failure_type: Type of failure

        Returns:
            Priority level: "critical", "high", "medium", "low"
        """
        priority_map = {
            "assertion": "high",  # Logic issue
            "timeout": "high",  # Performance issue
            "network": "high",  # Infrastructure issue
            "locator": "medium",  # Can be auto-healed
            "environment": "critical",  # Blocks all tests
            "unknown": "low",  # Needs investigation
        }
        return priority_map.get(failure_type, "low")

    async def get_failure_patterns(self, project_id: int) -> dict:
        """Get common failure patterns for a project.

        Args:
            project_id: Project ID to analyze

        Returns:
            Dictionary with failure patterns and frequency
        """
        try:
            # Query test cases for project
            result = await self.db.execute(
                select(TestCase).where(TestCase.project_id == project_id)
            )
            test_cases = result.scalars().all()

            patterns = defaultdict(int)
            for tc in test_cases:
                if tc.last_failure:
                    failure_type = self._classify_failure(tc.last_failure)
                    patterns[failure_type] += 1

            return {
                "project_id": project_id,
                "total_tests": len(test_cases),
                "patterns": dict(patterns),
                "top_pattern": max(patterns, key=patterns.get)
                if patterns
                else None,
                "analysis_timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error("failure_pattern_error", project_id=project_id, error=str(e))
            return {"error": str(e), "project_id": project_id}

    async def get_analysis_statistics(self, hours: int = 24) -> dict:
        """Get statistics on failure analyses performed.

        Args:
            hours: Time period to analyze (default: 24h)

        Returns:
            Statistics on failure analyses
        """
        total_failures = sum(len(v) for v in self.failure_history.values())
        failure_type_counts = {k: len(v) for k, v in self.failure_history.items()}

        return {
            "period_hours": hours,
            "total_failures_analyzed": total_failures,
            "by_type": failure_type_counts,
            "most_common": max(failure_type_counts, key=failure_type_counts.get)
            if failure_type_counts
            else None,
            "timestamp": datetime.utcnow().isoformat(),
        }
