"""Celery application and configuration."""
from celery import Celery
from app.config import settings

# Initialize Celery app
celery_app = Celery(
    "qa_automation",
    broker=settings.redis_url,
    backend=settings.redis_url
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
)

# Import tasks
from app.workers.tasks import execute_tests_task, generate_report_task, analyze_failures_task
