"""Test generation service with AI integration and caching."""
import hashlib
import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import TestCase
from app.services.claude_client import ClaudeClient
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class TestGenerationService:
    """Service for AI-powered test case generation."""

    def __init__(self, db: AsyncSession, redis_client=None):
        """Initialize test generation service.

        Args:
            db: AsyncSession for database operations
            redis_client: Optional Redis client for caching
        """
        self.db = db
        self.redis = redis_client
        self.claude = ClaudeClient()
        self.cache_ttl = 86400  # 24 hours

    async def generate_test_from_story(
        self,
        project_id: int,
        user_id: int,
        story_description: str,
        acceptance_criteria: str = "",
        framework: str = "pytest",
    ) -> dict:
        """Generate test case from user story.

        Args:
            project_id: Project ID
            user_id: User ID
            story_description: User story or requirement
            acceptance_criteria: Acceptance criteria
            framework: Testing framework

        Returns:
            Generated test case with code
        """
        # Build context for generation
        context = f"Acceptance Criteria:\n{acceptance_criteria}" if acceptance_criteria else ""

        # Check cache first
        cache_key = self._build_cache_key(story_description, framework)
        cached_result = await self._get_cached_result(cache_key)
        if cached_result:
            logger.info("test_generation_cache_hit", cache_key=cache_key)
            return cached_result

        # Generate via Claude
        logger.info(
            "test_generation_started",
            project_id=project_id,
            user_id=user_id,
            framework=framework,
        )

        result = await self.claude.generate_test_case(
            description=story_description,
            test_type="functional",
            framework=framework,
            context=context,
        )

        if "error" in result:
            logger.error("test_generation_failed", error=result["error"])
            return result

        # Cache the result
        await self._cache_result(cache_key, result)

        logger.info(
            "test_generation_completed",
            project_id=project_id,
            framework=framework,
        )

        return result

    async def generate_api_test(
        self,
        project_id: int,
        user_id: int,
        endpoint: str,
        method: str,
        expected_response: str = "",
    ) -> dict:
        """Generate API test case.

        Args:
            project_id: Project ID
            user_id: User ID
            endpoint: API endpoint (e.g., /api/users)
            method: HTTP method (GET, POST, etc.)
            expected_response: Expected response format

        Returns:
            Generated API test
        """
        description = f"Test {method} {endpoint}"
        if expected_response:
            description += f"\nExpected Response: {expected_response}"

        # Check cache
        cache_key = self._build_cache_key(description, "httpx")
        cached_result = await self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        result = await self.claude.generate_test_case(
            description=description,
            test_type="api",
            framework="httpx",
            context=f"Endpoint: {endpoint}\nMethod: {method}",
        )

        await self._cache_result(cache_key, result)

        logger.info(
            "api_test_generated",
            project_id=project_id,
            endpoint=endpoint,
            method=method,
        )

        return result

    async def generate_ui_test(
        self,
        project_id: int,
        user_id: int,
        user_flow: str,
        page_url: str = "",
        elements_to_interact: list = None,
    ) -> dict:
        """Generate UI test case using Playwright.

        Args:
            project_id: Project ID
            user_id: User ID
            user_flow: Description of user flow
            page_url: URL to test
            elements_to_interact: List of elements to interact with

        Returns:
            Generated Playwright test
        """
        elements_context = ""
        if elements_to_interact:
            elements_context = f"\nElements: {', '.join(elements_to_interact)}"

        description = f"UI Test:\n{user_flow}{elements_context}"
        if page_url:
            description += f"\nURL: {page_url}"

        cache_key = self._build_cache_key(description, "playwright")
        cached_result = await self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        result = await self.claude.generate_test_case(
            description=description,
            test_type="ui",
            framework="playwright",
            context=f"Page URL: {page_url}" if page_url else "",
        )

        await self._cache_result(cache_key, result)

        logger.info(
            "ui_test_generated",
            project_id=project_id,
            url=page_url,
        )

        return result

    async def suggest_test_improvements(self, test_code: str, framework: str = "pytest") -> dict:
        """Suggest improvements to test code.

        Args:
            test_code: Existing test code
            framework: Testing framework

        Returns:
            Optimization suggestions
        """
        logger.info("test_optimization_started", framework=framework)

        result = await self.claude.optimize_test_code(test_code, framework)

        logger.info("test_optimization_completed", framework=framework)

        return result

    async def batch_generate_tests(
        self,
        project_id: int,
        user_id: int,
        stories: list,
        framework: str = "pytest",
    ) -> list:
        """Generate multiple test cases in batch.

        Args:
            project_id: Project ID
            user_id: User ID
            stories: List of story descriptions
            framework: Testing framework

        Returns:
            List of generated tests
        """
        logger.info(
            "batch_generation_started",
            project_id=project_id,
            count=len(stories),
            framework=framework,
        )

        results = []
        for i, story in enumerate(stories):
            try:
                result = await self.generate_test_from_story(
                    project_id=project_id,
                    user_id=user_id,
                    story_description=story,
                    framework=framework,
                )
                results.append({
                    "story": story,
                    "result": result,
                    "success": "error" not in result,
                })
            except Exception as e:
                logger.error(
                    "batch_generation_item_failed",
                    item=i,
                    error=str(e),
                )
                results.append({
                    "story": story,
                    "error": str(e),
                    "success": False,
                })

        logger.info(
            "batch_generation_completed",
            project_id=project_id,
            successful=sum(1 for r in results if r["success"]),
            failed=sum(1 for r in results if not r["success"]),
        )

        return results

    def _build_cache_key(self, description: str, framework: str) -> str:
        """Build cache key from description and framework.

        Args:
            description: Test description
            framework: Testing framework

        Returns:
            Cache key
        """
        content = f"{description}:{framework}"
        hash_digest = hashlib.md5(content.encode()).hexdigest()
        return f"test_gen:{hash_digest}"

    async def _get_cached_result(self, cache_key: str) -> dict | None:
        """Get cached result from Redis.

        Args:
            cache_key: Cache key

        Returns:
            Cached result or None
        """
        if not self.redis:
            return None

        try:
            cached = self.redis.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.warning("cache_get_failed", cache_key=cache_key, error=str(e))

        return None

    async def _cache_result(self, cache_key: str, result: dict) -> None:
        """Cache result in Redis.

        Args:
            cache_key: Cache key
            result: Result to cache
        """
        if not self.redis:
            return

        try:
            self.redis.setex(cache_key, self.cache_ttl, json.dumps(result))
        except Exception as e:
            logger.warning("cache_set_failed", cache_key=cache_key, error=str(e))
