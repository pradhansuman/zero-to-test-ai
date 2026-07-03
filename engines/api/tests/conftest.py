"""Test fixtures for API engine."""
import pytest
from shared.contracts.engine_schemas import (
    APITestCase, HTTPMethod, Assertion, AssertionType
)


@pytest.fixture
def sample_api_test_case():
    """Sample API test case."""
    return APITestCase(
        id="TEST-001",
        name="Sample GET request",
        method=HTTPMethod.GET,
        endpoint="https://jsonplaceholder.typicode.com/posts/1",
        assertions=[
            Assertion(
                type=AssertionType.EQUALS,
                target="status_code",
                expected=200,
            )
        ],
    )


@pytest.fixture
def sample_assertion():
    """Sample assertion."""
    return Assertion(
        type=AssertionType.EQUALS,
        target="status_code",
        expected=200,
    )
