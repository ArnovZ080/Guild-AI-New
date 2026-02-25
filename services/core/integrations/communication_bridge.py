import logging
from typing import List, Dict, Any, Optional
from .base import IntegrationRegistry
from ..agents.models import TaskResult, TaskStatus

logger = logging.getLogger(__name__)

class CommunicationBridge:
    """
    Universal Bridge for Communication (Email, Slack, Discord).
    """
    
    @staticmethod
    async def send_message(content: str, target: str, channel: str = "auto") -> TaskResult:
        """
        Send a message via the specified or most appropriate channel.
        """
        connected_platforms = IntegrationRegistry.list_instances()
        process_log = [f"CommunicationBridge: Routing message to {target} via {channel}"]
        
        # Mapping logic
        platforms_to_try = []
        if channel == "auto":
            if "@" in target:
                platforms_to_try = ["sendgrid", "smtp"]
            else:
                platforms_to_try = ["slack", "discord"]
        else:
            platforms_to_try = [channel]

        results = {}
        for platform in platforms_to_try:
            instance = IntegrationRegistry.get_instance(platform)
            if not instance: continue
            
            try:
                result = await instance.execute_action("send_message", {"recipient": target, "content": content})
                results[platform] = result
                process_log.append(f"Successfully sent via {platform}.")
            except Exception as e:
                logger.error(f"Failed to send via {platform}: {e}")
                process_log.append(f"Failed to send via {platform}: {str(e)}")

        return TaskResult(
            status=TaskStatus.COMPLETED if any(results.values()) else TaskStatus.FAILED,
            data=results,
            process_log=process_log,
            educational_takeaway=f"I've sent your message to {target}."
        )

    @staticmethod
    async def broadcast(content: str) -> TaskResult:
        """Broadcast to all connected team channels."""
        # TODO: Implement broadcast to Slack/Discord
        return TaskResult(status=TaskStatus.COMPLETED, data={}, educational_takeaway="Broadcast pending implementation.")
