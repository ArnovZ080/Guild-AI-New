import logging
from typing import List, Dict, Any, Optional
from .base import IntegrationRegistry
from ..agents.models import TaskResult, TaskStatus

logger = logging.getLogger(__name__)

class CRMBridge:
    """
    Universal Bridge for CRM actions (HubSpot, Salesforce, etc.).
    """
    
    @staticmethod
    async def sync_contact(contact_data: Dict[str, Any]) -> TaskResult:
        """
        Sync a contact across all connected CRM platforms.
        """
        connected_platforms = IntegrationRegistry.list_instances()
        crm_platforms = ["hubspot", "salesforce", "pipedrive"]
        
        target_platforms = [p for p in connected_platforms if p in crm_platforms]
        
        if not target_platforms:
            return TaskResult(
                status=TaskStatus.FAILED,
                data={},
                educational_takeaway="No CRM platforms are connected. Please connect HubSpot or Salesforce."
            )
            
        results = {}
        process_log = [f"CRMBridge: Syncing contact across {', '.join(target_platforms)}"]
        
        for platform in target_platforms:
            instance = IntegrationRegistry.get_instance(platform)
            if not instance: continue
                
            try:
                result = await instance.execute_action("sync_contact", contact_data)
                results[platform] = result
                process_log.append(f"Successfully synced to {platform}.")
            except Exception as e:
                logger.error(f"CRM sync failed for {platform}: {e}")
                results[platform] = {"status": "error", "message": str(e)}
                process_log.append(f"Failed to sync to {platform}: {str(e)}")
                
        return TaskResult(
            status=TaskStatus.COMPLETED if any(results.values()) else TaskStatus.FAILED,
            data=results,
            process_log=process_log,
            educational_takeaway=f"I've synchronized the contact details with your CRM systems."
        )

    @staticmethod
    async def update_deal(deal_data: Dict[str, Any]) -> TaskResult:
        """Update a deal/opportunity in connected CRMs."""
        # Simplified for now, would need mapping logic per platform
        return await CRMBridge._dispatch_to_crms("update_deal", deal_data)

    @staticmethod
    async def _dispatch_to_crms(action: str, data: Dict[str, Any]) -> TaskResult:
        connected_platforms = [p for p in IntegrationRegistry.list_instances() if p in ["hubspot", "salesforce"]]
        results = {}
        for p in connected_platforms:
            instance = IntegrationRegistry.get_instance(p)
            results[p] = await instance.execute_action(action, data)
        return TaskResult(status=TaskStatus.COMPLETED, data=results, educational_takeaway="CRM action completed.")
