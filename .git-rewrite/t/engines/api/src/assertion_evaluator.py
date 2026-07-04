"""Assertion evaluation against HTTP responses."""
import re
from typing import Any
from jsonpath_ng import parse
import httpx
from shared.contracts.engine_schemas import Assertion, AssertionType


class AssertionEvaluator:
    """Evaluates assertions against HTTP responses."""

    def __init__(self, response: httpx.Response):
        self.response = response
        self.body = self._parse_body()

    def evaluate(self, assertion: Assertion) -> bool:
        """Evaluate a single assertion."""
        try:
            value = self._extract_value(assertion.target)

            if assertion.type == AssertionType.EQUALS:
                return value == assertion.expected
            elif assertion.type == AssertionType.CONTAINS:
                return str(assertion.expected) in str(value)
            elif assertion.type == AssertionType.NOT_CONTAINS:
                return str(assertion.expected) not in str(value)
            elif assertion.type == AssertionType.GREATER_THAN:
                return float(value) > float(assertion.expected)
            elif assertion.type == AssertionType.LESS_THAN:
                return float(value) < float(assertion.expected)
            elif assertion.type == AssertionType.MATCHES_REGEX:
                return bool(re.search(assertion.expected, str(value)))
            elif assertion.type == AssertionType.IS_NULL:
                return value is None
            elif assertion.type == AssertionType.IS_NOT_NULL:
                return value is not None
            elif assertion.type == AssertionType.IN_LIST:
                return value in assertion.expected
            elif assertion.type == AssertionType.LENGTH_EQUALS:
                return len(value) == assertion.expected
            elif assertion.type == AssertionType.TYPE_EQUALS:
                return type(value).__name__ == assertion.expected

            return False
        except Exception:
            return False

    def _extract_value(self, target: str) -> Any:
        """Extract value from response using JSONPath."""
        if target == "status_code":
            return self.response.status_code
        elif target.startswith("headers."):
            header_name = target.split(".", 1)[1]
            return self.response.headers.get(header_name)

        if self.body is None:
            return None

        try:
            jsonpath_expr = parse(target)
            matches = jsonpath_expr.find(self.body)
            return matches[0].value if matches else None
        except:
            return None

    def _parse_body(self) -> Any:
        """Parse response body as JSON."""
        try:
            return self.response.json()
        except:
            return {"_text": self.response.text}
