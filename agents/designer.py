"""
agents/designer.py
──────────────────
STAGE 2 (alt) — Test Designer Agent.

A rigorous alternative to the StrategistAgent that applies six formal
test-design techniques to derive a complete, high-signal test suite. Prefer
this agent when the issue has explicit acceptance criteria, bounded numeric
inputs, multi-condition rules, or stateful UI flows.

The Designer works in two phases:
  Phase 1 — Acceptance Criteria Extraction:
      Parse the issue body to enumerate every AC, numbered AC-1…AC-N.
  Phase 2 — Technique-Driven Derivation:
      For each AC, apply the most appropriate technique(s) and derive
      atomic, independent, deterministic cases.

Every case carries technique attribution, a concrete `test_data` block,
and a one-line `risk_rationale` — enabling the downstream Reviewer to
score coverage and correctness with specificity.

Downstream compatibility: SDETTestPlan.to_test_plan() downcasts to the
standard TestPlan contract so the Generator, Runner, and Reporter are
entirely unchanged.

I/O CONTRACT
    in : IssuePayload
    out: SDETTestPlan
"""
from __future__ import annotations

import re
import textwrap

from agents.base import Agent
from contracts.schemas import IssuePayload, SDETTestPlan


class TestDesignerAgent(Agent):
    NAME = "designer"

    SYSTEM = textwrap.dedent("""\
        You are a Test Designer in an automated QA pipeline. Given a feature
        specification and pre-extracted acceptance criteria, derive a complete,
        high-signal test suite using formal test-design techniques.

        ── TECHNIQUE SELECTION GUIDE ────────────────────────────────────────────
        Apply the most productive technique(s) per AC:

        1. Equivalence Partitioning (EP)
           Use when: inputs fall into classes with uniform behaviour.
           Produce: exactly one representative per valid class AND one per invalid class.
           Never produce two cases from the same class.

        2. Boundary Value Analysis (BVA)
           Use when: any input has a defined minimum, maximum, or threshold.
           Produce: min−1, min, min+1, a nominal mid-range value, max−1, max, max+1.
           Flag min−1 and max+1 as "negative" type; the rest as "boundary".

        3. Decision Table (DT)
           Use when: a rule has ≥ 2 independent boolean or categorical conditions.
           Produce: one case per unique combination that yields a different outcome.
           Never produce the full Cartesian product — collapse equivalent rows.

        4. State Transition (ST)
           Use when: the feature moves through discrete states (e.g. unauthenticated →
           authenticated → session-expired).
           Produce: every valid transition, at least one invalid transition, and one
           self-loop where applicable.

        5. Pairwise / Orthogonal Array (PW)
           Use when: ≥ 3 independent parameters each have ≥ 2 values.
           Produce: pairwise coverage (every pair of parameter values appears at least
           once) — never the full Cartesian product.

        6. Error Guessing / Negative (EG)
           Use when: none of the above are dominant, or to supplement them.
           Produce cases for: null/empty/whitespace, type mismatch, oversized input,
           duplicate submission, out-of-order operations, special characters.

        ── COVERAGE DIMENSIONS — include where applicable ───────────────────────
        happy path · negative/invalid · boundary/edge
        security (authn, authz, injection, sensitive-data exposure, IDOR)
        error handling & recovery · idempotency & retries
        concurrency / race conditions · data integrity & persistence
        accessibility (UI: keyboard nav, ARIA, contrast) · observability (logs/metrics)

        ── QUALITY BAR ──────────────────────────────────────────────────────────
        • Every AC produces ≥ 1 positive AND ≥ 1 negative case. No exceptions.
        • Each case is atomic: tests exactly one behaviour.
        • Each case is independent: no ordering dependency on another case.
        • Each case is deterministic: one unambiguous expected result.
        • `test_data` is always concrete — never "valid input" or "some value".
        • `expected_result` is always observable and directly assertable.
        • No two cases cover the same condition.

        ── PRIORITY ─────────────────────────────────────────────────────────────
        P0: data loss · security vulnerability · complete workflow block
        P1: core feature degraded, workaround exists
        P2: partial/edge behaviour
        P3: cosmetic, localisation, minor UX

        ── OUTPUT FORMAT ────────────────────────────────────────────────────────
        Return ONLY a valid JSON object. No markdown, no prose.

        {
          "issue_number": <int>,
          "test_cases": [
            {
              "id": "TC-001",
              "title": "<precise, unique title>",
              "requirement_ref": "AC-1",
              "type": "positive|negative|boundary|security|state|concurrency|idempotency|accessibility|observability",
              "technique": "Equivalence Partitioning|Boundary Value Analysis|Decision Table|State Transition|Pairwise|Error Guessing / Negative",
              "priority": "P0|P1|P2|P3",
              "risk_rationale": "<one sentence: what breaks and who is affected>",
              "preconditions": ["<observable system state before the test>"],
              "test_data": {"<field>": "<concrete literal value>"},
              "steps": ["1. <concrete action>", "2. <concrete action>"],
              "expected_result": "<single, assertable, observable outcome>"
            }
          ],
          "coverage_gaps": [
            {
              "requirement_ref": "AC-2",
              "reason": "<why a case could not be derived — spec ambiguous, out-of-scope, etc.>"
            }
          ]
        }
    """)

    def run(self, issue: IssuePayload) -> SDETTestPlan:
        acs = self._extract_acceptance_criteria(issue.body)
        requirement_block = self._format_requirement(issue, acs)
        context_block     = self._format_context(issue)

        prompt = (
            f"<requirement>\n{requirement_block}\n</requirement>\n\n"
            f"<context>\n{context_block}\n</context>"
        )

        # 20-40 detailed cases × ~150 tokens each → 6 000 token budget
        plan = self._complete_json(prompt, SDETTestPlan, max_tokens=6000)
        plan.issue_number = issue.issue_number

        p0s  = sum(1 for t in plan.test_cases if t.priority == "P0")
        techniques = sorted({t.technique for t in plan.test_cases})
        print(
            f"[designer] {len(plan.test_cases)} cases  "
            f"P0={p0s}  gaps={len(plan.coverage_gaps)}\n"
            f"           techniques: {', '.join(techniques)}"
        )
        return plan

    # ── prompt construction ──────────────────────────────────────────────────
    @staticmethod
    def _format_requirement(issue: IssuePayload, acs: dict[str, str]) -> str:
        lines = [
            f"Issue #{issue.issue_number} — {issue.title}",
            f"Repository : {issue.repo}",
            f"Type       : {issue.type}",
            f"Priority   : {issue.priority.value}",
        ]
        if issue.component:
            lines.append(f"Component  : {issue.component}")
        if issue.labels:
            lines.append(f"Labels     : {', '.join(issue.labels)}")

        lines.append("")
        if acs:
            lines.append("Acceptance Criteria (pre-extracted — derive cases for each):")
            for ref, text in acs.items():
                lines.append(f"  {ref}: {text}")
        else:
            lines.append("Acceptance Criteria: (none explicit — infer from title and body)")

        if issue.body.strip():
            lines += ["", "Full issue body:", issue.body.strip()]

        return "\n".join(lines)

    @staticmethod
    def _format_context(issue: IssuePayload) -> str:
        component = issue.component or "UI"
        label_lower = {lbl.lower() for lbl in issue.labels}

        # Infer security/auth constraints
        constraints: list[str] = []
        if any(k in label_lower for k in ("auth", "login", "jwt", "oauth", "session")):
            constraints.append("authentication / session management in scope")
        if any(k in label_lower for k in ("rate-limit", "throttle", "quota")):
            constraints.append("rate limiting applies — test both within and beyond the limit")
        if any(k in label_lower for k in ("api", "rest", "graphql", "webhook")):
            constraints.append("REST/JSON API — include malformed-payload and missing-header cases")
        if any(k in label_lower for k in ("payment", "checkout", "billing")):
            constraints.append("financial data — idempotency and data-integrity cases are P0")
        if issue.priority.value == "P0":
            constraints.append("SLA: any downtime is a P0 incident — recovery cases required")
        if not constraints:
            constraints.append("no elevated auth, rate-limit, or financial constraints identified")

        # Infer input boundaries from issue body
        bounds = TestDesignerAgent._infer_bounds(issue.body)
        bounds_block = (
            "Detected input boundaries (apply BVA):\n"
            + "\n".join(f"  {k}: {v}" for k, v in bounds.items())
            if bounds else ""
        )

        return "\n".join(filter(None, [
            f"- Component  : {component}",
            f"- Constraints: {'; '.join(constraints)}",
            "- Out of scope: performance/load testing, third-party integrations "
            "unless directly referenced in the issue body",
            bounds_block,
        ]))

    # ── helpers ──────────────────────────────────────────────────────────────
    @staticmethod
    def _extract_acceptance_criteria(body: str) -> dict[str, str]:
        """
        Parse common AC patterns from issue body before sending to the LLM,
        so the LLM doesn't have to re-parse prose — it can focus on derivation.

        Recognised patterns (in order of priority):
          1. Explicit "AC-N:" labels
          2. "Acceptance Criteria:" section with bullet points
          3. Gherkin "Given … When … Then" blocks
        """
        if not body:
            return {}
        acs: dict[str, str] = {}

        # Pattern 1: explicit AC-N labels anywhere in the body
        for m in re.finditer(
            r"\bAC-?(\d+)\b[:\s]+(.+?)(?=\bAC-?\d+\b|$)", body,
            re.IGNORECASE | re.DOTALL,
        ):
            text = m.group(2).strip().split("\n")[0].strip()
            if text:
                acs[f"AC-{m.group(1)}"] = text

        if acs:
            return acs

        # Pattern 2: "Acceptance Criteria:" / "Acceptance criteria" section
        ac_section = re.search(
            r"(?:acceptance criteria|ac)[:\s]*\n((?:\s*[-*\d.]\s*.+\n?)+)",
            body, re.IGNORECASE,
        )
        if ac_section:
            bullets = re.findall(r"[-*\d.]\s*(.+)", ac_section.group(1))
            for i, b in enumerate(bullets, 1):
                acs[f"AC-{i}"] = b.strip()
            if acs:
                return acs

        # Pattern 3: Gherkin Given/When/Then
        for i, m in enumerate(
            re.finditer(
                r"(Given\s+.+?)(?=Given\s|$)", body, re.IGNORECASE | re.DOTALL
            ),
            start=1,
        ):
            snippet = m.group(0).strip().replace("\n", " ")
            acs[f"AC-{i}"] = snippet[:150]

        return acs

    @staticmethod
    def _infer_bounds(body: str) -> dict[str, str]:
        """
        Extract numeric boundaries mentioned in the issue body so BVA cases
        can be grounded in real spec values rather than invented ones.
        e.g. "max 255 characters" → {"max_length": "255"}
        """
        bounds: dict[str, str] = {}
        patterns = [
            (r"(?:max(?:imum)?|up to|no more than)\s+(\d+)\s+(\w+)", "max_{1}"),
            (r"(?:min(?:imum)?|at least)\s+(\d+)\s+(\w+)",            "min_{1}"),
            (r"between\s+(\d+)\s+and\s+(\d+)\s+(\w+)",               "range_{2}"),
            (r"(\d+)\s*[-–]\s*(\d+)\s+(\w+)",                        "range_{2}"),
        ]
        for pat, label_template in patterns:
            for m in re.finditer(pat, body, re.IGNORECASE):
                groups = m.groups()
                label = label_template.format(*groups)
                bounds[label] = m.group(0).strip()
        return bounds
