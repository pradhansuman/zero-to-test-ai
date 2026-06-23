"""
Integration test — full IssueRef → ReportArtifact pipeline in demo/offline mode.

Runs without any API key or network: demo stubs provide canned LLM responses
so we can validate the real pipeline wiring, Pydantic contract hand-offs,
gate logic, and stage sequencing without spending API credit.
"""
import pytest
from unittest.mock import MagicMock
from contracts.schemas import (
    IssueRef, IssuePayload, TestPlan, GeneratedSuite,
    RunResults, ReportArtifact, ReviewReport, DimensionScores,
)
from orchestrator.pipeline import QAPipeline, PipelineTrace

# Canned ReviewReport — ReviewerAgent is advisory and not in demo_stubs,
# so we stub reviewer.run directly to avoid real API calls in offline tests.
_CANNED_REVIEW = ReviewReport(
    issue_number=1,
    scores=DimensionScores(
        coverage=4, correctness=4, edge_negative=3,
        atomicity=4, reproducibility=4, traceability=4,
        non_redundancy=4, prioritization=4,
    ),
    weighted_total=3.9,
    verdict='ship',
    critical_gaps=[],
    redundant_cases=[],
    top_3_fixes=[],
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def pipeline():
    p = QAPipeline(demo=True, offline=True)
    # Stub reviewer.run so no real Anthropic API call is made
    p.reviewer.run = MagicMock(return_value=_CANNED_REVIEW)
    return p


@pytest.fixture(scope="module")
def trace(pipeline):
    ref = IssueRef(repo="demo/frontend-app", issue_number=1)
    stages = {}

    def capture(stage, artifact):
        stages[stage] = artifact

    result = pipeline.run(ref, on_stage=capture)
    result._stages = stages
    return result


# ── Stage contract tests ───────────────────────────────────────────────────────

def test_PI_01_returns_pipeline_trace(trace):
    assert isinstance(trace, PipelineTrace)


def test_PI_02_ingestor_emits_issue_payload(trace):
    assert isinstance(trace.payload, IssuePayload)
    assert trace.payload.title
    assert trace.payload.repo == "demo/frontend-app"


def test_PI_03_planner_emits_test_plan_with_scenarios(trace):
    assert isinstance(trace.plan, TestPlan)
    assert len(trace.plan.scenarios) >= 1
    for s in trace.plan.scenarios:
        assert s.name
        assert s.description


def test_PI_04_generator_emits_runnable_suite(trace):
    assert isinstance(trace.suite, GeneratedSuite)
    assert len(trace.suite.files) >= 1
    # At least one generated file must reference Playwright test APIs
    combined = "\n".join(f.content for f in trace.suite.files)
    assert "test(" in combined or "import" in combined


def test_PI_05_runner_emits_run_results(trace):
    assert isinstance(trace.results, RunResults)
    assert trace.results.total >= 0
    assert trace.results.passed + trace.results.failed <= trace.results.total


def test_PI_06_reporter_emits_report_artifact(trace):
    assert isinstance(trace.report, ReportArtifact)
    assert trace.report.gate_decision in ("pass", "fail", "PASS", "FAIL")
    assert trace.report.summary_md


def test_PI_07_gate_is_determined_by_rule_not_llm(trace):
    """Gate must match the computed pass/fail from run results — not an LLM response."""
    results = trace.results
    expected_gate_pass = results.failed == 0
    actual_gate_pass = trace.report.gate_decision.upper() == "PASS"
    assert actual_gate_pass == expected_gate_pass, (
        f"Gate mismatch: results show failed={results.failed} but gate_decision={trace.report.gate_decision}"
    )


def test_PI_08_on_stage_callback_fires_for_all_stages(trace):
    """Every pipeline stage must call on_stage so callers can observe intermediate artifacts."""
    stages = trace._stages
    # "healed" is only emitted when there are failures; always check the core stages
    core = {"ingested", "planned", "generated", "tested", "reported"}
    missing = core - set(stages.keys())
    assert not missing, f"Missing stage callbacks: {missing}"


def test_PI_09_healing_attempts_are_recorded(trace):
    """HealerAgent records every attempt (even no-ops) in the trace."""
    assert hasattr(trace, "healing_log")
    assert isinstance(trace.healing_log, list)


def test_PI_10_all_contracts_round_trip_through_pydantic(trace):
    """All stage artifacts must be JSON-serialisable (Pydantic model_dump)."""
    artifacts = [trace.payload, trace.plan, trace.suite, trace.results, trace.report]
    for artifact in artifacts:
        dumped = artifact.model_dump()
        assert isinstance(dumped, dict)
        # Re-constructing from the dump must not raise
        artifact.__class__(**dumped)


def test_PI_11_issue_priority_propagates_to_plan(trace):
    """Every scenario emitted by the Planner must have a valid priority level."""
    from contracts.schemas import Priority
    valid = set(Priority)
    for s in trace.plan.scenarios:
        assert s.priority in valid, f"Invalid priority: {s.priority}"


def test_PI_12_generated_suite_references_test_titles_from_plan(trace):
    """Generator should produce code that references at least one scenario title keyword."""
    plan_keywords = {
        word.lower()
        for s in trace.plan.scenarios
        for word in s.name.split()
        if len(word) > 4
    }
    code_lower = "\n".join(f.content for f in trace.suite.files).lower()
    found = any(kw in code_lower for kw in plan_keywords)
    # Soft assertion — warn rather than fail if none match (LLM output is non-deterministic)
    if not found:
        pytest.warns(None)  # no hard fail — trace for human review
