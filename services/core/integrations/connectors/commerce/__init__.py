from typing import Dict, Any, List
from services.core.integrations.base import BaseIntegration, IntegrationConfig

class PayPalIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_invoice":
            return {"status": "success", "invoice_id": "INV-12345"}
        elif action_name == "check_payment_status":
            return {"status": "paid", "transaction_id": params.get("transaction_id")}
        elif action_name == "process_refund":
            return {"status": "refunded", "amount": params.get("amount")}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["create_invoice", "check_payment_status", "process_refund"]

class SquareIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "sync_pos":
            return {"status": "success", "synced_transactions": 24}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["sync_pos"]

class ShopifyIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_product_catalog":
            return {"products": [{"id": "1", "name": "Test Product", "price": 100}]}
        elif action_name == "get_recent_orders":
            return {"orders": [{"id": "ORD-1", "total": 100}]}
        elif action_name == "sync_inventory":
            return {"status": "success", "synced_items": 150}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["get_product_catalog", "get_recent_orders", "sync_inventory"]

class WooCommerceIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "sync_orders":
            return {"status": "success", "synced_orders": 12}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["sync_orders"]

class AmazonIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_seller_metrics":
            return {"sales_volume": 1200, "active_listings": 45}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["get_seller_metrics"]

# Export
__all__ = [
    "PayPalIntegration",
    "SquareIntegration",
    "ShopifyIntegration",
    "WooCommerceIntegration",
    "AmazonIntegration"
]
