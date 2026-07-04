#!/usr/bin/env python3
"""
Test Results Validation & Guardrails
Prevents misreporting and hallucinatory test counts
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple

def parse_playwright_report(report_dir: str = "playwright-report") -> Dict:
    """Extract actual test counts from Playwright JSON or HTML report."""
    try:
        # Try JSON first (authoritative source)
        json_file = Path(report_dir) / "test-results.json"
        if json_file.exists():
            with open(json_file) as f:
                data = json.load(f)
            stats = data.get("stats", {})
            return {
                "total": stats.get("expected", 0),
                "passed": stats.get("expected", 0) - stats.get("unexpected", 0) - stats.get("flaky", 0),
                "failed": stats.get("unexpected", 0),
                "flaky": stats.get("flaky", 0),
                "skipped": stats.get("skipped", 0),
                "source": "test-results.json"
            }

        # Fallback to HTML report parsing
        html_file = Path(report_dir) / "index.html"
        if html_file.exists():
            with open(html_file) as f:
                html_content = f.read()

            # Extract counts from HTML (look for patterns like "286 tests" etc)
            import re

            # Look for stat boxes
            test_match = re.search(r'(\d+)\s+(?:total\s+)?tests?', html_content, re.IGNORECASE)
            passed_match = re.search(r'(\d+)\s+passed', html_content, re.IGNORECASE)
            failed_match = re.search(r'(\d+)\s+failed', html_content, re.IGNORECASE)
            flaky_match = re.search(r'(\d+)\s+flaky', html_content, re.IGNORECASE)

            if test_match:
                total = int(test_match.group(1))
                passed = int(passed_match.group(1)) if passed_match else 0
                failed = int(failed_match.group(1)) if failed_match else 0
                flaky = int(flaky_match.group(1)) if flaky_match else 0

                return {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "flaky": flaky,
                    "skipped": 0,
                    "source": "index.html (parsed)"
                }

        return {"error": f"No test results found in {report_dir}"}
    except Exception as e:
        return {"error": str(e)}

def validate_test_metrics(actual: Dict) -> Tuple[bool, str]:
    """
    Validate test metrics for consistency.
    Returns (is_valid, message)
    """
    errors = []

    # Check required fields
    required = ["total", "passed", "failed", "flaky"]
    for field in required:
        if field not in actual:
            errors.append(f"Missing metric: {field}")

    if errors:
        return False, "; ".join(errors)

    total = actual["total"]
    passed = actual["passed"]
    failed = actual["failed"]
    flaky = actual["flaky"]

    # Validation rules
    validations = [
        (passed + failed + flaky <= total,
         f"Sum of results ({passed + failed + flaky}) exceeds total ({total})"),

        (passed >= 0, "Passed count cannot be negative"),
        (failed >= 0, "Failed count cannot be negative"),
        (flaky >= 0, "Flaky count cannot be negative"),

        (total > 0, "Total test count must be > 0"),

        (passed <= total, f"Passed ({passed}) cannot exceed total ({total})"),

        (passed + failed + flaky == total,
         f"Math check failed: {passed} + {failed} + {flaky} != {total}"),
    ]

    for condition, error_msg in validations:
        if not condition:
            errors.append(error_msg)

    if errors:
        return False, "; ".join(errors)

    return True, "All metrics valid"

def generate_safe_summary(actual: Dict) -> str:
    """Generate summary only after validation."""
    is_valid, msg = validate_test_metrics(actual)

    if not is_valid:
        return f"⚠️ VALIDATION FAILED: {msg}\nCannot generate summary until metrics are corrected."

    total = actual["total"]
    passed = actual["passed"]
    failed = actual["failed"]
    flaky = actual["flaky"]
    pass_rate = (passed / total * 100) if total > 0 else 0

    return f"""
✅ TEST RESULTS SUMMARY (VALIDATED)
{'='*50}
Total Tests:     {total}
Passed:          {passed} ({pass_rate:.1f}%)
Failed:          {failed}
Flaky:           {flaky}
Status:          {'🟢 PRODUCTION READY' if failed == 0 else '🔴 ISSUES FOUND'}
{'='*50}
""".strip()

def main():
    """Main validation routine."""
    print("🔍 Validating test results...\n")

    # Parse report
    actual = parse_playwright_report()

    if "error" in actual:
        print(f"❌ Error: {actual['error']}")
        sys.exit(1)

    print("📊 Extracted metrics:")
    for key, value in actual.items():
        print(f"  {key:12} = {value}")

    # Validate
    is_valid, msg = validate_test_metrics(actual)
    print(f"\n{'✅' if is_valid else '❌'} Validation: {msg}")

    if not is_valid:
        sys.exit(1)

    # Generate summary
    print("\n" + generate_safe_summary(actual))

    # Guardrail: Warn on unexpected changes
    print("\n🛡️ GUARDRAILS:")
    if actual["flaky"] > 0:
        print(f"  ⚠️  {actual['flaky']} flaky test(s) detected - investigate timing issues")
    if actual["failed"] > 0:
        print(f"  🔴 {actual['failed']} test(s) failed - review before merge")
    if actual["total"] < 50:
        print(f"  ⚠️  Only {actual['total']} tests - ensure coverage is adequate")
    if actual["passed"] < actual["total"] * 0.95:
        print(f"  ⚠️  Pass rate below 95% - investigate quality issues")

    return 0

if __name__ == "__main__":
    sys.exit(main())
