"""
tests/unit/test_triage.py
──────────────────────────
Unit tests for HealerAgent.classify_failure() and extract_selector().

These functions are the security boundary of the self-healing system:
  - classify_failure() must NEVER misclassify ASSERTION as LOCATOR
    (doing so would auto-heal a real bug, hiding it from engineers)
  - extract_selector() must return None rather than a wrong selector
"""
import pytest

from agents.healer import classify_failure, extract_selector
from contracts.schemas import FailureKind


class TestClassifyLocator:
    """All of these should be healable LOCATOR failures."""

    def test_locator_keyword(self):
        assert classify_failure("locator('button') resolved to 0 elements") == FailureKind.LOCATOR

    def test_no_element(self):
        assert classify_failure("No element found matching selector [data-testid='submit']") == FailureKind.LOCATOR

    def test_not_found(self):
        assert classify_failure("Element not found: #cart-button") == FailureKind.LOCATOR

    def test_not_visible(self):
        assert classify_failure("Element is not visible: .checkout-btn") == FailureKind.LOCATOR

    def test_waiting_for_selector(self):
        # Root cause is the selector, not a generic timeout — healer should attempt repair
        assert classify_failure("Timeout waiting for selector '[data-testid=\"login\"]'") == FailureKind.LOCATOR

    def test_resolved_to_0(self):
        assert classify_failure("locator.click: Error: resolved to 0 elements") == FailureKind.LOCATOR

    def test_strict_mode_violation(self):
        assert classify_failure("strict mode violation: locator('a') resolved to 2 elements") == FailureKind.LOCATOR


class TestClassifyAssertion:
    """These are NEVER healable — a real functional bug caused them."""

    def test_expect_call(self):
        assert classify_failure("expect(received).toBe(expected)") == FailureKind.ASSERTION

    def test_to_equal(self):
        assert classify_failure("Error: expect(value).to equal '0.875'") == FailureKind.ASSERTION

    def test_received_value(self):
        assert classify_failure("received: '0.5', expected: '0.875'") == FailureKind.ASSERTION

    def test_assertion_keyword(self):
        assert classify_failure("Assertion failed: text mismatch") == FailureKind.ASSERTION

    def test_to_be_keyword(self):
        assert classify_failure("Expected element to be checked") == FailureKind.ASSERTION

    def test_never_heals_assertion(self):
        # This is the critical invariant: assertion != locator, ever
        result = classify_failure("expect(locator).toHaveText('hello')")
        assert result == FailureKind.ASSERTION, (
            "CRITICAL: assertion failure must never be classified as LOCATOR"
        )


class TestClassifyTimeout:
    def test_timeout(self):
        assert classify_failure("Timeout 30000ms exceeded") == FailureKind.TIMEOUT

    def test_timed_out(self):
        assert classify_failure("page.waitForSelector: Timeout: Timed out 5000ms") == FailureKind.TIMEOUT


class TestClassifyOther:
    def test_none_error(self):
        assert classify_failure(None) == FailureKind.OTHER

    def test_empty_string(self):
        assert classify_failure("") == FailureKind.OTHER

    def test_unknown_error(self):
        assert classify_failure("JavaScript heap out of memory") == FailureKind.ENVIRONMENT

    def test_network_error(self):
        assert classify_failure("net::ERR_CONNECTION_REFUSED") == FailureKind.ENVIRONMENT


class TestExtractSelector:
    def test_data_testid_bracket(self):
        error = "locator('[data-testid=\"submit-btn\"]') resolved to 0 elements"
        sel = extract_selector(error)
        assert sel is not None
        assert "submit-btn" in sel

    def test_get_by_test_id(self):
        error = "getByTestId('cart-button') strict mode violation"
        sel = extract_selector(error)
        assert sel == "cart-button"

    def test_locator_css(self):
        error = "locator('css=.checkout') not found"
        sel = extract_selector(error)
        assert sel is not None

    def test_none_on_empty(self):
        assert extract_selector(None) is None

    def test_none_on_no_selector(self):
        assert extract_selector("JavaScript error: cannot read property") is None
