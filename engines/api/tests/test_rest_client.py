"""Tests for REST client."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from engines.api.src.rest_client import RestClient
from shared.contracts.engine_schemas import (
    APITestCase, HTTPMethod, Assertion, AssertionType, AuthType, APIAuth, TestStatus
)


class TestRestClient:
    """Test suite for RestClient."""

    @pytest.mark.asyncio
    async def test_execute_get_request_success(self):
        """Test successful GET request."""
        test_case = APITestCase(
            id="TEST-001",
            name="GET request",
            method=HTTPMethod.GET,
            endpoint="https://api.example.com/users",
            assertions=[
                Assertion(
                    type=AssertionType.EQUALS,
                    target="status_code",
                    expected=200,
                )
            ],
        )

        async with RestClient(base_url="https://api.example.com") as client:
            with patch.object(client, "_execute_with_retry") as mock_exec:
                mock_response = MagicMock(spec=httpx.Response)
                mock_response.status_code = 200
                mock_response.headers = {"content-type": "application/json"}
                mock_response.json.return_value = {"users": []}
                mock_response.text = '{"users": []}'
                mock_exec.return_value = mock_response

                result = await client.execute(test_case)

                assert result.status == TestStatus.PASSED
                assert result.response_status_code == 200

    @pytest.mark.asyncio
    async def test_execute_post_with_body(self):
        """Test POST request with body."""
        test_case = APITestCase(
            id="TEST-002",
            name="POST request",
            method=HTTPMethod.POST,
            endpoint="/users",
            body={"name": "John", "email": "john@example.com"},
            assertions=[],
        )

        async with RestClient(base_url="https://api.example.com") as client:
            with patch.object(client, "_execute_with_retry") as mock_exec:
                mock_response = MagicMock(spec=httpx.Response)
                mock_response.status_code = 201
                mock_response.headers = {}
                mock_response.json.return_value = {"id": 1}
                mock_exec.return_value = mock_response

                result = await client.execute(test_case)

                assert result.status == TestStatus.PASSED
                assert result.response_status_code == 201

    @pytest.mark.asyncio
    async def test_execute_with_bearer_auth(self):
        """Test request with Bearer authentication."""
        test_case = APITestCase(
            id="TEST-003",
            name="Authenticated request",
            method=HTTPMethod.GET,
            endpoint="/protected",
            auth=APIAuth(
                type=AuthType.BEARER,
                token="secret-token",
            ),
            assertions=[],
        )

        async with RestClient() as client:
            headers = client._build_headers(test_case)
            assert "Authorization" in headers
            assert headers["Authorization"] == "Bearer secret-token"

    @pytest.mark.asyncio
    async def test_execute_with_basic_auth(self):
        """Test request with Basic authentication."""
        test_case = APITestCase(
            id="TEST-004",
            name="Basic auth request",
            method=HTTPMethod.GET,
            endpoint="/protected",
            auth=APIAuth(
                type=AuthType.BASIC,
                username="user",
                password="pass",
            ),
            assertions=[],
        )

        async with RestClient() as client:
            headers = client._build_headers(test_case)
            assert "Authorization" in headers
            assert headers["Authorization"].startswith("Basic")

    @pytest.mark.asyncio
    async def test_execute_timeout_error(self):
        """Test timeout handling."""
        test_case = APITestCase(
            id="TEST-005",
            name="Timeout test",
            method=HTTPMethod.GET,
            endpoint="https://api.example.com/slow",
            timeout=1,
            assertions=[],
        )

        async with RestClient() as client:
            with patch.object(client, "_execute_with_retry") as mock_exec:
                mock_exec.side_effect = httpx.TimeoutException("Timeout")

                result = await client.execute(test_case)

                assert result.status == TestStatus.ERROR
                assert "timeout" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_execute_skipped_test(self):
        """Test skipped test case."""
        test_case = APITestCase(
            id="TEST-006",
            name="Skipped test",
            method=HTTPMethod.GET,
            endpoint="/users",
            skip=True,
            assertions=[],
        )

        async with RestClient() as client:
            result = await client.execute(test_case)

            assert result.status == TestStatus.SKIPPED
            assert result.response_time_ms == 0

    def test_build_url_with_base_url(self):
        """Test URL building with base URL."""
        client = RestClient(base_url="https://api.example.com")
        test_case = APITestCase(
            id="TEST",
            name="Test",
            method=HTTPMethod.GET,
            endpoint="/users",
            assertions=[],
        )

        url = client._build_url(test_case)
        assert url == "https://api.example.com/users"

    def test_build_url_with_full_url(self):
        """Test URL building with full endpoint URL."""
        client = RestClient()
        test_case = APITestCase(
            id="TEST",
            name="Test",
            method=HTTPMethod.GET,
            endpoint="https://other.example.com/data",
            assertions=[],
        )

        url = client._build_url(test_case)
        assert url == "https://other.example.com/data"

    @pytest.mark.asyncio
    async def test_execute_with_query_params(self):
        """Test request with query parameters."""
        test_case = APITestCase(
            id="TEST-007",
            name="Query params",
            method=HTTPMethod.GET,
            endpoint="/search",
            query_params={"q": "python", "limit": "10"},
            assertions=[],
        )

        async with RestClient(base_url="https://api.example.com") as client:
            with patch.object(client, "_execute_with_retry") as mock_exec:
                mock_response = MagicMock(spec=httpx.Response)
                mock_response.status_code = 200
                mock_response.headers = {}
                mock_response.json.return_value = []
                mock_exec.return_value = mock_response

                result = await client.execute(test_case)

                # Verify params were passed
                call_args = mock_exec.call_args
                assert call_args[1]["params"] == {"q": "python", "limit": "10"}

    @pytest.mark.asyncio
    async def test_execute_multiple_assertions(self):
        """Test multiple assertions on same response."""
        test_case = APITestCase(
            id="TEST-008",
            name="Multi assertions",
            method=HTTPMethod.GET,
            endpoint="/users",
            assertions=[
                Assertion(
                    type=AssertionType.EQUALS,
                    target="status_code",
                    expected=200,
                ),
                Assertion(
                    type=AssertionType.CONTAINS,
                    target="body.users",
                    expected="admin",
                ),
            ],
        )

        async with RestClient(base_url="https://api.example.com") as client:
            with patch.object(client, "_execute_with_retry") as mock_exec:
                mock_response = MagicMock(spec=httpx.Response)
                mock_response.status_code = 200
                mock_response.headers = {"content-type": "application/json"}
                mock_response.json.return_value = {"users": ["admin", "user"]}
                mock_exec.return_value = mock_response

                result = await client.execute(test_case)

                assert result.assertions_passed >= 1
