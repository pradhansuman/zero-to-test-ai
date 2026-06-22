"""
tests/unit/test_gate.py
────────────────────────
Unit tests for ReporterAgent._gate() — the CI merge gate.

This is the most critical test in the suite: a bug here silently approves
broken PRs or silently blocks valid ones. All logic is rule-based (no LLM),
so every branch can be exercised without an API key.

Gate policy:
  FAIL if any P0 test failed OR pass_rate < 90.0
  PASS otherwise
"""
import pytest

from contracts.schemas import RunResults, TestResult, TestType, Priority
from agents.reporter import ReporterAgent


def _make_results(
    specs: list[tuple[bool, str]],   # (passed, priority)
    total_duration_ms: int = 1000,
) -> RunResults:
    """Build a RunResults from (passed, priority) tuples."""
    results = [
        TestResult(
            id=f"TC-{i+1:03}", name=f"test {i+1}",
            type=TestType.E2E,
            priority=Priority[p],
            passed=passed,
            duration_ms=100,
        )
        for i, (passed, p) in enumerate(specs)
    ]
    total  = len(results)
    passed = sum(1 for r in results if r.passed)
    return RunResults(
        issue_number=1,
        results=results,
        total=total,
        passed=passed,
        failed=total - passed,
        pass_rate=round(passed / total * 100, 1) if total else 0.0,
        total_duration_ms=total_duration_ms,
    )


class TestGatePolicyP0:
    def test_single_p0_failure_blocks(self):
        run = _make_results([(False, "P0"), (True, "P1"), (True, "P2")])
        assert ReporterAgent._gate(run) == "FAIL"

    def test_p0_pass_does_not_block_by_itself(self):
        run = _make_results([(True, "P0"), (True, "P1")])
        assert ReporterAgent._gate(run) == "PASS"

    def test_multiple_p0_all_passing(self):
        run = _make_results([(True, "P0"), (True, "P0"), (True, "P1")])
        assert ReporterAgent._gate(run) == "PASS"

    def test_p1_failure_alone_does_not_block_if_rate_above_90(self):
        # 10 tests, 1 P1 failure → 90% pass rate → boundary case
        specs = [(True, "P1")] * 9 + [(False, "P1")]
        run = _make_results(specs)
        assert run.pass_rate == 90.0
        assert ReporterAgent._gate(run) == "PASS"

    def test_p0_failure_blocks_even_at_100_percent_rate(self):
        # Impossible in real usage (all pass + P0 fail), but tests gate priority
        run = _make_results([(True, "P1"), (True, "P2")])
        # Manually inject a P0 failure
        run.results.append(
            TestResult(id="TC-X", name="injected", type=TestType.E2E,
                       priority=Priority.P0, passed=False, duration_ms=0)
        )
        run.failed = 1
        assert ReporterAgent._gate(run) == "FAIL"


class TestGatePolicyPassRate:
    def test_exactly_90_passes(self):
        specs = [(True, "P2")] * 9 + [(False, "P2")]
        run = _make_results(specs)
        assert run.pass_rate == 90.0
        assert ReporterAgent._gate(run) == "PASS"

    def test_89_point_9_fails(self):
        # 9/10 = 90.0, need fewer passes — use 8/9 = 88.9%
        specs = [(True, "P2")] * 8 + [(False, "P2")]
        run = _make_results(specs)
        assert run.pass_rate < 90.0
        assert ReporterAgent._gate(run) == "FAIL"

    def test_100_percent_passes(self):
        run = _make_results([(True, "P1"), (True, "P2"), (True, "P0")])
        assert run.pass_rate == 100.0
        assert ReporterAgent._gate(run) == "PASS"

    def test_zero_tests_is_fail(self):
        run = RunResults(
            issue_number=1, results=[], total=0,
            passed=0, failed=0, pass_rate=0.0, total_duration_ms=0,
        )
        assert ReporterAgent._gate(run) == "FAIL"

    def test_all_failed_is_fail(self):
        run = _make_results([(False, "P1"), (False, "P2"), (False, "P2")])
        assert ReporterAgent._gate(run) == "FAIL"


class TestGateCombined:
    def test_p0_fail_overrides_high_pass_rate(self):
        # 99 pass, 1 P0 fail — pass_rate is 99% but still FAIL
        specs = [(True, "P2")] * 99 + [(False, "P0")]
        run = _make_results(specs)
        assert run.pass_rate == 99.0
        assert ReporterAgent._gate(run) == "FAIL"

    def test_low_rate_and_p0_fail_both_bad(self):
        specs = [(False, "P0"), (False, "P1"), (True, "P2")]
        run = _make_results(specs)
        assert ReporterAgent._gate(run) == "FAIL"
