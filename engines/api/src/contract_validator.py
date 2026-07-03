"""OpenAPI/Swagger contract validation for API testing."""
import logging
from typing import Optional, Dict, Any, List

import httpx
from jsonschema import validate, ValidationError
import yaml

from shared.contracts.engine_schemas import ContractValidationCase, APITestResult, TestStatus

logger = logging.getLogger(__name__)


class ContractValidator:
    """Validates API requests/responses against OpenAPI specs."""

    def __init__(self):
        self.specs_cache: Dict[str, Dict] = {}

    async def validate_case(self, case: ContractValidationCase) -> List[APITestResult]:
        """Validate test cases against OpenAPI spec."""
        spec = await self._fetch_spec(case.openapi_spec_url)

        if not spec:
            return [
                APITestResult(
                    test_id=tc.id,
                    test_name=tc.name,
                    status=TestStatus.ERROR,
                    method=tc.method,
                    endpoint=tc.endpoint,
                    request_headers={},
                    request_body=None,
                    response_status_code=None,
                    response_headers=None,
                    response_body=None,
                    response_time_ms=0,
                    assertions_passed=0,
                    assertions_failed=1,
                    error_message="Failed to fetch OpenAPI spec",
                    stack_trace=None,
                    tags=tc.tags,
                )
                for tc in case.test_cases
            ]

        results = []
        for tc in case.test_cases:
            result = self._validate_request(tc, spec)
            results.append(result)

        return results

    async def _fetch_spec(self, url: str) -> Optional[Dict]:
        """Fetch and parse OpenAPI spec."""
        if url in self.specs_cache:
            return self.specs_cache[url]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                response.raise_for_status()

                # Parse YAML or JSON
                if url.endswith(".yaml") or url.endswith(".yml"):
                    spec = yaml.safe_load(response.text)
                else:
                    spec = response.json()

                self.specs_cache[url] = spec
                return spec

        except Exception as e:
            logger.error(f"Failed to fetch spec from {url}: {e}")
            return None

    def _validate_request(self, test_case, spec: Dict) -> APITestResult:
        """Validate test case request against spec."""
        try:
            # Extract path and method from endpoint
            path = test_case.endpoint.split("?")[0]
            method = test_case.method.value.lower()

            # Find matching path in spec
            paths = spec.get("paths", {})
            matching_path = None
            for path_pattern in paths.keys():
                if path_pattern in path or path in path_pattern:
                    matching_path = path_pattern
                    break

            if not matching_path:
                return self._create_error_result(
                    test_case,
                    f"Path not found in spec: {path}",
                )

            # Validate method
            method_spec = paths[matching_path].get(method)
            if not method_spec:
                return self._create_error_result(
                    test_case,
                    f"Method {method.upper()} not defined for {matching_path}",
                )

            # Validate request parameters
            if test_case.query_params:
                params_spec = method_spec.get("parameters", [])
                self._validate_params(test_case.query_params, params_spec)

            # Validate request body
            if test_case.body:
                request_body_spec = method_spec.get("requestBody", {})
                self._validate_body(test_case.body, request_body_spec)

            return APITestResult(
                test_id=test_case.id,
                test_name=test_case.name,
                status=TestStatus.PASSED,
                method=test_case.method,
                endpoint=test_case.endpoint,
                request_headers=test_case.headers or {},
                request_body=test_case.body,
                response_status_code=200,
                response_headers={},
                response_body=None,
                response_time_ms=0,
                assertions_passed=1,
                assertions_failed=0,
                tags=test_case.tags,
            )

        except ValidationError as e:
            return self._create_error_result(test_case, f"Validation error: {e.message}")
        except Exception as e:
            return self._create_error_result(test_case, str(e))

    def _validate_params(self, params: Dict, params_spec: List) -> None:
        """Validate query parameters against spec."""
        required_params = {
            p["name"] for p in params_spec
            if p.get("required", False)
        }

        provided_params = set(params.keys())
        missing = required_params - provided_params

        if missing:
            raise ValidationError(f"Missing required parameters: {missing}")

    def _validate_body(self, body: Dict, request_body_spec: Dict) -> None:
        """Validate request body against spec."""
        content = request_body_spec.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema")

        if schema:
            validate(instance=body, schema=schema)

    @staticmethod
    def _create_error_result(test_case, error_msg: str) -> APITestResult:
        """Create error result."""
        return APITestResult(
            test_id=test_case.id,
            test_name=test_case.name,
            status=TestStatus.FAILED,
            method=test_case.method,
            endpoint=test_case.endpoint,
            request_headers=test_case.headers or {},
            request_body=test_case.body,
            response_status_code=None,
            response_headers=None,
            response_body=None,
            response_time_ms=0,
            assertions_passed=0,
            assertions_failed=1,
            error_message=error_msg,
            stack_trace=None,
            tags=test_case.tags,
        )
