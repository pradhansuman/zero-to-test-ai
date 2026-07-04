"""Integration tests for failure analysis API."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_analyze_failure_assertion(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis for assertion failure."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "AssertionError: expected True but got False",
            "test_name": "test_login_validation",
            "stack_trace": "test_login.py:45 in test_login_validation",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["failure_type"] == "assertion"
    assert data["test_name"] == "test_login_validation"
    assert "root_cause" in data
    assert data["priority"] == "high"
    assert isinstance(data["suggested_fixes"], list)


@pytest.mark.asyncio
async def test_analyze_failure_timeout(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis for timeout failure."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "TimeoutError: Wait timed out after 30 seconds",
            "test_name": "test_page_load",
            "stack_trace": "page.py:102 in wait_for_selector",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["failure_type"] == "timeout"
    assert data["priority"] == "high"
    assert "suggested_fixes" in data


@pytest.mark.asyncio
async def test_analyze_failure_locator(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis for locator/element not found."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "NoSuchElementException: Element not found with selector '.login-btn'",
            "test_name": "test_button_click",
            "stack_trace": "browser.py:234 in find_element",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["failure_type"] == "locator"
    assert data["priority"] == "medium"


@pytest.mark.asyncio
async def test_analyze_failure_network(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis for network failure."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "ConnectionError: Failed to establish connection to API",
            "test_name": "test_api_call",
            "stack_trace": "requests.py:78 in get",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["failure_type"] == "network"
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_analyze_failure_environment(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis for environment/config failure."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "EnvironmentError: MISSING_API_KEY env variable not set",
            "test_name": "test_integration",
            "stack_trace": "config.py:45 in load_config",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["failure_type"] == "environment"
    assert data["priority"] == "critical"


@pytest.mark.asyncio
async def test_get_failure_patterns_empty(
    async_client: AsyncClient,
    auth_headers: dict,
    created_project: dict,
):
    """Test getting failure patterns for project with no failures."""
    response = await async_client.get(
        f"/api/ai/failure-patterns/{created_project['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["project_id"] == created_project["id"]
    assert "patterns" in data
    assert data["total_tests"] >= 0


@pytest.mark.asyncio
async def test_get_failure_statistics(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test getting failure analysis statistics."""
    response = await async_client.get(
        "/api/ai/failure-statistics",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert "period_hours" in data
    assert "statistics" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_analyze_failure_with_test_case_id(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis with test case ID for context."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "AssertionError: Login failed",
            "test_name": "test_login",
            "stack_trace": "test_auth.py:10",
            "test_case_id": 123,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["test_case_id"] == 123
    assert data["failure_type"] in [
        "assertion",
        "network",
        "timeout",
        "locator",
        "environment",
        "unknown",
    ]


@pytest.mark.asyncio
async def test_analyze_failure_unknown_type(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Test failure analysis for unknown failure type."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "SomeRandomError: Something went wrong",
            "test_name": "test_unknown",
            "stack_trace": "unknown.py:99",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["failure_type"] == "unknown"
    assert data["priority"] == "low"


@pytest.mark.asyncio
async def test_analyze_failure_unauthorized(
    async_client: AsyncClient,
):
    """Test that unauthenticated requests are rejected."""
    response = await async_client.post(
        "/api/ai/analyze-failure",
        json={
            "error_message": "Test error",
            "test_name": "test_something",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_failure_patterns_unauthorized(
    async_client: AsyncClient,
):
    """Test that unauthenticated pattern requests are rejected."""
    response = await async_client.get(
        "/api/ai/failure-patterns/1",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_failure_statistics_unauthorized(
    async_client: AsyncClient,
):
    """Test that unauthenticated statistics requests are rejected."""
    response = await async_client.get(
        "/api/ai/failure-statistics",
    )

    assert response.status_code == 401
