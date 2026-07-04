#!/bin/bash
# Start Celery worker

celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
