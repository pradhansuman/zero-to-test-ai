"""AI test code review service for quality analysis."""
import re
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.claude_client import ClaudeClient
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class TestReviewer:
    """Reviews test code for quality and coverage."""

    def __init__(self, db: AsyncSession, claude_client: ClaudeClient = None):
        self.db = db
        self.claude = claude_client or ClaudeClient()

    async def review_test_code(
        self,
        test_code: str,
        framework: str = "pytest"
    ) -> dict:
        """Review test code quality comprehensively.

        Args:
            test_code: Test code to review
            framework: Test framework (pytest, unittest, playwright)

        Returns:
            Review with metrics and suggestions
        """
        try:
            metrics = {
                "coverage_score": self._calculate_coverage_score(test_code),
                "maintainability": self._score_maintainability(test_code),
                "assertions_quality": self._score_assertions(test_code),
                "edge_cases": self._detect_edge_cases(test_code),
                "complexity": self._calculate_cyclomatic_complexity(test_code),
                "docstring_completeness": self._check_documentation(test_code),
            }

            # Get Claude review for deep analysis
            review = await self.claude.optimize_test_code(test_code, framework)

            overall_score = self._aggregate_score(metrics)

            result = {
                "framework": framework,
                "metrics": metrics,
                "overall_score": overall_score,
                "improvements": review.get("improvements", []),
                "summary": review.get("summary", ""),
                "timestamp": datetime.utcnow().isoformat(),
            }

            logger.info(
                "test_reviewed",
                framework=framework,
                overall_score=overall_score,
            )

            return result

        except Exception as e:
            logger.error("test_review_error", error=str(e))
            return {"error": str(e)}

    def _calculate_coverage_score(self, test_code: str) -> float:
        """Calculate test coverage score (0-100).

        Args:
            test_code: Test code

        Returns:
            Coverage score
        """
        # Count assertions
        assert_count = len(re.findall(r"assert\s+", test_code))
        if_count = len(re.findall(r"if\s+", test_code))

        # Simple heuristic: more assertions = better coverage
        score = min(100, (assert_count / max(1, if_count)) * 50 + 50)
        return round(score, 1)

    def _score_maintainability(self, test_code: str) -> float:
        """Score code maintainability (0-100).

        Args:
            test_code: Test code

        Returns:
            Maintainability score
        """
        lines = test_code.split("\n")
        long_lines = sum(1 for line in lines if len(line) > 100)
        nested_depth = self._max_indentation_depth(test_code)

        # Penalize long lines and deep nesting
        score = 100
        score -= min(20, long_lines)
        score -= min(30, nested_depth * 10)

        return max(0, round(score, 1))

    def _score_assertions(self, test_code: str) -> float:
        """Score assertion quality (0-100).

        Args:
            test_code: Test code

        Returns:
            Assertion score
        """
        assertions = len(re.findall(r"assert\s+", test_code))

        # 3-5 assertions is ideal
        if 3 <= assertions <= 5:
            return 90.0
        elif assertions < 3:
            return 60.0
        else:
            return 75.0

    def _detect_edge_cases(self, test_code: str) -> list:
        """Detect edge cases covered in test.

        Args:
            test_code: Test code

        Returns:
            List of detected edge cases
        """
        edge_cases = []

        if re.search(r"None|null", test_code):
            edge_cases.append("Null handling")
        if re.search(r"empty|len\(\s*0", test_code):
            edge_cases.append("Empty collections")
        if re.search(r"negative|-\d+", test_code):
            edge_cases.append("Negative values")
        if re.search(r"max|MAX|boundary", test_code):
            edge_cases.append("Boundary values")
        if re.search(r"exception|Exception|error", test_code):
            edge_cases.append("Exception handling")

        return edge_cases

    def _calculate_cyclomatic_complexity(self, test_code: str) -> int:
        """Calculate cyclomatic complexity.

        Args:
            test_code: Test code

        Returns:
            Complexity score
        """
        # Count control flow statements
        conditions = len(re.findall(r"if|elif|else|for|while", test_code))
        return conditions + 1

    def _check_documentation(self, test_code: str) -> float:
        """Check docstring and comment completeness.

        Args:
            test_code: Test code

        Returns:
            Documentation score (0-100)
        """
        has_docstring = '"""' in test_code or "'''" in test_code
        comment_lines = len(re.findall(r"#", test_code))

        score = 0
        if has_docstring:
            score += 50
        score += min(50, comment_lines * 10)

        return min(100.0, float(score))

    def _max_indentation_depth(self, test_code: str) -> int:
        """Calculate maximum indentation depth.

        Args:
            test_code: Test code

        Returns:
            Max indentation level
        """
        lines = test_code.split("\n")
        max_depth = 0

        for line in lines:
            if line.strip():
                depth = len(line) - len(line.lstrip())
                max_depth = max(max_depth, depth // 4)

        return max_depth

    def _aggregate_score(self, metrics: dict) -> float:
        """Aggregate all metrics into overall score.

        Args:
            metrics: Dictionary of metric scores

        Returns:
            Overall score (0-100)
        """
        weights = {
            "coverage_score": 0.3,
            "maintainability": 0.25,
            "assertions_quality": 0.25,
            "edge_cases": 0.1,
            "complexity": 0.05,
            "docstring_completeness": 0.05,
        }

        total = 0
        for metric, weight in weights.items():
            if metric in metrics:
                value = metrics[metric]
                # Normalize edge_cases and complexity
                if metric == "edge_cases":
                    value = min(100, len(value) * 20)
                elif metric == "complexity":
                    value = max(0, 100 - value * 5)

                total += value * weight

        return round(total, 1)

    async def suggest_test_improvements(
        self,
        test_code: str,
        framework: str = "pytest"
    ) -> dict:
        """Suggest test improvements.

        Args:
            test_code: Test code
            framework: Test framework

        Returns:
            Improvement suggestions
        """
        try:
            improvements = []

            # Static analysis checks
            if len(test_code.split("\n")) > 50:
                improvements.append({
                    "type": "size",
                    "message": "Test is too long, consider splitting",
                    "priority": "medium",
                })

            if self._max_indentation_depth(test_code) > 3:
                improvements.append({
                    "type": "nesting",
                    "message": "Deep nesting detected, simplify logic",
                    "priority": "medium",
                })

            assert_count = len(re.findall(r"assert\s+", test_code))
            if assert_count < 3:
                improvements.append({
                    "type": "coverage",
                    "message": "Add more assertions for better coverage",
                    "priority": "high",
                })

            if "def test_" not in test_code:
                improvements.append({
                    "type": "structure",
                    "message": "Missing test function definition",
                    "priority": "critical",
                })

            return {
                "framework": framework,
                "improvement_count": len(improvements),
                "improvements": improvements,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error("improvement_suggestion_error", error=str(e))
            return {"error": str(e)}
