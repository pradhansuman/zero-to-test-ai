"""
engines/api/src/rest_client.py
──────────────────────────────
Async REST client for API testing.
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any

import httpx

from shared.contracts.engine_schemas import (
    APITestCase, APITestResult, APIAuth, HTTPMethod, TestStatus, AuthType
)


logger = logging.getLogger(__name__)


class RestClientError(Exception):
    """Base exception for REST client errors."""
    pass


class RestClient:
    """Async REST client for executing API test cases."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30,
        retry_count: int = 0,
        retry_delay: float = 1.0,
        ssl_verify: bool = True,
        proxy: Optional[str] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.ssl_verify = ssl_verify
        self.proxy = proxy
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            verify=self.ssl_verify,
            proxies=self.proxy,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def execute(self, test_case: APITestCase) -> APITestResult:
        """Execute a single REST API test case."""
        if test_case.skip:
            return self._create_skipped_result(test_case)

        start_time = time.time()

        try:
            url = self._build_url(test_case)
            headers = self._build_headers(test_case)

            logger.info(f"Executing {test_case.method.value} {url}")

            response = await self._execute_with_retry(
                method=test_case.method,
                url=url,
                headers=headers,
                params=test_case.query_params or {},
                json=test_case.body,
                timeout=test_case.timeout,
            )

            response_time_ms = (time.time() - start_time) * 1000

            assertions_passed, assertions_failed = self._evaluate_assertions(
                test_case.assertions, response
            )

            status = TestStatus.PASSED if assertions_failed == 0 else TestStatus.FAILED

            return APITestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                status=status,
                method=test_case.method,
                endpoint=test_case.endpoint,
                request_headers=dict(headers),
                request_body=test_case.body,
                response_status_code=response.status_code,
                response_headers=dict(response.headers),
                response_body=self._parse_response(response),
                response_time_ms=response_time_ms,
                assertions_passed=assertions_passed,
                assertions_failed=assertions_failed,
                tags=test_case.tags,
            )

        except httpx.TimeoutException as e:
            response_time_ms = (time.time() - start_time) * 1000
            logger.error(f"Timeout: {e}")
            return self._create_error_result(
                test_case, "Request timeout", response_time_ms, str(e)
            )

        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            logger.error(f"Error: {e}", exc_info=True)
            return self._create_error_result(
                test_case, str(e), response_time_ms, str(e)
            )

    async def _execute_with_retry(
        self, method: HTTPMethod, url: str, headers: Dict, params: Dict,
        json: Optional[Dict], timeout: int
    ) -> httpx.Response:
        """Execute request with exponential backoff retry."""
        if not self._client:
            raise RestClientError("Client not initialized")

        for attempt in range(self.retry_count + 1):
            try:
                response = await self._client.request(
                    method=method.value,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    timeout=timeout,
                )
                return response

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempt < self.retry_count:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(f"Retry in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    raise

    def _build_url(self, test_case: APITestCase) -> str:
        """Build full URL from base_url and endpoint."""
        if test_case.endpoint.startswith("http"):
            return test_case.endpoint
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{test_case.endpoint.lstrip('/')}"
        return test_case.endpoint

    def _build_headers(self, test_case: APITestCase) -> Dict[str, str]:
        """Build request headers with auth."""
        headers = dict(test_case.headers or {})
        if test_case.auth:
            auth_header = self._get_auth_header(test_case.auth)
            if auth_header:
                headers.update(auth_header)
        headers.setdefault("User-Agent", "QA-API-Engine/1.0")
        return headers

    def _get_auth_header(self, auth: APIAuth) -> Optional[Dict[str, str]]:
        """Generate authorization header."""
        if auth.type == AuthType.NONE:
            return None
        elif auth.type == AuthType.BEARER:
            return {"Authorization": f"Bearer {auth.token}"}
        elif auth.type == AuthType.BASIC:
            import base64
            creds = base64.b64encode(
                f"{auth.username}:{auth.password}".encode()
            ).decode()
            return {"Authorization": f"Basic {creds}"}
        elif auth.type == AuthType.API_KEY:
            return {auth.header_name or "X-API-Key": auth.api_key}
        return None

    def _evaluate_assertions(self, assertions, response: httpx.Response) -> tuple[int, int]:
        """Evaluate all assertions against response."""
        from .assertion_evaluator import AssertionEvaluator
        evaluator = AssertionEvaluator(response)
        passed = 0
        failed = 0
        for assertion in assertions:
            if evaluator.evaluate(assertion):
                passed += 1
            else:
                failed += 1
        return passed, failed

    @staticmethod
    def _create_skipped_result(test_case: APITestCase) -> APITestResult:
        """Create a skipped test result."""
        return APITestResult(
            test_id=test_case.id,
            test_name=test_case.name,
            status=TestStatus.SKIPPED,
            method=test_case.method,
            endpoint=test_case.endpoint,
            request_headers={},
            request_body=None,
            response_status_code=None,
            response_headers=None,
            response_body=None,
            response_time_ms=0,
            assertions_passed=0,
            assertions_failed=0,
            tags=test_case.tags,
        )

    @staticmethod
    def _create_error_result(
        test_case: APITestCase, error_msg: str, response_time: float, stack: str
    ) -> APITestResult:
        """Create an error test result."""
        return APITestResult(
            test_id=test_case.id,
            test_name=test_case.name,
            status=TestStatus.ERROR,
            method=test_case.method,
            endpoint=test_case.endpoint,
            request_headers={},
            request_body=test_case.body,
            response_status_code=None,
            response_headers=None,
            response_body=None,
            response_time_ms=response_time,
            assertions_passed=0,
            assertions_failed=len(test_case.assertions),
            error_message=error_msg,
            stack_trace=stack,
            tags=test_case.tags,
        )

    @staticmethod
    def _parse_response(response: httpx.Response) -> Any:
        """Parse response body."""
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                return response.json()
            except:
                return response.text
        return response.text
