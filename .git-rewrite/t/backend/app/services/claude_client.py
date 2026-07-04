"""Claude AI client for intelligent test generation and analysis."""
import anthropic
from app.config import settings
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class ClaudeClient:
    """Interface to Claude API for AI-powered test automation."""

    def __init__(self):
        """Initialize Claude client with API key."""
        if not settings.claude_api_key:
            logger.warning("claude_api_key_not_configured", message="Claude API key not set")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=settings.claude_api_key)

    async def generate_test_case(
        self,
        description: str,
        test_type: str = "functional",
        framework: str = "pytest",
        context: str = "",
    ) -> dict:
        """Generate a test case from natural language description.

        Args:
            description: User story or requirement description
            test_type: Type of test (functional, api, performance, etc.)
            framework: Testing framework (pytest, playwright, etc.)
            context: Additional context for test generation

        Returns:
            dict with test_name, test_code, assertions, tags
        """
        if not self.client:
            logger.error("claude_not_configured", message="Cannot generate test without API key")
            return {"error": "Claude API not configured"}

        prompt = self._build_test_generation_prompt(description, test_type, framework, context)

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=settings.claude_max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            test_code = message.content[0].text
            logger.info(
                "test_generated",
                test_type=test_type,
                framework=framework,
                tokens_used=message.usage.input_tokens + message.usage.output_tokens,
            )

            return {
                "test_code": test_code,
                "test_type": test_type,
                "framework": framework,
                "generated_by": "claude",
                "model": settings.claude_model,
            }
        except Exception as e:
            logger.error(
                "test_generation_failed",
                error=str(e),
                test_type=test_type,
                framework=framework,
            )
            return {"error": str(e)}

    async def suggest_locator_fix(
        self,
        broken_selector: str,
        element_description: str,
        html_snippet: str = "",
    ) -> dict:
        """Suggest a new CSS/XPath selector for a broken locator.

        Args:
            broken_selector: The current broken selector
            element_description: Description of what element to find
            html_snippet: HTML context around the element

        Returns:
            dict with suggested_selector, confidence, explanation
        """
        if not self.client:
            return {"error": "Claude API not configured"}

        prompt = self._build_locator_healing_prompt(
            broken_selector, element_description, html_snippet
        )

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            response = message.content[0].text
            logger.info(
                "locator_healing_suggested",
                element=element_description,
                tokens_used=message.usage.input_tokens + message.usage.output_tokens,
            )

            return {
                "suggested_selector": response.split("\n")[0],
                "explanation": response,
                "confidence": 0.75,
                "healed_by": "claude",
            }
        except Exception as e:
            logger.error(
                "locator_healing_failed",
                error=str(e),
                element=element_description,
            )
            return {"error": str(e)}

    async def analyze_test_failure(
        self,
        error_message: str,
        test_name: str,
        stack_trace: str = "",
    ) -> dict:
        """Analyze a test failure and suggest causes and fixes.

        Args:
            error_message: The error/assertion message
            test_name: Name of the failing test
            stack_trace: Full stack trace if available

        Returns:
            dict with failure_type, likely_causes, suggested_fixes
        """
        if not self.client:
            return {"error": "Claude API not configured"}

        prompt = self._build_failure_analysis_prompt(error_message, test_name, stack_trace)

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            analysis = message.content[0].text
            logger.info(
                "failure_analyzed",
                test_name=test_name,
                tokens_used=message.usage.input_tokens + message.usage.output_tokens,
            )

            return {
                "analysis": analysis,
                "failure_type": self._classify_failure(error_message),
                "test_name": test_name,
                "analyzed_by": "claude",
            }
        except Exception as e:
            logger.error("failure_analysis_failed", error=str(e), test_name=test_name)
            return {"error": str(e)}

    async def optimize_test_code(self, test_code: str, test_framework: str = "pytest") -> dict:
        """Suggest improvements to test code quality and maintainability.

        Args:
            test_code: The test code to analyze
            test_framework: The testing framework used

        Returns:
            dict with improvements, refactored_code, complexity_score
        """
        if not self.client:
            return {"error": "Claude API not configured"}

        prompt = self._build_test_optimization_prompt(test_code, test_framework)

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )

            suggestions = message.content[0].text
            logger.info(
                "test_optimized",
                framework=test_framework,
                tokens_used=message.usage.input_tokens + message.usage.output_tokens,
            )

            return {
                "suggestions": suggestions,
                "optimized_by": "claude",
                "framework": test_framework,
            }
        except Exception as e:
            logger.error("test_optimization_failed", error=str(e))
            return {"error": str(e)}

    def _build_test_generation_prompt(
        self, description: str, test_type: str, framework: str, context: str
    ) -> str:
        """Build prompt for test generation."""
        return f"""Generate a {test_type} test case using {framework}.

Requirement: {description}

Context: {context}

Requirements for the generated test:
1. Use {framework} framework
2. Include clear assertions
3. Follow best practices (AAA pattern)
4. Handle edge cases
5. Use meaningful variable names
6. Include comments for complex logic

Generate the complete test code:"""

    def _build_locator_healing_prompt(
        self, broken_selector: str, element_description: str, html_snippet: str
    ) -> str:
        """Build prompt for locator healing."""
        html_context = f"\nHTML Context:\n{html_snippet}" if html_snippet else ""
        return f"""Fix this broken CSS/XPath selector.

Current Selector: {broken_selector}
Element to Find: {element_description}{html_context}

Provide:
1. New CSS or XPath selector
2. Why the original selector broke
3. Why the new selector is more robust

New Selector:"""

    def _build_failure_analysis_prompt(
        self, error_message: str, test_name: str, stack_trace: str
    ) -> str:
        """Build prompt for failure analysis."""
        trace_context = f"\nStack Trace:\n{stack_trace}" if stack_trace else ""
        return f"""Analyze this test failure and suggest causes and fixes.

Test Name: {test_name}
Error Message: {error_message}{trace_context}

Provide:
1. Classification of failure type (assertion, timeout, network, etc.)
2. Most likely root causes
3. Suggested fixes to try
4. Prevention strategies for future

Analysis:"""

    def _build_test_optimization_prompt(self, test_code: str, framework: str) -> str:
        """Build prompt for test code optimization."""
        return f"""Review and optimize this {framework} test code.

Test Code:
{test_code}

Provide:
1. Code quality issues
2. Maintainability improvements
3. Performance optimizations
4. Best practice violations
5. Refactored code

Analysis and Recommendations:"""

    def _classify_failure(self, error_message: str) -> str:
        """Classify failure type based on error message."""
        error_lower = error_message.lower()
        if "timeout" in error_lower or "timed out" in error_lower:
            return "timeout"
        elif "assertion" in error_lower or "assert" in error_lower:
            return "assertion"
        elif "network" in error_lower or "connection" in error_lower:
            return "network"
        elif "element" in error_lower or "locator" in error_lower or "selector" in error_lower:
            return "locator"
        else:
            return "unknown"
