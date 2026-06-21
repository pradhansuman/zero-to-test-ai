"""
agents/runner.py
────────────────
STAGE 4 — Test Layers / Runner.

Executes the generated suite and rolls results up into RunResults. Like the
Ingestor, this stage is deterministic — it shells out to the real Playwright
CLI and parses its JSON reporter. No LLM: test results must be ground truth.

I/O CONTRACT
    in : GeneratedSuite
    out: RunResults

Two modes:
  • real=True  → writes files to a workspace, runs `npx playwright test`,
                 parses results.json (use in CI).
  • real=False → deterministic simulation for local demos / unit tests of the
                 pipeline itself (no Node required).
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from contracts.schemas import (
    GeneratedSuite, RunResults, TestResult, TestType, Priority,
)


class RunnerAgent:
    NAME = "runner"

    def __init__(self, workspace: str = "./.qa-workspace", real: bool = False):
        self.workspace = Path(workspace)
        self.real = real

    # ── write generated files to disk ───────────────────────────
    def _materialise(self, suite: GeneratedSuite) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)

        # Write only spec files — skip any config the LLM generated; we provide our own
        for f in suite.files:
            if "playwright.config" in f.path:
                continue
            dest = self.workspace / f.path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(f.content, encoding="utf-8")

        # Write a guaranteed-working config — reads QA_TARGET_URL so the right
        # app is tested; writes JSON report to a file (not stdout) for reliability
        target_url = os.environ.get("QA_TARGET_URL", "https://demoqa.com")
        (self.workspace / "playwright.config.ts").write_text(
            f"""import {{ defineConfig }} from '@playwright/test';
export default defineConfig({{
  testDir: './tests',
  timeout: 30_000,
  retries: 1,
  use: {{
    headless: true,
    baseURL: '{target_url}',
    screenshot: 'only-on-failure',
  }},
  reporter: [['json', {{ outputFile: 'results.json' }}]],
}});
""",
            encoding="utf-8",
        )

        # Symlink parent node_modules so the config can be compiled by Playwright
        node_link = self.workspace / "node_modules"
        parent_modules = Path.cwd() / "node_modules"
        if parent_modules.exists() and not node_link.exists():
            node_link.symlink_to(parent_modules.resolve())

        pkg = self.workspace / "package.json"
        if not pkg.exists():
            pkg.write_text('{"name":"qa-suite","private":true}', encoding="utf-8")

    # ── real Playwright run ─────────────────────────────────────
    def _run_real(self, suite: GeneratedSuite) -> RunResults:
        self._materialise(suite)

        # Use local binary (via symlinked node_modules) to avoid version mismatch
        pw_bin = self.workspace / "node_modules" / ".bin" / "playwright"
        cmd = [str(pw_bin) if pw_bin.exists() else "npx playwright", "test"]
        if not pw_bin.exists():
            cmd = ["npx", "playwright", "test"]

        # Pre-flight: list discovered tests so errors appear in the pipeline output
        list_result = subprocess.run(
            cmd[:-1] + ["test", "--list"] if pw_bin.exists() else ["npx", "playwright", "test", "--list"],
            cwd=self.workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"[runner] test discovery:\n{list_result.stdout[:600] or '(empty)'}")
        if list_result.stderr:
            print(f"[runner] discovery errors:\n{list_result.stderr[:600]}")

        # Run the tests — config writes results.json via reporter option
        result = subprocess.run(
            cmd,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"[runner] playwright exit={result.returncode}")
        if result.stderr:
            print(f"[runner] stderr:\n{result.stderr[:800]}")

        results_path = self.workspace / "results.json"
        if not results_path.exists():
            raise RuntimeError(
                f"Playwright produced no results.json (exit {result.returncode}).\n"
                f"stdout: {result.stdout[:400]}\n"
                f"stderr: {result.stderr[:800]}"
            )
        report = json.loads(results_path.read_text())

        results: list[TestResult] = []
        for spec in report.get("suites", []):
            for case in spec.get("specs", []):
                t = case["tests"][0]
                res = t["results"][0]
                results.append(TestResult(
                    id=case["title"].split(":")[0],
                    name=case["title"],
                    type=TestType.E2E,
                    priority=Priority.P1,
                    passed=res["status"] == "passed",
                    duration_ms=res.get("duration", 0),
                    retries=len(t["results"]) - 1,
                    error=(res.get("error") or {}).get("message"),
                ))
        return self._rollup(suite.issue_number, results)

    # ── deterministic simulation (demo) ─────────────────────────
    def _run_sim(self, suite: GeneratedSuite) -> RunResults:
        results: list[TestResult] = []
        seed = suite.issue_number
        for i, f in enumerate(suite.files):
            for j, tc in enumerate(f.covers or [f"TC-{i+1:03d}"]):
                # deterministic pseudo-result: P0s occasionally retry
                idx = seed + i * 10 + j
                passed = (idx % 7) != 0
                # failed tests get a locator-style error so the Healer has
                # something realistic to repair in the demo
                err = None
                if not passed:
                    err = (
                        "locator('[data-testid=\"submit-btn\"]') resolved to 0 "
                        "elements — waiting for selector timed out"
                    )
                results.append(TestResult(
                    id=tc,
                    name=f"{tc} — {f.path}",
                    type=TestType.E2E if "spec" in f.path else TestType.UNIT,
                    priority=Priority.P0 if j == 0 else Priority.P1,
                    passed=passed,
                    duration_ms=300 + (idx % 5) * 240,
                    retries=1 if (idx % 5 == 0) else 0,
                    error=err,
                ))
        return self._rollup(suite.issue_number, results)

    # ── DOM snapshot provider (for the Self-Healing agent) ──────
    def dom_provider(self, test_id: str) -> str:
        """
        Return the current DOM for a failing test.
          • real mode: read the Playwright trace / page snapshot from the run.
          • sim mode : a canned snapshot where the button's testid has been
            RENAMED from 'submit-btn' to 'login-submit' — i.e. the UI changed,
            which is exactly the scenario self-healing exists for.
        """
        if self.real:
            snap = self.workspace / "snapshots" / f"{test_id}.html"
            if snap.exists():
                return snap.read_text(encoding="utf-8")
        return (
            '<form data-testid="login-form">'
            '<input data-testid="email-input" aria-invalid="true"/>'
            '<input data-testid="password-input" type="password"/>'
            '<span data-testid="email-error" role="alert">Email is required</span>'
            '<button data-testid="login-submit" type="submit">Sign in</button>'
            '</form>'
        )

    # ── roll-up ─────────────────────────────────────────────────
    @staticmethod
    def _rollup(issue_number: int, results: list[TestResult]) -> RunResults:
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        return RunResults(
            issue_number=issue_number,
            results=results,
            total=total,
            passed=passed,
            failed=total - passed,
            pass_rate=round(passed / total * 100, 1) if total else 0.0,
            total_duration_ms=sum(r.duration_ms for r in results),
        )

    def run(self, suite: GeneratedSuite) -> RunResults:
        return self._run_real(suite) if self.real else self._run_sim(suite)
