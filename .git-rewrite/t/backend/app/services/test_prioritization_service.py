"""Intelligent test prioritization service for Phase 4 Task 3."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models import (
    TestCase, TestPrioritization, PerformanceProfile,
    Execution, ExecutionResult, ExecutionStatus
)
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class TestPrioritizationService:
    """Service for intelligent test prioritization based on risk and impact."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_risk_score(
        self,
        project_id: int,
        code_changes: List[Dict[str, str]],
        test_case: TestCase
    ) -> float:
        """
        Calculate risk score (0.0-1.0) based on code change patterns.
        Higher score = higher risk = should run earlier.
        """
        if not code_changes:
            return 0.5  # Default medium risk

        risk_score = 0.0

        # Check if test name matches changed files/modules
        for change in code_changes:
            file_path = change.get("file", "").lower()
            test_name = (test_case.name or "").lower()

            # Direct module match (highest risk)
            if any(part in test_name for part in file_path.split("/")):
                risk_score += 0.3

            # Type affinity (API test for API changes)
            if "api" in file_path and "api" in test_name:
                risk_score += 0.2
            elif "ui" in file_path and ("ui" in test_name or "e2e" in test_name):
                risk_score += 0.2

            # Database changes
            if "database" in file_path or "migration" in file_path:
                if "integration" in test_name or "api" in test_name:
                    risk_score += 0.15

        # Normalize to 0.0-1.0
        return min(risk_score, 1.0)

    async def calculate_impact_score(
        self,
        project_id: int,
        test_case_id: int,
        code_changes: List[Dict[str, str]]
    ) -> float:
        """
        Calculate impact score from integration analysis.
        Uses Phase 3 impact analysis data if available.
        """
        try:
            # Get test's historical impact
            result = await self.db.execute(
                select(ExecutionResult)
                .where(ExecutionResult.test_case_id == test_case_id)
                .order_by(ExecutionResult.created_at.desc())
                .limit(50)
            )
            results = result.scalars().all()

            if not results:
                return 0.5

            # Count recent failures as indicator of impact
            recent_failures = sum(1 for r in results if r.status == ExecutionStatus.FAILED)
            impact = recent_failures / len(results)

            return min(impact + 0.2, 1.0)  # Bias toward testing previously failing areas
        except Exception as e:
            logger.error("impact_score_calculation_error", error=str(e))
            return 0.5

    async def calculate_duration_score(
        self,
        project_id: int,
        test_case_id: int
    ) -> float:
        """
        Calculate duration score (inverse of execution time).
        Faster tests score lower (run later) within same risk band.
        Returns 0.0 (fast) to 1.0 (slow).
        """
        try:
            result = await self.db.execute(
                select(PerformanceProfile)
                .where(PerformanceProfile.test_case_id == test_case_id)
            )
            profile = result.scalar_one_or_none()

            if not profile or profile.avg_duration == 0:
                return 0.5

            # Normalize duration: 0s = 0.0, 60s = 1.0
            duration_score = min(profile.avg_duration / 60.0, 1.0)
            return duration_score
        except Exception as e:
            logger.error("duration_score_calculation_error", error=str(e))
            return 0.5

    async def calculate_stability_score(
        self,
        project_id: int,
        test_case_id: int
    ) -> float:
        """
        Calculate stability score (0.0=flaky, 1.0=stable).
        Based on historical pass rate over 30 days.
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            result = await self.db.execute(
                select(ExecutionResult)
                .where(
                    (ExecutionResult.test_case_id == test_case_id)
                    & (ExecutionResult.created_at >= cutoff_date)
                )
            )
            results = result.scalars().all()

            if not results:
                return 0.8  # Default to stable if no history

            passes = sum(1 for r in results if r.status == ExecutionStatus.PASSED)
            pass_rate = passes / len(results)

            # Pass rate directly maps to stability
            return pass_rate
        except Exception as e:
            logger.error("stability_score_calculation_error", error=str(e))
            return 0.8

    async def calculate_priority_score(
        self,
        risk_score: float,
        impact_score: float,
        duration_score: float,
        stability_score: float
    ) -> float:
        """
        Calculate overall priority score using weighted combination.
        Higher score = run earlier.
        """
        # Weights: risk and impact are most important
        weights = {
            "risk": 0.40,
            "impact": 0.30,
            "stability": 0.20,  # Flaky tests should run earlier to catch issues
            "duration": 0.10,   # Speed optimization is secondary to correctness
        }

        # Stability is inverted: flakier (lower score) = higher priority
        adjusted_stability = 1.0 - stability_score

        overall_score = (
            (risk_score * weights["risk"]) +
            (impact_score * weights["impact"]) +
            (adjusted_stability * weights["stability"]) +
            ((1.0 - duration_score) * weights["duration"])  # Invert duration: fast = high priority
        )

        return min(overall_score, 1.0)

    async def prioritize_tests(
        self,
        project_id: int,
        test_ids: List[int],
        code_changes: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Prioritize tests and return ordered list with scores and reasoning.
        """
        try:
            # Get test cases
            result = await self.db.execute(
                select(TestCase).where(
                    (TestCase.project_id == project_id)
                    & (TestCase.id.in_(test_ids))
                )
            )
            test_cases = result.scalars().all()

            prioritized = []

            for test_case in test_cases:
                # Calculate individual scores
                risk = await self.calculate_risk_score(project_id, code_changes, test_case)
                impact = await self.calculate_impact_score(project_id, test_case.id, code_changes)
                duration = await self.calculate_duration_score(project_id, test_case.id)
                stability = await self.calculate_stability_score(project_id, test_case.id)

                # Calculate overall priority
                priority_score = await self.calculate_priority_score(
                    risk, impact, duration, stability
                )

                # Generate reasoning
                reasons = []
                if risk > 0.6:
                    reasons.append("High code change risk")
                if impact > 0.6:
                    reasons.append("High failure impact")
                if stability < 0.8:
                    reasons.append(f"Flaky test ({stability:.0%} stable)")
                if duration < 0.3:
                    reasons.append("Fast execution (optimization)")

                prioritized.append({
                    "test_id": test_case.id,
                    "test_name": test_case.name,
                    "priority_score": round(priority_score, 3),
                    "risk_score": round(risk, 3),
                    "impact_score": round(impact, 3),
                    "duration_score": round(duration, 3),
                    "stability_score": round(stability, 3),
                    "reasons": reasons if reasons else ["Standard test"]
                })

            # Sort by priority score descending (highest first)
            prioritized.sort(key=lambda x: x["priority_score"], reverse=True)

            # Add execution order
            for idx, item in enumerate(prioritized, 1):
                item["order"] = idx

            logger.info(
                "tests_prioritized",
                project_id=project_id,
                count=len(prioritized),
                avg_score=round(sum(p["priority_score"] for p in prioritized) / len(prioritized), 3)
            )

            return {
                "project_id": project_id,
                "prioritized_tests": prioritized,
                "total_tests": len(prioritized),
                "timestamp": datetime.utcnow().isoformat(),
                "code_changes_analyzed": len(code_changes)
            }
        except Exception as e:
            logger.error("test_prioritization_error", error=str(e))
            return {"error": str(e)}

    async def save_prioritization(
        self,
        project_id: int,
        test_id: int,
        priority_score: float,
        scores: Dict[str, float],
        reasons: List[str]
    ) -> Dict[str, Any]:
        """Save prioritization result to database for history/learning."""
        try:
            prioritization = TestPrioritization(
                project_id=project_id,
                test_case_id=test_id,
                risk_score=scores.get("risk", 0.5),
                impact_score=scores.get("impact", 0.5),
                duration_score=scores.get("duration", 0.5),
                stability_score=scores.get("stability", 0.8),
                overall_priority_score=priority_score,
                reasoning={
                    "reasons": reasons,
                    "weights": {
                        "risk": 0.40,
                        "impact": 0.30,
                        "stability": 0.20,
                        "duration": 0.10
                    }
                }
            )
            self.db.add(prioritization)
            await self.db.flush()

            logger.info(
                "prioritization_saved",
                project_id=project_id,
                test_id=test_id,
                score=priority_score
            )

            return {
                "id": prioritization.id,
                "test_id": test_id,
                "priority_score": priority_score,
                "saved_at": prioritization.calculated_at.isoformat()
            }
        except Exception as e:
            logger.error("prioritization_save_error", error=str(e))
            return {"error": str(e)}

    async def get_performance_profile(
        self,
        test_case_id: int
    ) -> Dict[str, Any]:
        """Get or create performance profile for a test."""
        try:
            result = await self.db.execute(
                select(PerformanceProfile)
                .where(PerformanceProfile.test_case_id == test_case_id)
            )
            profile = result.scalar_one_or_none()

            if not profile:
                return {
                    "test_case_id": test_case_id,
                    "avg_duration": 0,
                    "runs_count": 0,
                    "status": "no_data"
                }

            return {
                "test_case_id": test_case_id,
                "avg_duration": round(profile.avg_duration, 2),
                "min_duration": round(profile.min_duration, 2),
                "max_duration": round(profile.max_duration, 2),
                "p50_duration": round(profile.p50_duration, 2),
                "p95_duration": round(profile.p95_duration, 2),
                "runs_count": profile.runs_count,
                "trend": profile.trend,
                "updated_at": profile.updated_at.isoformat()
            }
        except Exception as e:
            logger.error("performance_profile_error", error=str(e))
            return {"error": str(e)}

    async def update_performance_profile(
        self,
        project_id: int,
        test_case_id: int,
        duration: float
    ) -> Dict[str, Any]:
        """Update performance profile with new execution data."""
        try:
            result = await self.db.execute(
                select(PerformanceProfile)
                .where(PerformanceProfile.test_case_id == test_case_id)
            )
            profile = result.scalar_one_or_none()

            if not profile:
                profile = PerformanceProfile(
                    test_case_id=test_case_id,
                    project_id=project_id,
                    avg_duration=duration,
                    min_duration=duration,
                    max_duration=duration,
                    p50_duration=duration,
                    p95_duration=duration,
                    runs_count=1,
                    last_execution_duration=duration
                )
                self.db.add(profile)
            else:
                # Update rolling averages
                old_avg = profile.avg_duration
                profile.runs_count += 1
                profile.avg_duration = (old_avg * (profile.runs_count - 1) + duration) / profile.runs_count
                profile.min_duration = min(profile.min_duration, duration)
                profile.max_duration = max(profile.max_duration, duration)
                profile.last_execution_duration = duration

                # Detect trend
                if profile.avg_duration < old_avg * 0.95:
                    profile.trend = "getting_faster"
                elif profile.avg_duration > old_avg * 1.05:
                    profile.trend = "getting_slower"
                else:
                    profile.trend = "stable"

            await self.db.flush()

            logger.info(
                "performance_profile_updated",
                test_case_id=test_case_id,
                duration=duration,
                avg_duration=round(profile.avg_duration, 2)
            )

            return {
                "test_case_id": test_case_id,
                "avg_duration": round(profile.avg_duration, 2),
                "runs_count": profile.runs_count
            }
        except Exception as e:
            logger.error("performance_profile_update_error", error=str(e))
            return {"error": str(e)}
