import logging
from typing import List, Dict, Any, Optional
from .base import IntegrationRegistry
from ..agents.models import TaskResult, TaskStatus

logger = logging.getLogger(__name__)

class SocialBridge:
    """
    Universal Bridge for Social Media distribution and monitoring.
    Acts as a middleware between the AI and specific social platforms.
    """
    
    @staticmethod
    async def post_content(content: str, platforms: Optional[List[str]] = None, media_urls: Optional[List[str]] = None) -> TaskResult:
        """
        Post content across all connected or specified social platforms.
        """
        connected_platforms = IntegrationRegistry.list_instances()
        # Filter for social platforms if none specified
        social_platforms = ["twitter", "linkedin", "instagram", "tiktok"]
        
        target_platforms = platforms if platforms else [p for p in connected_platforms if p in social_platforms]
        
        if not target_platforms:
            return TaskResult(
                status=TaskStatus.FAILED,
                data={},
                educational_takeaway="No social media platforms are connected. Please connect Twitter or LinkedIn in the Integration Hub."
            )
            
        results = {}
        process_log = [f"SocialBridge: Initiating post to {', '.join(target_platforms)}"]
        
        for platform in target_platforms:
            instance = IntegrationRegistry.get_instance(platform)
            if not instance:
                process_log.append(f"Skipping {platform}: No active connection.")
                continue
                
            try:
                # Standardized action across all social connectors
                result = await instance.execute_action("post_content", {"content": content, "media_urls": media_urls})
                results[platform] = result
                process_log.append(f"Successfully posted to {platform}.")
            except Exception as e:
                logger.error(f"Failed to post to {platform}: {e}")
                results[platform] = {"status": "error", "message": str(e)}
                process_log.append(f"Failed to post to {platform}: {str(e)}")
                
        return TaskResult(
            status=TaskStatus.COMPLETED if any(results.values()) else TaskStatus.FAILED,
            data=results,
            process_log=process_log,
            educational_takeaway=f"I've shared your content on {', '.join(results.keys())}."
        )

    @staticmethod
    async def get_unified_analytics() -> TaskResult:
        """Fetch and aggregate analytics from all connected social platforms."""
        # TODO: Implement cross-platform analytics aggregation
        return TaskResult(
            status=TaskStatus.COMPLETED,
            data={},
            process_log=["Unified analytics fetch not yet implemented."],
            educational_takeaway="I'm still learning how to aggregate your social stats!"
        )
