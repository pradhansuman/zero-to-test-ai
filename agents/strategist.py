"""
agents/strategist.py
─────────────────────
STAGE 2 — Test Strategist Agent.

Determines *what* to test by reasoning about risk, acceptance criteria, and
coverage strategy before producing scenarios. Enforces a minimum coverage
guarantee: every acceptance criterion in the issue gets at least one positive
AND one negative case.

Replaces the former PlannerAgent with a structured three-phase approach:
  Phase 1 — Risk Assessment: identify the highest-consequence failure modes.
  Phase 2 — AC Mapping: extract acceptance criteria from the issue body.
  Phase 3 — Scenario Derivation: produce 5-10 atomic, prioritised scenarios.

I/O CONTRACT
    in : IssuePayload
    out: TestPlan
"""
from __future__ import annotations

import re

from agents.base import Agent
from contracts.schemas import IssuePayload, TestPlan


class StrategistAgent(Agent):
    NAME = "strategist"

    SYSTEM = """\
You are a Test Strategist in an automated QA pipeline. Your role is to reason
about risk and acceptance criteria before deciding what to test — never write
test code here.

PHASE 1 — RISK ASSESSMENT
Identify the two or three highest-consequence failure modes for this issue. A
failure mode is a specific observable breakage, not a vague category. Rank by:
  (a) user impact — does it block a core workflow or lose data?
  (b) likelihood — how easy is it to trigger?
  (c) detectability — would it be caught without automated tests?

PHASE 2 — ACCEPTANCE-CRITERIA MAPPING
Extract all acceptance criteria (ACs) stated or implied in the issue body.
Label them AC-1, AC-2, … If none are explicit, infer them from the title and
description. Every AC must produce at least one positive AND one negative scenario.

PHASE 3 — SCENARIO DERIVATION
Produce 5–10 concrete scenarios from the risk analysis and AC list. Rules:
- Mix coverage types: happy path, negative/invalid, boundary/edge, security,
  state transition. Do not produce only happy paths.
- Each step is a concrete, executable action ("fill the numerator field with 7"),
  not an abstraction ("enter valid input").
- `expected` is one assertable outcome the Generator can turn into a single
  expect() call — no compound assertions.
- Escalate priority independently of the issue label when a scenario implies
  data loss, auth bypass, or irreversible side effects.
- P0: data loss / security / complete workflow block.
  P1: core feature degraded, workaround exists.
  P2: partial/edge behaviour, cosmetic.

Return ONLY valid JSON — no markdown, no prose before or after:
{
  "issue_number": <int>,
  "summary": "<one-line description of what is being tested and why>",
  "test_approach": "<strategic stance, e.g. 'risk-first AC-coverage matrix targeting auth boundary'>",
  "scenarios": [
    {
      "id": "TC-001",
      "name": "<concise name>",
      "type": "e2e|unit|api|integ",
      "priority": "P0|P1|P2",
      "coverage_type": "happy|negative|boundary|security|state|concurrency",
      "requirement_ref": "AC-1",
      "description": "<what behaviour this verifies and why it matters>",
      "steps": ["1. <concrete action>", "2. <concrete action>"],
      "expected": "<single assertable outcome>"
    }
  ],
  "coverage_areas": ["area1", "area2"],
  "risk_level": "high|medium|low",
  "risk_rationale": "<one sentence linking the highest-risk scenario to user impact>"
}"""

    def run(self, issue: IssuePayload) -> TestPlan:
        acs = self._extract_acceptance_criteria(issue.body)
        ac_block = (
            "\n".join(f"  {k}: {v}" for k, v in acs.items())
            if acs else "  (none explicit — infer from title and description)"
        )

        prompt = (
            f"Issue #{issue.issue_number} ({issue.repo})\n"
            f"Title: {issue.title}\n"
            f"Labels: {', '.join(issue.labels) or 'none'}\n"
            f"Priority: {issue.priority.value}  "
            f"Type: {issue.type}  "
            f"Component: {issue.component or 'n/a'}\n\n"
            f"Extracted acceptance criteria:\n{ac_block}\n\n"
            f"Full issue body:\n{issue.body}\n"
        )

        plan = self._complete_json(prompt, TestPlan, max_tokens=3000)
        plan.issue_number = issue.issue_number

        pos = sum(1 for s in plan.scenarios if s.coverage_type == "happy")
        neg = sum(1 for s in plan.scenarios
                  if s.coverage_type in ("negative", "boundary", "security"))
        print(
            f"[strategist] {len(plan.scenarios)} scenarios  "
            f"positive={pos}  negative/boundary/security={neg}  "
            f"risk={plan.risk_level.value}"
        )
        return plan

    # ── pre-processing ───────────────────────────────────────────────────────
    @staticmethod
    def _extract_acceptance_criteria(body: str) -> dict[str, str]:
        """
        Pull explicit ACs from common issue-body patterns before sending to the LLM.
        Returns {"AC-1": "text", "AC-2": "text", …} or {} if none found.
        Patterns recognised:
          - "[ ] AC-1: ..."  (GitHub checkbox)
          - "**AC-1** ..."
          - "- Given ... When ... Then ..."
          - "Acceptance Criteria:" followed by bullet lines
        """
        acs: dict[str, str] = {}
        if not body:
            return acs

        # Pattern 1: explicit AC-N labels
        for m in re.finditer(
            r"(?:AC-?(\d+))[:\s]+(.+?)(?=AC-?\d+|$)", body, re.IGNORECASE | re.DOTALL
        ):
            key = f"AC-{m.group(1)}"
            text = m.group(2).strip().split("\n")[0].strip()
            if text:
                acs[key] = text

        if acs:
            return acs

        # Pattern 2: "Acceptance Criteria:" section with bullet points
        ac_section = re.search(
            r"acceptance criteria[:\s]*\n((?:[-*]\s*.+\n?)+)", body, re.IGNORECASE
        )
        if ac_section:
            bullets = re.findall(r"[-*]\s*(.+)", ac_section.group(1))
            for i, bullet in enumerate(bullets, start=1):
                acs[f"AC-{i}"] = bullet.strip()

        # Pattern 3: Gherkin Given/When/Then blocks
        if not acs:
            for i, m in enumerate(
                re.finditer(r"Given\s+(.+?)(?=Given|$)", body, re.IGNORECASE | re.DOTALL),
                start=1,
            ):
                acs[f"AC-{i}"] = m.group(0).strip().replace("\n", " ")[:120]

        return acs
