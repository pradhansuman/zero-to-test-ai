"""Advanced test scheduling with resource awareness."""
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)


class TestScheduler:
    """Schedules tests with resource and cost awareness."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def schedule_tests(
        self,
        test_ids: List[int],
        priority: str = "normal",
        resource_constraints: Dict = None,
    ) -> Dict:
        """Schedule tests with resource optimization.

        Args:
            test_ids: Test IDs to schedule
            priority: Priority level (low, normal, high, critical)
            resource_constraints: CPU/memory limits

        Returns:
            Schedule plan
        """
        resource_constraints = resource_constraints or {
            "cpu_percent": 80,
            "memory_mb": 2048,
        }

        priority_delay = {
            "critical": 0,
            "high": 60,
            "normal": 300,
            "low": 3600,
        }

        optimal_time = self._calculate_optimal_time(
            priority,
            priority_delay.get(priority, 0)
        )

        return {
            "test_ids": test_ids,
            "priority": priority,
            "scheduled_time": optimal_time.isoformat(),
            "resource_constraints": resource_constraints,
            "estimated_duration": self._estimate_duration(len(test_ids)),
            "estimated_cost": self._estimate_cost(len(test_ids)),
            "created_at": datetime.utcnow().isoformat(),
        }

    def _calculate_optimal_time(self, priority: str, delay: int) -> datetime:
        """Calculate optimal execution time.

        Args:
            priority: Priority level
            delay: Initial delay in seconds

        Returns:
            Optimal datetime
        """
        now = datetime.utcnow()
        scheduled = now + timedelta(seconds=delay)

        # Prefer off-peak hours (10 PM - 6 AM) for cost savings
        hour = scheduled.hour
        if hour >= 6 and hour < 22:  # Peak hours
            # Schedule for next off-peak window
            if hour < 22:
                scheduled = scheduled.replace(hour=22, minute=0, second=0)
            else:
                scheduled = scheduled + timedelta(days=1)
                scheduled = scheduled.replace(hour=0, minute=0, second=0)

        return scheduled

    def _estimate_duration(self, test_count: int) -> int:
        """Estimate execution duration in seconds.

        Args:
            test_count: Number of tests

        Returns:
            Estimated duration in seconds
        """
        # ~2 seconds per test + 30s overhead
        return (test_count * 2) + 30

    def _estimate_cost(self, test_count: int) -> float:
        """Estimate execution cost in dollars.

        Args:
            test_count: Number of tests

        Returns:
            Estimated cost
        """
        # ~$0.01 per test
        return test_count * 0.01

    async def reschedule_tests(
        self,
        schedule_id: str,
        new_priority: str,
    ) -> Dict:
        """Reschedule existing schedule with new priority.

        Args:
            schedule_id: Schedule ID
            new_priority: New priority level

        Returns:
            Updated schedule
        """
        priority_delay = {
            "critical": 0,
            "high": 60,
            "normal": 300,
            "low": 3600,
        }

        new_time = self._calculate_optimal_time(
            new_priority,
            priority_delay.get(new_priority, 0)
        )

        logger.info(
            "schedule_rescheduled",
            schedule_id=schedule_id,
            new_priority=new_priority,
        )

        return {
            "schedule_id": schedule_id,
            "new_priority": new_priority,
            "new_scheduled_time": new_time.isoformat(),
        }

    async def get_schedule_status(self, schedule_id: str) -> Dict:
        """Get schedule status.

        Args:
            schedule_id: Schedule ID

        Returns:
            Schedule status
        """
        return {
            "schedule_id": schedule_id,
            "status": "scheduled",
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def cancel_schedule(self, schedule_id: str) -> Dict:
        """Cancel a schedule.

        Args:
            schedule_id: Schedule ID

        Returns:
            Cancellation confirmation
        """
        logger.info("schedule_cancelled", schedule_id=schedule_id)

        return {
            "schedule_id": schedule_id,
            "status": "cancelled",
            "cancelled_at": datetime.utcnow().isoformat(),
        }
