import logging
from typing import List, Dict, Any, Optional
from .base import IntegrationRegistry
from ..agents.models import TaskResult, TaskStatus

logger = logging.getLogger(__name__)

class CalendarBridge:
    """
    Universal Bridge for Calendar actions (Google Calendar, Outlook, etc.).
    """
    
    @staticmethod
    async def schedule_event(event_details: Dict[str, Any]) -> TaskResult:
        """
        Schedule an event across all connected calendars.
        """
        connected_platforms = IntegrationRegistry.list_instances()
        calendar_platforms = ["google_calendar", "outlook"]
        
        target_platforms = [p for p in connected_platforms if p in calendar_platforms]
        
        if not target_platforms:
            return TaskResult(
                status=TaskStatus.FAILED,
                data={},
                educational_takeaway="No calendar platforms are connected. Please connect Google Calendar or Outlook."
            )
            
        results = {}
        process_log = [f"CalendarBridge: Scheduling event in {', '.join(target_platforms)}"]
        
        for platform in target_platforms:
            instance = IntegrationRegistry.get_instance(platform)
            if not instance: continue
                
            try:
                result = await instance.execute_action("create_event", event_details)
                results[platform] = result
                process_log.append(f"Successfully scheduled in {platform}.")
            except Exception as e:
                logger.error(f"Calendar scheduling failed for {platform}: {e}")
                results[platform] = {"status": "error", "message": str(e)}
                process_log.append(f"Failed to schedule in {platform}: {str(e)}")
                
        return TaskResult(
            status=TaskStatus.COMPLETED if any(results.values()) else TaskStatus.FAILED,
            data=results,
            process_log=process_log,
            educational_takeaway=f"I've added the event to your {', '.join(results.keys())}."
        )

    @staticmethod
    async def get_daily_agenda() -> TaskResult:
        """Fetch and merge agenda from all connected calendars."""
        # TODO: Implement agenda merging
        return TaskResult(
            status=TaskStatus.COMPLETED,
            data={},
            process_log=["Agenda aggregation not yet implemented."],
            educational_takeaway="I'm working on merging your daily schedules!"
        )
