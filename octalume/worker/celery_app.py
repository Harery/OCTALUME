"""Celery configuration for background tasks."""

import asyncio

from celery import Celery

from octalume.utils.config import get_settings
from octalume.utils.logging import get_logger

logger = get_logger(__name__)

settings = get_settings()

celery_app = Celery(
    "octalume",
    broker=settings.redis_url or "redis://localhost:6379/0",
    backend=settings.redis_url or "redis://localhost:6379/0",
    include=[
        "octalume.worker.tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    task_routes={
        "octalume.worker.tasks.run_compliance_scan": {"queue": "compliance"},
        "octalume.worker.tasks.run_health_check": {"queue": "monitoring"},
        "octalume.worker.tasks.cleanup_expired_data": {"queue": "maintenance"},
    },
)


def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
