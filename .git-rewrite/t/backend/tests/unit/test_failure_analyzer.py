"""Unit tests for failure analyzer service."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.failure_analyzer import FailureAnalyzer


@pytest.fixture
def mock_db():
    """Create mock database session."""
    return AsyncMock()


@pytest.fixture
def mock_claude_client():
    """Create mock Claude client."""
    return AsyncMock()


@pytest.fixture
def failure_analyzer(mock_db, mock_claude_client):
    """Create failure analyzer instance with mocks."""
    return FailureAnalyzer(mock_db, mock_claude_client)


class TestFailureClassification:
    """Test failure type classification."""

    def test_classify_assertion_failure(self, failure_analyzer):
        """Test assertion failure classification."""
        error_msg = "AssertionError: expected True but got False"
        result = failure_analyzer._classify_failure(error_msg)
        assert result == "assertion"

    def test_classify_timeout_failure(self, failure_analyzer):
        """Test timeout failure classification."""
        error_msg = "TimeoutError: Wait timed out after 30 seconds"
        result = failure_analyzer._classify_failure(error_msg)
        assert result == "timeout"

    def test_classify_network_failure(self, failure_analyzer):
        """Test network failure classification."""
        error_msg = "ConnectionError: Failed to establish connection to API"
        result = failure_analyzer._classify_failure(error_msg)
        assert result == "network"

    def test_classify_locator_failure(self, failure_analyzer):
        """Test locator failure classification."""
        error_msg = "NoSuchElementException: Element not found with selector"
        result = failure_analyzer._classify_failure(error_msg)
        assert result == "locator"

    def test_classify_environment_failure(self, failure_analyzer):
        """Test environment failure classification."""
        error_msg = "EnvironmentError: MISSING_API_KEY env variable not set"
        result = failure_analyzer._classify_failure(error_msg)
        assert result == "environment"

    def test_classify_unknown_failure(self, failure_analyzer):
        """Test unknown failure classification."""
        error_msg = "SomeRandomError: Something went wrong"
        result = failure_analyzer._classify_failure(error_msg)
        assert result == "unknown"

    def test_classify_with_stack_trace(self, failure_analyzer):
        """Test classification considers stack trace."""
        error_msg = "Error occurred"
        stack_trace = "connection refused in network.py"
        result = failure_analyzer._classify_failure(error_msg, stack_trace)
        assert result == "network"


class TestPriorityCalculation:
    """Test priority calculation based on failure type."""

    def test_assertion_is_high_priority(self, failure_analyzer):
        """Test assertion failures are high priority."""
        priority = failure_analyzer._calculate_priority("assertion")
        assert priority == "high"

    def test_timeout_is_high_priority(self, failure_analyzer):
        """Test timeout failures are high priority."""
        priority = failure_analyzer._calculate_priority("timeout")
        assert priority == "high"

    def test_network_is_high_priority(self, failure_analyzer):
        """Test network failures are high priority."""
        priority = failure_analyzer._calculate_priority("network")
        assert priority == "high"

    def test_locator_is_medium_priority(self, failure_analyzer):
        """Test locator failures are medium priority."""
        priority = failure_analyzer._calculate_priority("locator")
        assert priority == "medium"

    def test_environment_is_critical_priority(self, failure_analyzer):
        """Test environment failures are critical."""
        priority = failure_analyzer._calculate_priority("environment")
        assert priority == "critical"

    def test_unknown_is_low_priority(self, failure_analyzer):
        """Test unknown failures are low priority."""
        priority = failure_analyzer._calculate_priority("unknown")
        assert priority == "low"


@pytest.mark.asyncio
async def test_analyze_failure_basic(mock_db, mock_claude_client):
    """Test basic failure analysis."""
    mock_claude_client.analyze_test_failure.return_value = {
        "analysis": "Test logic error",
        "fixes": ["Check expected value", "Verify test data"],
    }

    analyzer = FailureAnalyzer(mock_db, mock_claude_client)
    result = await analyzer.analyze_failure(
        error_msg="AssertionError: expected True",
        test_name="test_login",
        stack_trace="test_auth.py:10",
    )

    assert result["test_name"] == "test_login"
    assert result["failure_type"] == "assertion"
    assert result["priority"] == "high"
    assert result["root_cause"] == "Test logic error"
    assert len(result["suggested_fixes"]) == 2


@pytest.mark.asyncio
async def test_analyze_failure_stores_in_history(mock_db, mock_claude_client):
    """Test that analyzed failures are stored in history."""
    mock_claude_client.analyze_test_failure.return_value = {
        "analysis": "Root cause",
        "fixes": [],
    }

    analyzer = FailureAnalyzer(mock_db, mock_claude_client)

    # Analyze two failures
    await analyzer.analyze_failure(
        error_msg="AssertionError: test1",
        test_name="test_one",
    )
    await analyzer.analyze_failure(
        error_msg="AssertionError: test2",
        test_name="test_two",
    )

    # Check history contains both
    assert len(analyzer.failure_history["assertion"]) == 2


@pytest.mark.asyncio
async def test_analyze_failure_handles_claude_error(mock_db, mock_claude_client):
    """Test failure analysis handles Claude API errors gracefully."""
    mock_claude_client.analyze_test_failure.side_effect = Exception("API error")

    analyzer = FailureAnalyzer(mock_db, mock_claude_client)
    result = await analyzer.analyze_failure(
        error_msg="Test error",
        test_name="test_something",
    )

    assert "error" in result
    assert "API error" in result["error"]


@pytest.mark.asyncio
async def test_check_failure_history_empty(mock_db):
    """Test checking failure history when empty."""
    analyzer = FailureAnalyzer(mock_db)
    similar = await analyzer._check_failure_history("error", "assertion")
    assert similar == []


@pytest.mark.asyncio
async def test_check_failure_history_finds_similar(mock_db):
    """Test finding similar failures in history."""
    analyzer = FailureAnalyzer(mock_db)

    # Manually add to history
    analyzer.failure_history["assertion"] = [
        {
            "error_message": "Expected value is missing",
            "root_cause": "Data issue",
            "suggested_fixes": ["Check data"],
            "timestamp": "2026-07-03T00:00:00",
        }
    ]

    similar = await analyzer._check_failure_history(
        "Expected value is incorrect", "assertion"
    )

    assert len(similar) > 0
    assert "Expected" in similar[0]["error_message"]


@pytest.mark.asyncio
async def test_get_analysis_statistics(mock_db, mock_claude_client):
    """Test getting analysis statistics."""
    mock_claude_client.analyze_test_failure.return_value = {
        "analysis": "Root cause",
        "fixes": [],
    }

    analyzer = FailureAnalyzer(mock_db, mock_claude_client)

    # Analyze different types of failures
    await analyzer.analyze_failure("AssertionError: test1", "test_one")
    await analyzer.analyze_failure("TimeoutError: test2", "test_two")
    await analyzer.analyze_failure("AssertionError: test3", "test_three")

    stats = await analyzer.get_analysis_statistics()

    assert stats["total_failures_analyzed"] == 3
    assert "assertion" in stats["by_type"]
    assert "timeout" in stats["by_type"]
    assert stats["by_type"]["assertion"] == 2
    assert stats["by_type"]["timeout"] == 1


@pytest.mark.asyncio
async def test_store_failure_analysis_respects_limit(mock_db, mock_claude_client):
    """Test that failure history respects 100-entry limit per type."""
    mock_claude_client.analyze_test_failure.return_value = {
        "analysis": "Root cause",
        "fixes": [],
    }

    analyzer = FailureAnalyzer(mock_db, mock_claude_client)

    # Store 105 assertion failures
    for i in range(105):
        await analyzer.analyze_failure(f"AssertionError: test_{i}", f"test_{i}")

    # Should keep only last 100
    assert len(analyzer.failure_history["assertion"]) == 100


def test_failure_types_defined(failure_analyzer):
    """Test that all failure types are properly defined."""
    expected_types = [
        "assertion",
        "timeout",
        "network",
        "locator",
        "environment",
        "unknown",
    ]

    for ft in expected_types:
        assert ft in failure_analyzer.FAILURE_TYPES
        assert isinstance(failure_analyzer.FAILURE_TYPES[ft], str)
        assert len(failure_analyzer.FAILURE_TYPES[ft]) > 0


def test_priority_mapping_comprehensive(failure_analyzer):
    """Test that all failure types have priority mappings."""
    for failure_type in failure_analyzer.FAILURE_TYPES.keys():
        priority = failure_analyzer._calculate_priority(failure_type)
        assert priority in ["critical", "high", "medium", "low"]
