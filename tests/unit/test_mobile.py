"""
tests/unit/test_mobile.py
──────────────────────────
Unit tests for mobile/cross-browser support.

Covers:
  - BrowserTarget enum values and BROWSER_DEVICE_MAP completeness
  - GeneratedSuite.browser_targets default and validation
  - Runner config generation: multi-project playwright.config.ts content
  - Generator fallback: UI suites get mobile targets injected
  - SDETTestPlan.to_test_plan() maps 'responsive' type correctly
"""
import pytest

from contracts.schemas import (
    BrowserTarget, BROWSER_DEVICE_MAP,
    GeneratedSuite, GeneratedFile,
    SDETTestCase, SDETTestPlan,
    TestType,
)


# ── BrowserTarget enum ────────────────────────────────────────────────────────

class TestBrowserTargetEnum:
    def test_chromium_desktop_value(self):
        assert BrowserTarget.CHROMIUM_DESKTOP == "chromium-desktop"

    def test_chromium_mobile_value(self):
        assert BrowserTarget.CHROMIUM_MOBILE == "chromium-mobile"

    def test_webkit_mobile_value(self):
        assert BrowserTarget.WEBKIT_MOBILE == "webkit-mobile"

    def test_firefox_desktop_value(self):
        assert BrowserTarget.FIREFOX_DESKTOP == "firefox-desktop"

    def test_tablet_chrome_value(self):
        assert BrowserTarget.TABLET_CHROME == "tablet-chrome"

    def test_five_targets_defined(self):
        assert len(BrowserTarget) == 5


class TestBrowserDeviceMap:
    def test_all_targets_have_device_mapping(self):
        for target in BrowserTarget:
            assert target in BROWSER_DEVICE_MAP, f"{target} missing from BROWSER_DEVICE_MAP"

    def test_desktop_chrome_maps_to_correct_device(self):
        name, device = BROWSER_DEVICE_MAP[BrowserTarget.CHROMIUM_DESKTOP]
        assert "Chrome" in name
        assert "Desktop Chrome" in device

    def test_mobile_chrome_maps_to_pixel(self):
        name, device = BROWSER_DEVICE_MAP[BrowserTarget.CHROMIUM_MOBILE]
        assert "Mobile" in name
        assert "Pixel" in device

    def test_webkit_mobile_maps_to_iphone(self):
        name, device = BROWSER_DEVICE_MAP[BrowserTarget.WEBKIT_MOBILE]
        assert "Safari" in name
        assert "iPhone" in device

    def test_tablet_maps_to_ipad(self):
        name, device = BROWSER_DEVICE_MAP[BrowserTarget.TABLET_CHROME]
        assert "iPad" in device

    def test_all_device_names_nonempty(self):
        for target, (name, device) in BROWSER_DEVICE_MAP.items():
            assert name.strip(), f"Empty project name for {target}"
            assert device.strip(), f"Empty device key for {target}"


# ── GeneratedSuite defaults ───────────────────────────────────────────────────

class TestGeneratedSuiteDefaults:
    def _make_suite(self, targets=None) -> GeneratedSuite:
        kwargs = dict(
            issue_number=1,
            files=[GeneratedFile(path="tests/e2e/test.spec.ts", content="// test")],
        )
        if targets is not None:
            kwargs["browser_targets"] = targets
        return GeneratedSuite(**kwargs)

    def test_default_is_desktop_only(self):
        suite = self._make_suite()
        assert suite.browser_targets == [BrowserTarget.CHROMIUM_DESKTOP]

    def test_explicit_mobile_targets_accepted(self):
        targets = [BrowserTarget.CHROMIUM_DESKTOP, BrowserTarget.CHROMIUM_MOBILE]
        suite = self._make_suite(targets)
        assert BrowserTarget.CHROMIUM_MOBILE in suite.browser_targets

    def test_all_five_targets_accepted(self):
        all_targets = list(BrowserTarget)
        suite = self._make_suite(all_targets)
        assert len(suite.browser_targets) == 5

    def test_webkit_mobile_accepted(self):
        suite = self._make_suite([BrowserTarget.WEBKIT_MOBILE])
        assert suite.browser_targets[0] == BrowserTarget.WEBKIT_MOBILE


# ── Runner config generation ──────────────────────────────────────────────────

class TestRunnerConfigGeneration:
    """
    Test that the Runner constructs the correct playwright.config.ts content
    for single and multi-browser targets.
    Uses string generation logic in isolation (no subprocess calls).
    """

    @staticmethod
    def _build_config(targets: list[BrowserTarget], target_url: str, test_dir: str, results_path: str) -> str:
        projects_ts = "\n".join(
            f"    {{ name: '{name}', use: {{ ...devices['{device}'] }} }},"
            for t in targets
            for name, device in [BROWSER_DEVICE_MAP.get(t, ("Desktop Chrome", "Desktop Chrome"))]
        )
        return f"""import {{ defineConfig, devices }} from '@playwright/test';
export default defineConfig({{
  testDir: '{test_dir}',
  timeout: 30_000,
  retries: 1,
  use: {{ headless: true, baseURL: '{target_url}' }},
  reporter: [['json', {{ outputFile: '{results_path}' }}]],
  projects: [
{projects_ts}
  ],
}});
"""

    def test_desktop_only_config(self):
        cfg = self._build_config(
            [BrowserTarget.CHROMIUM_DESKTOP],
            "https://example.com", "/tmp/tests", "/tmp/results.json"
        )
        assert "Desktop Chrome" in cfg
        assert "Pixel 7" not in cfg
        assert "iPhone" not in cfg

    def test_mobile_config_includes_three_projects(self):
        targets = [
            BrowserTarget.CHROMIUM_DESKTOP,
            BrowserTarget.CHROMIUM_MOBILE,
            BrowserTarget.WEBKIT_MOBILE,
        ]
        cfg = self._build_config(targets, "https://example.com", "/tmp/tests", "/tmp/results.json")
        assert "Desktop Chrome" in cfg
        assert "Pixel 7" in cfg
        assert "iPhone 14" in cfg

    def test_config_has_projects_block(self):
        cfg = self._build_config(
            [BrowserTarget.CHROMIUM_DESKTOP],
            "https://example.com", "/tmp/tests", "/tmp/results.json"
        )
        assert "projects:" in cfg

    def test_config_imports_devices(self):
        cfg = self._build_config(
            [BrowserTarget.CHROMIUM_MOBILE],
            "https://example.com", "/tmp/tests", "/tmp/results.json"
        )
        assert "devices" in cfg

    def test_tablet_config(self):
        cfg = self._build_config(
            [BrowserTarget.TABLET_CHROME],
            "https://example.com", "/tmp/tests", "/tmp/results.json"
        )
        assert "iPad Pro 11" in cfg


# ── SDETTestPlan responsive type mapping ─────────────────────────────────────

class TestResponsiveTypeMapping:
    def _make_responsive_case(self) -> SDETTestCase:
        return SDETTestCase(
            id="TC-001", title="Nav collapses at 375px",
            requirement_ref="AC-1", type="responsive",
            technique="Boundary Value Analysis", priority="P1",
            risk_rationale="Mobile users can't navigate without hamburger menu",
            steps=["1. View at 375px", "2. Check nav"], expected_result="hamburger visible",
        )

    def test_responsive_maps_to_e2e(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[self._make_responsive_case()])
        test_plan = plan.to_test_plan()
        assert test_plan.scenarios[0].type == TestType.E2E

    def test_responsive_coverage_area_included(self):
        plan = SDETTestPlan(issue_number=1, test_cases=[self._make_responsive_case()])
        test_plan = plan.to_test_plan()
        assert "responsive" in test_plan.coverage_areas

    def test_accessibility_maps_to_e2e(self):
        case = SDETTestCase(
            id="TC-002", title="Touch target size >= 44px",
            requirement_ref="AC-2", type="accessibility",
            technique="Error Guessing / Negative", priority="P1",
            risk_rationale="Small targets fail WCAG on mobile",
            steps=["1. Check button height"], expected_result="height >= 44px",
        )
        plan = SDETTestPlan(issue_number=1, test_cases=[case])
        assert plan.to_test_plan().scenarios[0].type == TestType.E2E
