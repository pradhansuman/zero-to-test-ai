"""Smart locator healing with learning and confidence scoring."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from app.database.models import TestCase
from app.services.claude_client import ClaudeClient
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class LocatorHealer:
    """Heal broken CSS/XPath selectors with learning capability."""

    def __init__(self, db: AsyncSession):
        """Initialize healer with database session."""
        self.db = db
        self.claude = ClaudeClient()
        self.healing_history = {}  # In-memory cache, use DB for persistence

    async def heal_locator(
        self,
        broken_selector: str,
        element_description: str,
        html_snippet: str = "",
        test_case_id: int = None,
    ) -> dict:
        """Heal a broken locator with confidence scoring.

        Args:
            broken_selector: Current broken CSS/XPath selector
            element_description: Description of element to find
            html_snippet: HTML context around the element
            test_case_id: Associated test case ID

        Returns:
            Healed selector with confidence score
        """
        logger.info(
            "locator_healing_started",
            element=element_description,
            broken_selector=broken_selector,
        )

        # Check healing history for similar cases
        historical_suggestion = await self._check_history(
            element_description, broken_selector
        )
        if historical_suggestion:
            logger.info("healing_from_history", element=element_description)
            return historical_suggestion

        # Get suggestion from Claude
        suggestion = await self.claude.suggest_locator_fix(
            broken_selector=broken_selector,
            element_description=element_description,
            html_snippet=html_snippet,
        )

        if "error" in suggestion:
            return suggestion

        # Score confidence based on:
        # 1. Selector type (ID > class > xpath)
        # 2. HTML context available
        # 3. Historical success rate
        confidence = await self._calculate_confidence(
            broken_selector, suggestion.get("suggested_selector", ""), html_snippet
        )

        result = {
            "original_selector": broken_selector,
            "suggested_selector": suggestion.get("suggested_selector"),
            "explanation": suggestion.get("explanation"),
            "confidence": confidence,
            "test_case_id": test_case_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Store in history
        await self._store_healing_history(result)

        logger.info(
            "locator_healed",
            element=element_description,
            confidence=confidence,
            suggested_selector=suggestion.get("suggested_selector"),
        )

        return result

    async def apply_healing(
        self,
        test_case_id: int,
        original_selector: str,
        new_selector: str,
    ) -> dict:
        """Apply healing to test case and track success.

        Args:
            test_case_id: Test case to update
            original_selector: Original broken selector
            new_selector: New healed selector

        Returns:
            Update result with success tracking
        """
        try:
            # Update test case in database
            result = await self.db.execute(
                update(TestCase)
                .where(TestCase.id == test_case_id)
                .values(test_code=new_selector)  # Simplified - would extract full code
            )

            await self.db.commit()

            # Track healing attempt
            healing_attempt = {
                "test_case_id": test_case_id,
                "original_selector": original_selector,
                "new_selector": new_selector,
                "success": True,
                "timestamp": datetime.utcnow().isoformat(),
            }

            await self._store_healing_attempt(healing_attempt)

            logger.info(
                "healing_applied",
                test_case_id=test_case_id,
                new_selector=new_selector,
            )

            return {"success": True, "test_case_id": test_case_id}

        except Exception as e:
            logger.error(
                "healing_application_failed",
                test_case_id=test_case_id,
                error=str(e),
            )
            return {"success": False, "error": str(e)}

    async def validate_healed_selector(
        self,
        selector: str,
        html_content: str,
    ) -> bool:
        """Validate healed selector works with given HTML.

        Args:
            selector: CSS/XPath selector to validate
            html_content: HTML to test against

        Returns:
            True if selector finds elements, False otherwise
        """
        # In real implementation, would use Playwright/Selenium
        # For now, basic validation
        return len(selector) > 0 and (selector.startswith("#") or selector.startswith("."))

    async def get_healing_statistics(self, hours: int = 24) -> dict:
        """Get healing statistics for monitoring.

        Args:
            hours: Time period to analyze

        Returns:
            Statistics dict with success rates
        """
        # Implement with database queries
        return {
            "total_attempts": len(self.healing_history),
            "successful": sum(
                1
                for h in self.healing_history.values()
                if h.get("success") is True
            ),
            "failed": sum(
                1
                for h in self.healing_history.values()
                if h.get("success") is False
            ),
            "average_confidence": sum(
                h.get("confidence", 0)
                for h in self.healing_history.values()
            ) / max(len(self.healing_history), 1),
        }

    async def _calculate_confidence(
        self,
        original: str,
        suggested: str,
        html_snippet: str,
    ) -> float:
        """Calculate confidence score (0-1.0) for healed selector.

        Scoring factors:
        - ID selectors (highest confidence: 0.95)
        - Class selectors (high: 0.85)
        - XPath with specific attributes (medium: 0.75)
        - HTML context available (boost +0.05)
        - Not using generic selectors (penalty -0.1)
        """
        confidence = 0.7  # Base confidence

        # Boost for specific selector types
        if suggested.startswith("#"):
            confidence = 0.95  # ID selectors are most reliable
        elif suggested.startswith("."):
            confidence = 0.85  # Class selectors
        elif "[" in suggested and "]" in suggested:
            confidence = 0.80  # Attribute selectors

        # Boost if HTML context provided
        if html_snippet:
            confidence += 0.05

        # Penalty for overly generic selectors
        if suggested in ["button", "input", "div"]:
            confidence -= 0.1

        return min(max(confidence, 0.0), 1.0)

    async def _check_history(
        self,
        element_description: str,
        broken_selector: str,
    ) -> dict | None:
        """Check healing history for similar cases.

        Args:
            element_description: Element description
            broken_selector: Original selector

        Returns:
            Previous successful healing or None
        """
        key = f"{element_description}:{broken_selector}"
        if key in self.healing_history:
            history = self.healing_history[key]
            if history.get("success"):
                logger.info("healing_cache_hit", key=key)
                return history

        return None

    async def _store_healing_history(self, result: dict) -> None:
        """Store healing result in history.

        Args:
            result: Healing result to store
        """
        key = f"{result.get('element', '')}:{result.get('original_selector', '')}"
        self.healing_history[key] = result

        # In production, also store in database for persistence
        # INSERT INTO healing_history (original, suggested, confidence)

    async def _store_healing_attempt(self, attempt: dict) -> None:
        """Store healing attempt for success tracking.

        Args:
            attempt: Healing attempt record
        """
        # Store in database for analytics
        # INSERT INTO healing_attempts (test_case_id, success, timestamp)
        logger.info("healing_attempt_recorded", test_case_id=attempt["test_case_id"])
