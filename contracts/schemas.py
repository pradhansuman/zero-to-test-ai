"""
contracts/schemas.py
─────────────────────
The typed I/O contract for every agent in the AI-Assisted QA pipeline.

Each agent declares exactly what it consumes and what it emits. These models
are the *only* thing agents share — no agent reaches into another's internals.
This is what makes the pipeline composable: any stage can be swapped, mocked,
or re-run in isolation as long as it honours the contract.

    IssueRef ─▶ [Ingestor]  ─▶ IssuePayload
    IssuePayload ─▶ [Planner]   ─▶ TestPlan
    TestPlan ─▶ [Generator] ─▶ GeneratedSuite
    (TestPlan + GeneratedSuite) ─▶ [Reviewer] ─▶ ReviewReport (advisory)
    GeneratedSuite ─▶ [Runner]   ─▶ RunResults
    RunResults ─▶ [Reporter]  ─▶ ReportArtifact
"""
from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ─────────────────────────── shared enums ───────────────────────────
class Priority(str, Enum):
    P0 = "P0"   # critical — blocks release
    P1 = "P1"   # high — must fix this sprint
    P2 = "P2"   # medium — backlog


class TestType(str, Enum):
    E2E = "e2e"
    UNIT = "unit"
    API = "api"
    INTEG = "integ"


class RiskLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ─────────────── stage 1 — GitHub Issue Ingestion ───────────────
class IssueRef(BaseModel):
    """INPUT to the Ingestor — a pointer to a real GitHub issue."""
    repo: str = Field(..., description="owner/name, e.g. 'mui/material-ui'")
    issue_number: int
    github_token: Optional[str] = Field(
        None, description="PAT for private repos / higher rate limits"
    )


class IssuePayload(BaseModel):
    """OUTPUT of the Ingestor — normalised, agent-ready issue object."""
    issue_number: int
    repo: str
    state: str
    title: str
    body: str
    labels: list[str] = []
    priority: Priority = Priority.P2
    type: str = "bug"                 # bug | feature | chore
    component: Optional[str] = None
    milestone: Optional[str] = None
    author: Optional[str] = None
    comments_count: int = 0
    url: str = ""
    pipeline_stage: str = "ingested"
    ready_for_planner: bool = True


# ─────────────── stage 2 — Strategist / TestDesigner Agent ─────────────────
class TestScenario(BaseModel):
    id: str = Field(..., description="TC-001, TC-002, ...")
    name: str
    type: TestType
    priority: Priority
    description: str
    steps: list[str]
    expected: str
    # enriched fields — optional for backward compat, populated by StrategistAgent
    coverage_type: Optional[str] = Field(
        None, description="happy | negative | boundary | security | state | concurrency"
    )
    requirement_ref: Optional[str] = Field(
        None, description="AC-1, AC-2, … — which acceptance criterion this covers"
    )


class TestPlan(BaseModel):
    """OUTPUT of the Strategist — a structured, risk-prioritised test plan."""
    issue_number: int
    summary: str
    scenarios: list[TestScenario]
    coverage_areas: list[str]
    risk_level: RiskLevel
    risk_rationale: str
    test_approach: Optional[str] = Field(
        None, description="strategic stance, e.g. 'risk-first AC-coverage matrix'"
    )


# ─────────────── stage 3 — Generator Agent ───────────────
class BrowserTarget(str, Enum):
    """
    Which browser environments to run the generated suite against.
    All options use Playwright's bundled browsers — no paid service required.

    CHROMIUM_DESKTOP  desktop Chrome (1280×720)           — always included
    CHROMIUM_MOBILE   Chrome on Pixel 7 (412×915, touch)  — free, fast
    WEBKIT_MOBILE     Safari engine on iPhone 14 (390×844) — catches iOS bugs
    FIREFOX_DESKTOP   desktop Firefox                     — cross-browser parity
    TABLET_CHROME     Chrome on iPad Pro 11 (834×1194)    — tablet breakpoint
    """
    CHROMIUM_DESKTOP = "chromium-desktop"
    CHROMIUM_MOBILE  = "chromium-mobile"
    WEBKIT_MOBILE    = "webkit-mobile"
    FIREFOX_DESKTOP  = "firefox-desktop"
    TABLET_CHROME    = "tablet-chrome"


# Maps BrowserTarget → (project name, Playwright device key)
BROWSER_DEVICE_MAP: dict[BrowserTarget, tuple[str, str]] = {
    BrowserTarget.CHROMIUM_DESKTOP: ("Desktop Chrome",   "Desktop Chrome"),
    BrowserTarget.CHROMIUM_MOBILE:  ("Mobile Chrome",    "Pixel 7"),
    BrowserTarget.WEBKIT_MOBILE:    ("Mobile Safari",    "iPhone 14"),
    BrowserTarget.FIREFOX_DESKTOP:  ("Desktop Firefox",  "Desktop Firefox"),
    BrowserTarget.TABLET_CHROME:    ("Tablet Chrome",    "iPad Pro 11"),
}


class GeneratedFile(BaseModel):
    path: str = Field(..., description="relative path, e.g. tests/e2e/login.spec.ts")
    language: str = "typescript"
    content: str
    covers: list[str] = Field(default_factory=list, description="TC ids covered")


class GeneratedSuite(BaseModel):
    """OUTPUT of the Generator — runnable test files + browser targets."""
    issue_number: int
    files: list[GeneratedFile]
    framework: str = "playwright"
    total_tests: int = 0
    notes: Optional[str] = None
    browser_targets: list[BrowserTarget] = Field(
        default_factory=lambda: [BrowserTarget.CHROMIUM_DESKTOP],
        description="Which browser environments to execute this suite against",
    )


# ─────────────── stage 2 (alt) — SDET Agent ───────────────
class SDETTestCase(BaseModel):
    """One atomic test case derived by a formal test-design technique."""
    id: str                  # TC-001
    title: str
    requirement_ref: str     # AC-1, AC-2, …
    type: str                # positive|negative|boundary|security|state|concurrency|…
    technique: str           # Equivalence Partitioning | Boundary Value Analysis | …
    priority: str            # P0–P3
    risk_rationale: str
    preconditions: list[str] = Field(default_factory=list)
    test_data: dict          = Field(default_factory=dict)
    steps: list[str]         = Field(default_factory=list)
    expected_result: str


class CoverageGap(BaseModel):
    requirement_ref: str
    reason: str


class SDETTestPlan(BaseModel):
    """OUTPUT of the SDETAgent — richer than TestPlan; includes technique attribution,
    concrete test_data, and a coverage-gap manifest."""
    issue_number: int
    test_cases: list[SDETTestCase]
    coverage_gaps: list[CoverageGap] = Field(default_factory=list)

    def to_test_plan(self) -> "TestPlan":
        """Downcast to the standard TestPlan so the downstream Generator is unchanged."""
        _type_map = {
            "positive": TestType.E2E, "negative": TestType.E2E,
            "boundary": TestType.E2E, "security": TestType.E2E,
            "state": TestType.E2E,    "concurrency": TestType.INTEG,
            "api": TestType.API,      "integ": TestType.INTEG,
            "idempotency": TestType.INTEG, "accessibility": TestType.E2E,
            "responsive": TestType.E2E,    "localization": TestType.E2E,
            "observability": TestType.INTEG,
        }
        _pri_map = {
            "P0": Priority.P0, "P1": Priority.P1,
            "P2": Priority.P2, "P3": Priority.P2,  # P3 → P2, no P3 in enum
        }

        scenarios: list["TestScenario"] = []
        for tc in self.test_cases:
            desc = f"[{tc.technique}] {tc.title}. Risk: {tc.risk_rationale}"
            scenarios.append(TestScenario(
                id=tc.id,
                name=tc.title,
                type=_type_map.get(tc.type.split("/")[0].lower(), TestType.E2E),
                priority=_pri_map.get(tc.priority, Priority.P2),
                description=desc,
                steps=tc.steps or [f"Test data: {tc.test_data}"],
                expected=tc.expected_result,
            ))

        priorities = {tc.priority for tc in self.test_cases}
        risk = (RiskLevel.HIGH if "P0" in priorities
                else RiskLevel.MEDIUM if "P1" in priorities
                else RiskLevel.LOW)

        techniques = sorted({tc.technique for tc in self.test_cases})
        types      = sorted({tc.type      for tc in self.test_cases})
        return TestPlan(
            issue_number=self.issue_number,
            summary=(
                f"SDET-derived plan: {len(self.test_cases)} cases via "
                f"{', '.join(techniques[:3])}{'…' if len(techniques) > 3 else ''}"
            ),
            scenarios=scenarios,
            coverage_areas=list(dict.fromkeys(types)),  # order-preserving dedup
            risk_level=risk,
            risk_rationale=(
                f"{len([t for t in self.test_cases if t.priority=='P0'])} P0 cases; "
                f"{len(self.coverage_gaps)} coverage gap(s) noted by SDET agent"
            ),
        )


# ─────────────── stage 3.5 — Reviewer Agent ───────────────
class DimensionScores(BaseModel):
    """Per-dimension quality scores, each 1 (poor) – 5 (excellent)."""
    coverage:        int = Field(..., ge=1, le=5, description="Every AC + key risk area exercised")
    correctness:     int = Field(..., ge=1, le=5, description="Expected results actually match stated input")
    edge_negative:   int = Field(..., ge=1, le=5, description="Boundaries, invalid input, error paths present")
    atomicity:       int = Field(..., ge=1, le=5, description="One behaviour per case, no hidden ordering")
    reproducibility: int = Field(..., ge=1, le=5, description="Concrete data + steps; runnable cold")
    traceability:    int = Field(..., ge=1, le=5, description="Each case maps to a requirement/AC")
    non_redundancy:  int = Field(..., ge=1, le=5, description="No duplicated conditions inflating the count")
    prioritization:  int = Field(..., ge=1, le=5, description="Risk-aligned and justified")


class ReviewReport(BaseModel):
    """OUTPUT of the Reviewer — advisory quality audit of the generated test suite."""
    issue_number: int
    scores: DimensionScores
    weighted_total: float = Field(
        ...,
        description="(coverage*2 + correctness*2 + rest*1) / 10 — max 5.0",
    )
    critical_gaps:    list[str] = Field(default_factory=list)
    redundant_cases:  list[str] = Field(default_factory=list)
    verdict: str = Field(..., description="ship | revise | reject")
    top_3_fixes: list[str] = Field(default_factory=list)


# ─────────────── stage 4 — Test Runner (Layers) ───────────────
class TestResult(BaseModel):
    id: str
    name: str
    type: TestType
    priority: Priority
    passed: bool
    duration_ms: int
    retries: int = 0
    error: Optional[str] = None


class RunResults(BaseModel):
    """OUTPUT of the Runner — per-test results + roll-up."""
    issue_number: int
    results: list[TestResult]
    total: int
    passed: int
    failed: int
    pass_rate: float
    total_duration_ms: int
    browsers: list[str] = ["chromium"]


# ─────────────── stage 5 — Reporter Agent ───────────────
class ReportArtifact(BaseModel):
    """OUTPUT of the Reporter — the human-facing summary."""
    issue_number: int
    headline: str
    summary_md: str
    pass_rate: float
    allure_path: str = "allure-report/index.html"
    gate_decision: str = Field(..., description="PASS | FAIL — CI merge gate")
    issue_comment: str = Field(..., description="markdown posted back to the GH issue")
    healed: int = 0          # tests recovered by the Healer before reporting
    self_healing_log: list["HealingAttempt"] = Field(default_factory=list)


# ─────────────── stage 4.5 — Self-Healing Agent ───────────────
class FailureKind(str, Enum):
    LOCATOR = "locator"        # element not found / not visible — healable
    ASSERTION = "assertion"    # logic wrong — NOT healable, this is a real bug
    ENVIRONMENT = "environment" # infra/browser launch/network reset — NOT healable, re-run pipeline
    FLAKY = "flaky"            # passed on Playwright retry — quarantine candidate
    TIMEOUT = "timeout"        # pure wait exhaustion — may be flaky, retry once
    OTHER = "other"


class HealingAttempt(BaseModel):
    """One self-heal cycle on one failing test."""
    test_id: str
    failure_kind: FailureKind
    healable: bool
    old_selector: Optional[str] = None
    new_selector: Optional[str] = None
    rationale: Optional[str] = None        # why Claude chose the new selector
    confidence: float = 0.0                # 0–1, from the Healer
    rerun_passed: Optional[bool] = None    # result after patch + re-run
    file_path: Optional[str] = None        # file that was patched
