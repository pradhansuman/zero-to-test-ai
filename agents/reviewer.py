"""
agents/reviewer.py
──────────────────
QA Reviewer — audits the generated test suite against the test plan.

Sits between Generator and Runner. It is advisory-only: its verdict does NOT
gate the pipeline. The authoritative gate lives in ReporterAgent._gate(), which
is rule-based and operates on actual run results, not predicted quality.

The reviewer scores 8 quality dimensions (1–5) and emits a ReviewReport.
Coverage and correctness are weighted 2× in the weighted_total.
"""
from __future__ import annotations

import textwrap

from contracts.schemas import (
    GeneratedSuite, ReviewReport, DimensionScores, TestPlan,
)
from agents.base import Agent


_WEIGHTS = {
    "coverage": 2,
    "correctness": 2,
    "edge_negative": 1,
    "atomicity": 1,
    "reproducibility": 1,
    "traceability": 1,
    "non_redundancy": 1,
    "prioritization": 1,
}
_TOTAL_WEIGHT = sum(_WEIGHTS.values())  # 10


class ReviewerAgent(Agent):
    NAME = "reviewer"
    SYSTEM = textwrap.dedent("""\
        You are a QA reviewer auditing test-case quality. Do NOT rewrite the cases —
        score them and surface gaps.

        Score each dimension 1-5 (5 = excellent) with one line of evidence citing
        specific case IDs:
        - Coverage completeness — every AC + key risk area exercised, positive & negative.
        - Correctness — expected results are actually right for the stated input.
        - Edge & negative depth — boundaries, invalid input, error paths present.
        - Atomicity & independence — one behavior per case, no hidden ordering.
        - Reproducibility — concrete data + steps; a new tester could run it cold.
        - Traceability — each case maps to a requirement/AC.
        - Non-redundancy — no duplicated conditions inflating the count.
        - Prioritization — risk-aligned and justified.

        Respond with JSON only — no prose before or after.
        Use this exact shape:
        {
          "scores": {
            "coverage": <1-5>, "correctness": <1-5>, "edge_negative": <1-5>,
            "atomicity": <1-5>, "reproducibility": <1-5>, "traceability": <1-5>,
            "non_redundancy": <1-5>, "prioritization": <1-5>
          },
          "weighted_total": <float, max 5.0>,
          "critical_gaps": ["<gap>", ...],
          "redundant_cases": ["<TC-xxx duplicates TC-yyy>", ...],
          "verdict": "ship | revise | reject",
          "top_3_fixes": ["<fix>", "<fix>", "<fix>"]
        }
        weighted_total = (coverage*2 + correctness*2 + edge_negative + atomicity +
                          reproducibility + traceability + non_redundancy + prioritization) / 10
    """)

    def run(self, plan: TestPlan, suite: GeneratedSuite) -> ReviewReport:
        requirement_block = self._format_requirement(plan)
        test_cases_block  = self._format_test_cases(suite)

        prompt = (
            f"<requirement>\n{requirement_block}\n</requirement>\n\n"
            f"<test_cases>\n{test_cases_block}\n</test_cases>"
        )

        raw = self._complete_json(prompt, _RawReview, max_tokens=2000)

        # Always recompute weighted_total from parsed scores so it's trustworthy,
        # regardless of what the LLM calculated.
        s = raw.scores
        computed = (
            s.coverage        * _WEIGHTS["coverage"]
            + s.correctness   * _WEIGHTS["correctness"]
            + s.edge_negative * _WEIGHTS["edge_negative"]
            + s.atomicity     * _WEIGHTS["atomicity"]
            + s.reproducibility * _WEIGHTS["reproducibility"]
            + s.traceability  * _WEIGHTS["traceability"]
            + s.non_redundancy * _WEIGHTS["non_redundancy"]
            + s.prioritization * _WEIGHTS["prioritization"]
        ) / _TOTAL_WEIGHT

        report = ReviewReport(
            issue_number=plan.issue_number,
            scores=raw.scores,
            weighted_total=round(computed, 2),
            critical_gaps=raw.critical_gaps,
            redundant_cases=raw.redundant_cases,
            verdict=raw.verdict,
            top_3_fixes=raw.top_3_fixes,
        )
        print(
            f"[reviewer] verdict={report.verdict}  "
            f"weighted_total={report.weighted_total}/5.0  "
            f"gaps={len(report.critical_gaps)}"
        )
        return report

    # ── prompt formatters ────────────────────────────────────────────────────
    @staticmethod
    def _format_requirement(plan: TestPlan) -> str:
        lines = [
            f"Issue #{plan.issue_number}",
            f"Summary: {plan.summary}",
            f"Risk: {plan.risk_level.value} — {plan.risk_rationale}",
            f"Coverage areas: {', '.join(plan.coverage_areas)}",
            "",
            "Scenarios (acceptance criteria):",
        ]
        for sc in plan.scenarios:
            lines.append(
                f"  {sc.id}: [{sc.priority.value}/{sc.type.value}] {sc.name}\n"
                f"    Description: {sc.description}\n"
                f"    Expected: {sc.expected}"
            )
        return "\n".join(lines)

    @staticmethod
    def _format_test_cases(suite: GeneratedSuite) -> str:
        parts = []
        for f in suite.files:
            if "spec" in f.path:
                # Truncate very large specs so the prompt stays within budget.
                # 6000 chars ≈ ~1500 tokens — enough to assess structure + coverage.
                body = f.content if len(f.content) <= 6000 else f.content[:6000] + "\n... [truncated]"
                parts.append(f"// FILE: {f.path}\n{body}")
        return "\n\n".join(parts) if parts else "(no spec files found)"


# Internal parse target — we recompute weighted_total ourselves before
# constructing the public ReviewReport, so we parse into this looser model first.
from pydantic import BaseModel  # noqa: E402

class _RawReview(BaseModel):
    scores: DimensionScores
    weighted_total: float
    critical_gaps: list[str] = []
    redundant_cases: list[str] = []
    verdict: str
    top_3_fixes: list[str] = []
