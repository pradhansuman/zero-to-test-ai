"""Tests for Phase 4 Task 3: Intelligent Test Prioritization."""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import (
    Project, User, TestCase, ExecutionResult, ExecutionStatus,
    PerformanceProfile, UserRole, TestFramework
)
from app.services.test_prioritization_service import TestPrioritizationService


class TestPrioritizationFeature:
    """Test suite for intelligent test prioritization."""

    async def test_calculate_risk_score_high_risk(self, test_db: AsyncSession):
        """Test risk score calculation for high-risk changes."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_api_users",
            description="Test user API",
            test_code="test code",
            test_type="integration"
        )
        test_db.add(test_case)
        await test_db.commit()

        service = TestPrioritizationService(test_db)

        code_changes = [
            {"file": "src/api/users.py", "module": "api"},
            {"file": "src/services/user_service.py", "module": "service"}
        ]

        risk_score = await service.calculate_risk_score(project.id, code_changes, test_case)

        # Should detect API changes match test_api pattern
        assert risk_score > 0.3
        assert risk_score <= 1.0

    async def test_calculate_risk_score_low_risk(self, test_db: AsyncSession):
        """Test risk score for unrelated changes."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_ui_login",
            description="Test login UI",
            test_code="test code",
            test_type="e2e"
        )
        test_db.add(test_case)
        await test_db.commit()

        service = TestPrioritizationService(test_db)

        code_changes = [
            {"file": "docs/README.md", "module": "docs"},
            {"file": "config/docker-compose.yml", "module": "config"}
        ]

        risk_score = await service.calculate_risk_score(project.id, code_changes, test_case)

        # Should be low risk for documentation changes
        assert risk_score < 0.5

    async def test_calculate_stability_score_stable_test(self, test_db: AsyncSession):
        """Test stability score for consistently passing test."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_stable",
            description="Stable test",
            test_code="test code",
            test_type="unit"
        )
        test_db.add(test_case)
        await test_db.flush()

        # Add execution results (all passing)
        for i in range(10):
            result = ExecutionResult(
                execution_id=i,
                test_case_id=test_case.id,
                status=ExecutionStatus.PASSED,
                duration_seconds=5.0,
                created_at=datetime.utcnow() - timedelta(days=30-i)
            )
            test_db.add(result)
        await test_db.commit()

        service = TestPrioritizationService(test_db)
        stability = await service.calculate_stability_score(project.id, test_case.id)

        # Should be high (close to 1.0) for consistently passing test
        assert stability > 0.8
        assert stability <= 1.0

    async def test_calculate_stability_score_flaky_test(self, test_db: AsyncSession):
        """Test stability score for flaky test."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_flaky",
            description="Flaky test",
            test_code="test code",
            test_type="e2e"
        )
        test_db.add(test_case)
        await test_db.flush()

        # Add alternating pass/fail results
        for i in range(10):
            result = ExecutionResult(
                execution_id=i,
                test_case_id=test_case.id,
                status=ExecutionStatus.PASSED if i % 2 == 0 else ExecutionStatus.FAILED,
                duration_seconds=5.0,
                created_at=datetime.utcnow() - timedelta(days=30-i)
            )
            test_db.add(result)
        await test_db.commit()

        service = TestPrioritizationService(test_db)
        stability = await service.calculate_stability_score(project.id, test_case.id)

        # Should be lower (around 0.5) for flaky test
        assert stability < 0.7

    async def test_update_performance_profile(self, test_db: AsyncSession):
        """Test performance profile updates."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_performance",
            description="Performance test",
            test_code="test code",
            test_type="performance"
        )
        test_db.add(test_case)
        await test_db.commit()

        service = TestPrioritizationService(test_db)

        # Record first execution
        result1 = await service.update_performance_profile(project.id, test_case.id, 10.0)
        assert result1["avg_duration"] == 10.0
        assert result1["runs_count"] == 1

        await test_db.commit()

        # Record second execution
        result2 = await service.update_performance_profile(project.id, test_case.id, 12.0)
        assert result2["avg_duration"] == 11.0  # Average of 10 and 12
        assert result2["runs_count"] == 2

        await test_db.commit()

        # Get profile
        profile = await service.get_performance_profile(test_case.id)
        assert profile["avg_duration"] == 11.0
        assert profile["runs_count"] == 2

    async def test_prioritize_tests_ordering(self, test_db: AsyncSession):
        """Test that tests are ordered correctly by priority."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        # Create test cases with different risk profiles
        high_risk_test = TestCase(
            project_id=project.id,
            name="test_api_critical",
            description="Critical API test",
            test_code="test code",
            test_type="integration"
        )
        low_risk_test = TestCase(
            project_id=project.id,
            name="test_docs_example",
            description="Documentation example",
            test_code="test code",
            test_type="unit"
        )
        test_db.add_all([high_risk_test, low_risk_test])
        await test_db.commit()

        service = TestPrioritizationService(test_db)

        code_changes = [
            {"file": "src/api/critical.py", "module": "api"},
        ]

        result = await service.prioritize_tests(
            project_id=project.id,
            test_ids=[high_risk_test.id, low_risk_test.id],
            code_changes=code_changes
        )

        # High-risk test should be first
        prioritized = result["prioritized_tests"]
        assert len(prioritized) == 2
        assert prioritized[0]["order"] == 1
        assert prioritized[1]["order"] == 2

        # High-risk should have higher priority score
        assert prioritized[0]["priority_score"] >= prioritized[1]["priority_score"]

    async def test_duration_score_calculation(self, test_db: AsyncSession):
        """Test duration score calculation."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_slow",
            description="Slow test",
            test_code="test code",
            test_type="e2e"
        )
        test_db.add(test_case)
        await test_db.flush()

        # Create performance profile with 30 second duration
        profile = PerformanceProfile(
            test_case_id=test_case.id,
            project_id=project.id,
            avg_duration=30.0,
            min_duration=25.0,
            max_duration=35.0,
            p50_duration=30.0,
            p95_duration=34.0,
            runs_count=20
        )
        test_db.add(profile)
        await test_db.commit()

        service = TestPrioritizationService(test_db)
        duration_score = await service.calculate_duration_score(project.id, test_case.id)

        # 30 seconds = 0.5 on 0-60 second scale
        assert 0.4 < duration_score < 0.6

    async def test_priority_score_weighting(self, test_db: AsyncSession):
        """Test that priority score correctly weights risk and stability."""
        service = TestPrioritizationService(test_db)

        # High risk, stable test should score high
        score1 = await service.calculate_priority_score(
            risk_score=0.9,
            impact_score=0.5,
            duration_score=0.5,
            stability_score=0.9
        )

        # Low risk, unstable test should score medium
        score2 = await service.calculate_priority_score(
            risk_score=0.1,
            impact_score=0.1,
            duration_score=0.5,
            stability_score=0.3
        )

        # Risk and stability heavily influence score
        assert score1 > score2

    async def test_reasoning_generation(self, test_db: AsyncSession):
        """Test that reasonable explanations are provided."""
        user = User(email="test@example.com", username="testuser", password_hash="hashed", role=UserRole.ADMIN)
        test_db.add(user)
        await test_db.flush()
        project = Project(name="Test Project", owner_id=user.id, test_framework=TestFramework.PLAYWRIGHT)
        test_db.add(project)
        await test_db.flush()

        test_case = TestCase(
            project_id=project.id,
            name="test_critical_api",
            description="Critical API test",
            test_code="test code",
            test_type="integration"
        )
        test_db.add(test_case)
        await test_db.flush()

        # Create execution results showing instability
        for i in range(10):
            result = ExecutionResult(
                execution_id=i,
                test_case_id=test_case.id,
                status=ExecutionStatus.PASSED if i < 3 else ExecutionStatus.FAILED,
                duration_seconds=5.0,
                created_at=datetime.utcnow() - timedelta(days=30-i)
            )
            test_db.add(result)
        await test_db.commit()

        service = TestPrioritizationService(test_db)

        code_changes = [{"file": "src/api/critical.py", "module": "api"}]
        result = await service.prioritize_tests(
            project_id=project.id,
            test_ids=[test_case.id],
            code_changes=code_changes
        )

        # Should have meaningful reasons
        test_info = result["prioritized_tests"][0]
        assert len(test_info["reasons"]) > 0
        assert any("risk" in reason.lower() or "flaky" in reason.lower() for reason in test_info["reasons"])
