"""
Guild-AI Celery Application with Beat Schedule.

Handles all recurring background tasks for the content-to-customer flywheel.
"""
from celery import Celery
from celery.schedules import crontab
from services.core.config import settings

celery_app = Celery(
    "guild",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.conf.beat_schedule = {
    # Publish content that's been approved and scheduled
    "publish-scheduled-content": {
        "task": "services.core.tasks.publish_scheduled_content",
        "schedule": 300.0,  # every 5 minutes
    },
    # Process nurture sequence steps that are due
    "process-nurture-steps": {
        "task": "services.core.tasks.process_due_nurture_steps",
        "schedule": 900.0,  # every 15 minutes
    },
    # Sync external calendars (Google, Outlook)
    "sync-calendars": {
        "task": "services.core.tasks.sync_external_calendars",
        "schedule": 1800.0,  # every 30 minutes
    },
    # Collect content performance data from integrations
    "collect-performance-data": {
        "task": "services.core.tasks.collect_performance_data",
        "schedule": 3600.0,  # every hour
    },
    # Generate daily content strategy suggestions at 6am UTC
    "daily-content-strategy": {
        "task": "services.core.tasks.daily_content_strategy",
        "schedule": crontab(hour=6, minute=0),
    },
    # Morning brief at 7am UTC
    "daily-brief": {
        "task": "services.core.tasks.generate_daily_brief",
        "schedule": crontab(hour=7, minute=0),
    },
}
