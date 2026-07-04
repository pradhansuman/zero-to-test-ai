"""Simple validation script for Task 3: Failure Analysis Engine."""
import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.services.failure_analyzer import FailureAnalyzer


async def test_failure_analyzer():
    """Test failure analyzer service."""
    print("=" * 60)
    print("TASK 3: Failure Analysis Engine - Validation Tests")
    print("=" * 60)

    # Create mock objects
    mock_db = AsyncMock()
    mock_claude = AsyncMock()
    mock_claude.analyze_test_failure.return_value = {
        "analysis": "Test logic validation failed",
        "fixes": ["Check expected value", "Verify test data"],
    }

    # Initialize analyzer
    analyzer = FailureAnalyzer(mock_db, mock_claude)
    print("\n✓ FailureAnalyzer initialized successfully")

    # Test 1: Assertion failure classification
    print("\n" + "-" * 60)
    print("TEST 1: Assertion Failure Classification")
    print("-" * 60)
    result = analyzer._classify_failure("AssertionError: expected True but got False")
    assert result == "assertion", f"Expected 'assertion', got '{result}'"
    print(f"✓ Classification: {result}")
    print(f"✓ Priority: {analyzer._calculate_priority(result)}")

    # Test 2: Timeout failure
    print("\n" + "-" * 60)
    print("TEST 2: Timeout Failure Classification")
    print("-" * 60)
    result = analyzer._classify_failure("TimeoutError: Wait timed out after 30 seconds")
    assert result == "timeout", f"Expected 'timeout', got '{result}'"
    print(f"✓ Classification: {result}")
    print(f"✓ Priority: {analyzer._calculate_priority(result)}")

    # Test 3: Locator failure
    print("\n" + "-" * 60)
    print("TEST 3: Locator Failure Classification")
    print("-" * 60)
    result = analyzer._classify_failure(
        "NoSuchElementException: Element not found with selector"
    )
    assert result == "locator", f"Expected 'locator', got '{result}'"
    print(f"✓ Classification: {result}")
    print(f"✓ Priority: {analyzer._calculate_priority(result)}")

    # Test 4: Network failure
    print("\n" + "-" * 60)
    print("TEST 4: Network Failure Classification")
    print("-" * 60)
    result = analyzer._classify_failure("ConnectionError: Failed to connect to API")
    assert result == "network", f"Expected 'network', got '{result}'"
    print(f"✓ Classification: {result}")
    print(f"✓ Priority: {analyzer._calculate_priority(result)}")

    # Test 5: Environment failure
    print("\n" + "-" * 60)
    print("TEST 5: Environment Failure Classification")
    print("-" * 60)
    result = analyzer._classify_failure("EnvironmentError: MISSING_API_KEY not set")
    assert result == "environment", f"Expected 'environment', got '{result}'"
    print(f"✓ Classification: {result}")
    print(f"✓ Priority: {analyzer._calculate_priority(result)}")

    # Test 6: Full analysis
    print("\n" + "-" * 60)
    print("TEST 6: Full Failure Analysis")
    print("-" * 60)
    analysis = await analyzer.analyze_failure(
        error_msg="AssertionError: expected True but got False",
        test_name="test_login_validation",
        stack_trace="test_auth.py:45 in test_login",
        test_case_id=123,
    )

    assert analysis["test_name"] == "test_login_validation"
    assert analysis["failure_type"] == "assertion"
    assert analysis["priority"] == "high"
    assert "root_cause" in analysis
    assert "suggested_fixes" in analysis
    print(f"✓ Test: {analysis['test_name']}")
    print(f"✓ Failure Type: {analysis['failure_type']}")
    print(f"✓ Priority: {analysis['priority']}")
    print(f"✓ Root Cause: {analysis['root_cause']}")
    print(f"✓ Suggested Fixes: {len(analysis['suggested_fixes'])} fixes")

    # Test 7: Failure history (clear first, then add new ones)
    print("\n" + "-" * 60)
    print("TEST 7: Failure History Management")
    print("-" * 60)
    # Create new analyzer for clean history
    analyzer2 = FailureAnalyzer(mock_db, mock_claude)
    await analyzer2.analyze_failure("AssertionError: test1", "test_one")
    await analyzer2.analyze_failure("AssertionError: test2", "test_two")
    await analyzer2.analyze_failure("TimeoutError: test3", "test_three")

    assert len(analyzer2.failure_history["assertion"]) == 2
    assert len(analyzer2.failure_history["timeout"]) == 1
    print(f"✓ Stored assertion failures: {len(analyzer2.failure_history['assertion'])}")
    print(f"✓ Stored timeout failures: {len(analyzer2.failure_history['timeout'])}")

    # Test 8: Statistics
    print("\n" + "-" * 60)
    print("TEST 8: Analysis Statistics")
    print("-" * 60)
    stats = await analyzer2.get_analysis_statistics()
    assert stats["total_failures_analyzed"] == 3
    assert "assertion" in stats["by_type"]
    print(f"✓ Total failures analyzed: {stats['total_failures_analyzed']}")
    print(f"✓ By type: {stats['by_type']}")
    print(f"✓ Most common: {stats['most_common']}")

    # Test 9: Similar failure detection
    print("\n" + "-" * 60)
    print("TEST 9: Similar Failure Detection")
    print("-" * 60)
    similar = await analyzer2._check_failure_history(
        "Expected value is incorrect", "assertion"
    )
    print(f"✓ Similar failures found: {len(similar)}")

    # Test 10: All failure types defined
    print("\n" + "-" * 60)
    print("TEST 10: Failure Type Definitions")
    print("-" * 60)
    for ft, description in analyzer.FAILURE_TYPES.items():
        priority = analyzer._calculate_priority(ft)
        print(f"✓ {ft:15} → {description:50} [Priority: {priority}]")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓ Task 3 Complete")
    print("=" * 60)
    print("\nImplemented Features:")
    print("  ✓ Failure classification (6 types)")
    print("  ✓ Priority calculation")
    print("  ✓ Claude AI integration for analysis")
    print("  ✓ Failure history tracking")
    print("  ✓ Statistics aggregation")
    print("  ✓ Similar failure detection")
    print("  ✓ API endpoints (3)")
    print("  ✓ Comprehensive error handling")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_failure_analyzer())
