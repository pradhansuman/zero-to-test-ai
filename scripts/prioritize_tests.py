#!/usr/bin/env python3
"""
scripts/prioritize_tests.py
────────────────────────────
Dynamic test prioritization based on git diff.

Reads the list of files changed since a base commit (default: HEAD~1) and maps
them to the highest-risk Playwright test patterns. Only those test groups run
in CI on minor PRs — cutting runtime from ~8 min to < 2 min for low-risk changes.

Usage:
    # Get grep pattern for current diff
    python scripts/prioritize_tests.py

    # Diff against a specific base
    python scripts/prioritize_tests.py --base main

    # Output JSON (for CI matrix)
    python scripts/prioritize_tests.py --json

    # Use in Playwright (pipe into --grep)
    GREP=$(python scripts/prioritize_tests.py)
    npx playwright test --config playwright.math-hub.config.ts --grep "$GREP"

    # Always run full suite (override)
    python scripts/prioritize_tests.py --full

Exit codes:
    0 — success; grep pattern printed to stdout
    1 — error; message on stderr
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# ─── Risk mapping: file glob patterns → Playwright test grep patterns ──────────
#
# Each entry maps a file path pattern (Python regex against git diff output) to
# a list of grep strings. Any test whose describe/test title matches any of those
# strings will be included in the priority run.
#
# Risk levels:
#   P0 patterns — run if ANY file changes (always included)
#   P1 patterns — run when specific areas change
#
RISK_MAP: list[dict] = [
    {
        "name": "math_hub_source",
        "description": "Main SPA source changed — full functional + visual suite",
        "file_patterns": [r"math_hub\.html$", r"math_hub\.css$", r"math_hub\.js$"],
        "grep_patterns": [
            "CBSE",           # all golden spec tests
            "TC-API",         # API contract tests
            "VR-",            # visual regression tests
            "TC-SEC",         # security tests
        ],
        "priority": "P0",
    },
    {
        "name": "playwright_config",
        "description": "Playwright config changed — run smoke suite to validate setup",
        "file_patterns": [r"playwright.*\.config\.ts$", r"playwright.*\.config\.js$"],
        "grep_patterns": [
            "TC-001",         # page load (smoke)
            "TC-002",         # navigation (smoke)
            "TC-003",         # core widget (smoke)
        ],
        "priority": "P0",
    },
    {
        "name": "performance_tests",
        "description": "Perf spec or k6 changed — run full perf suite",
        "file_patterns": [r"math-hub-perf\.spec\.ts$", r"math-hub\.k6\.js$"],
        "grep_patterns": ["TC-PERF"],
        "priority": "P1",
    },
    {
        "name": "security_tests",
        "description": "Security spec changed — run full security suite",
        "file_patterns": [r"math-hub-security\.spec\.ts$"],
        "grep_patterns": ["TC-SEC"],
        "priority": "P1",
    },
    {
        "name": "api_tests",
        "description": "API spec changed — run API contract suite",
        "file_patterns": [r"math-hub-api\.spec\.ts$"],
        "grep_patterns": ["TC-API"],
        "priority": "P1",
    },
    {
        "name": "loop_tests",
        "description": "Endurance loop spec changed — run loop suite",
        "file_patterns": [r"math-hub-loop\.spec\.ts$"],
        "grep_patterns": ["TC-LOOP"],
        "priority": "P1",
    },
    {
        "name": "visual_tests",
        "description": "Visual spec or baselines changed — run visual regression suite",
        "file_patterns": [r"math-hub-visual\.spec\.ts$", r"__snapshots__/"],
        "grep_patterns": ["VR-"],
        "priority": "P1",
    },
    {
        "name": "pipeline_agents",
        "description": "Pipeline agent code changed — run demo pipeline smoke test",
        "file_patterns": [r"agents/", r"orchestrator/", r"contracts/"],
        "grep_patterns": [],     # No Playwright tests — CI runs python -m orchestrator.pipeline --demo --offline
        "priority": "P1",
        "ci_command": "python -m orchestrator.pipeline --demo --offline",
    },
    {
        "name": "healer",
        "description": "Healer / failure classification changed — run unit tests",
        "file_patterns": [r"agents/healer\.py$", r"contracts/schemas\.py$"],
        "grep_patterns": [],
        "priority": "P1",
        "ci_command": "python -m pytest tests/unit/ -q",
    },
]

# Tests that always run regardless of diff (smoke gate)
ALWAYS_RUN = ["TC-001", "TC-002", "TC-003"]


def get_changed_files(base: str) -> list[str]:
    """Return list of files changed vs base ref."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base],
            capture_output=True, text=True, check=True,
        )
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        if not files:
            # Try staged files too (for pre-commit hooks)
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True, text=True, check=True,
            )
            files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        return files
    except subprocess.CalledProcessError as e:
        print(f"git diff failed: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def match_risk(changed_files: list[str]) -> list[dict]:
    """Return the risk entries triggered by the changed file list."""
    triggered = []
    for entry in RISK_MAP:
        for changed in changed_files:
            if any(re.search(pat, changed) for pat in entry["file_patterns"]):
                triggered.append(entry)
                break
    return triggered


def build_grep_pattern(triggered: list[dict]) -> str:
    """Combine all grep patterns into a single Playwright --grep regex."""
    patterns = list(ALWAYS_RUN)
    for entry in triggered:
        patterns.extend(entry.get("grep_patterns", []))
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique = [p for p in patterns if not (p in seen or seen.add(p))]  # type: ignore[func-returns-value]
    return "|".join(unique)


def main() -> None:
    ap = argparse.ArgumentParser(description="Compute Playwright --grep from git diff")
    ap.add_argument("--base", default="HEAD~1",
                    help="Base git ref to diff against (default: HEAD~1)")
    ap.add_argument("--json", action="store_true",
                    help="Output full JSON report instead of grep pattern")
    ap.add_argument("--full", action="store_true",
                    help="Always run full suite (print empty string — no --grep filter)")
    args = ap.parse_args()

    if args.full:
        print("")  # empty = no filter = all tests run
        return

    changed = get_changed_files(args.base)

    if not changed:
        print("", file=sys.stderr)
        print("No changed files detected — running full suite.", file=sys.stderr)
        print("")
        return

    triggered = match_risk(changed)
    grep = build_grep_pattern(triggered)

    if args.json:
        report = {
            "base": args.base,
            "changed_files": changed,
            "triggered_rules": [
                {"name": e["name"], "priority": e["priority"], "description": e["description"]}
                for e in triggered
            ],
            "ci_commands": [e["ci_command"] for e in triggered if "ci_command" in e],
            "grep_pattern": grep,
            "full_suite": not bool(grep.strip()),
        }
        print(json.dumps(report, indent=2))
    else:
        if triggered:
            names = ", ".join(e["name"] for e in triggered)
            print(f"# Triggered rules: {names}", file=sys.stderr)
            print(f"# Changed files: {', '.join(changed[:5])}"
                  + ("..." if len(changed) > 5 else ""), file=sys.stderr)
        print(grep)


if __name__ == "__main__":
    main()
