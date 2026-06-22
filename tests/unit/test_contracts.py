"""
tests/unit/test_contracts.py
──────────────────────────────
Unit tests for contract models and their transformation logic.

Tests SDETTestPlan.to_test_plan() priority/risk/type mapping,
and the AC extraction + bound inference helpers.
No LLM calls — purely deterministic logic.
"""
import pytest

from contracts.schemas import (
    SDETTestCase, SDETTestPlan, CoverageGap,
    TestPlan, TestType, Priority, RiskLevel,
)
from agents.strategist import StrategistAgent
from agents.designer import TestDesignerAgent


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_case(
    id: str = "TC-001",
    technique: str = "Equivalence Partitioning",
    type: str = "positive",
    priority: str = "P1",
) -> SDETTestCase:
    return SDETTestCase(
        id=id, title=f"Test {id}", requirement_ref="AC-1",
        type=type, technique=technique, priority=priority,
        risk_rationale="example",
        steps=["1. do thing"], expected_result="outcome visible",
    )


# ── SDETTestPlan.to_test_plan() ───────────────────────────────────────────────

class TestToTestPlanPriority:
    def test_p0_maps_correctly(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(priority="P0")])
        result = plan.to_test_plan()
        assert result.scenarios[0].priority == Priority.P0

    def test_p1_maps_correctly(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(priority="P1")])
        assert plan.to_test_plan().scenarios[0].priority == Priority.P1

    def test_p3_downcasts_to_p2(self):
        # No P3 in Priority enum — must map to P2
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(priority="P3")])
        assert plan.to_test_plan().scenarios[0].priority == Priority.P2

    def test_unknown_priority_defaults_to_p2(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(priority="UNKNOWN")])
        assert plan.to_test_plan().scenarios[0].priority == Priority.P2


class TestToTestPlanRiskLevel:
    def test_any_p0_yields_high_risk(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[
            _make_case("TC-001", priority="P2"),
            _make_case("TC-002", priority="P0"),
        ])
        assert plan.to_test_plan().risk_level == RiskLevel.HIGH

    def test_p1_without_p0_yields_medium(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[
            _make_case("TC-001", priority="P1"),
            _make_case("TC-002", priority="P2"),
        ])
        assert plan.to_test_plan().risk_level == RiskLevel.MEDIUM

    def test_all_p2_yields_low(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[
            _make_case("TC-001", priority="P2"),
            _make_case("TC-002", priority="P2"),
        ])
        assert plan.to_test_plan().risk_level == RiskLevel.LOW


class TestToTestPlanTypeMapping:
    def test_positive_maps_to_e2e(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(type="positive")])
        assert plan.to_test_plan().scenarios[0].type == TestType.E2E

    def test_concurrency_maps_to_integ(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(type="concurrency")])
        assert plan.to_test_plan().scenarios[0].type == TestType.INTEG

    def test_api_maps_to_api(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(type="api")])
        assert plan.to_test_plan().scenarios[0].type == TestType.API

    def test_unknown_type_defaults_to_e2e(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[_make_case(type="exotic")])
        assert plan.to_test_plan().scenarios[0].type == TestType.E2E


class TestToTestPlanSummary:
    def test_summary_lists_techniques(self):
        plan = SDETTestPlan(issue_number=5, test_cases=[
            _make_case("TC-001", technique="Boundary Value Analysis"),
            _make_case("TC-002", technique="Equivalence Partitioning"),
        ])
        summary = plan.to_test_plan().summary
        assert "Boundary Value Analysis" in summary or "Equivalence Partitioning" in summary

    def test_issue_number_preserved(self):
        plan = SDETTestPlan(issue_number=42, test_cases=[_make_case()])
        assert plan.to_test_plan().issue_number == 42

    def test_coverage_areas_deduped(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[
            _make_case("TC-001", type="positive"),
            _make_case("TC-002", type="positive"),  # duplicate type
            _make_case("TC-003", type="negative"),
        ])
        areas = plan.to_test_plan().coverage_areas
        assert areas.count("positive") == 1   # deduplicated


# ── AC extraction ─────────────────────────────────────────────────────────────

class TestACExtractionExplicitLabels:
    def test_parses_ac_n_labels(self):
        body = "AC-1: User can log in\nAC-2: Empty password shows error\nAC-3: Locked account message"
        acs = StrategistAgent._extract_acceptance_criteria(body)
        assert len(acs) == 3
        assert "AC-1" in acs
        assert "log in" in acs["AC-1"].lower()

    def test_case_insensitive(self):
        body = "ac-1: something works"
        acs = StrategistAgent._extract_acceptance_criteria(body)
        assert len(acs) >= 1

    def test_empty_body_returns_empty(self):
        assert StrategistAgent._extract_acceptance_criteria("") == {}

    def test_none_body_returns_empty(self):
        assert StrategistAgent._extract_acceptance_criteria(None) == {}


class TestACExtractionBulletSection:
    def test_acceptance_criteria_section(self):
        body = "## Acceptance Criteria:\n- First criterion\n- Second criterion\n- Third criterion"
        acs = StrategistAgent._extract_acceptance_criteria(body)
        assert len(acs) == 3
        assert "AC-1" in acs

    def test_prefers_explicit_labels_over_bullets(self):
        body = "AC-1: Explicit label\n## Acceptance Criteria:\n- Bullet one"
        acs = StrategistAgent._extract_acceptance_criteria(body)
        # Explicit labels take priority
        assert "AC-1" in acs
        assert acs["AC-1"] == "Explicit label"


# ── Bound inference ───────────────────────────────────────────────────────────

class TestBoundInference:
    def test_max_keyword(self):
        bounds = TestDesignerAgent._infer_bounds("Max 255 characters allowed")
        assert any("255" in v for v in bounds.values())

    def test_min_keyword(self):
        bounds = TestDesignerAgent._infer_bounds("Minimum 8 characters required")
        assert any("8" in v for v in bounds.values())

    def test_between_range(self):
        bounds = TestDesignerAgent._infer_bounds("Must be between 1 and 100 items")
        assert any("100" in v or "1" in v for v in bounds.values())

    def test_empty_body_returns_empty(self):
        assert TestDesignerAgent._infer_bounds("") == {}

    def test_no_numbers_returns_empty(self):
        assert TestDesignerAgent._infer_bounds("User should be able to log in") == {}


# ── TokenUsage ────────────────────────────────────────────────────────────────

class TestTokenUsage:
    def test_total(self):
        from agents.base import TokenUsage
        u = TokenUsage(input_tokens=100, output_tokens=50)
        assert u.total == 150

    def test_addition(self):
        from agents.base import TokenUsage
        a = TokenUsage(100, 50)
        b = TokenUsage(200, 75)
        c = a + b
        assert c.input_tokens == 300
        assert c.output_tokens == 125

    def test_cost_positive(self):
        from agents.base import TokenUsage
        u = TokenUsage(input_tokens=1_000_000, output_tokens=1_000_000)
        assert u.estimated_cost_usd > 0
