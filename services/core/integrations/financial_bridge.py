import logging
from typing import List, Dict, Any, Optional
from .base import IntegrationRegistry
from ..agents.models import TaskResult, TaskStatus

logger = logging.getLogger(__name__)

class FinancialBridge:
    """
    Universal Bridge for Financial operations (Stripe, Shopify, PayPal).
    """
    
    @staticmethod
    async def get_revenue_snapshot() -> TaskResult:
        """Get a unified view of revenue across all connected platforms."""
        connected_platforms = [p for p in IntegrationRegistry.list_instances() if p in ["stripe", "shopify"]]
        results = {}
        for p in connected_platforms:
            instance = IntegrationRegistry.get_instance(p)
            results[p] = await instance.execute_action("get_revenue_snapshot", {})
            
        return TaskResult(
            status=TaskStatus.COMPLETED,
            data={"platforms": results},
            educational_takeaway="I've aggregated your revenue data from all connected sources."
        )

    @staticmethod
    async def create_invoice(params: Dict[str, Any]) -> TaskResult:
        """Route invoice creation to the primary financial platform."""
        platform = params.get("platform", "stripe") # Default to stripe
        instance = IntegrationRegistry.get_instance(platform)
        
        if not instance:
            return TaskResult(status=TaskStatus.FAILED, data={}, educational_takeaway=f"No active connection for {platform}.")
            
        try:
            result = await instance.execute_action("create_invoice", params)
            return TaskResult(
                status=TaskStatus.COMPLETED,
                data=result,
                educational_takeaway=f"Invoice created successfully on {platform}."
            )
        except Exception as e:
            return TaskResult(status=TaskStatus.FAILED, data={}, educational_takeaway=f"Failed to create invoice: {str(e)}")
