import logging
import stripe
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)

class StripeIntegration(BaseIntegration):
    """
    Stripe integration port.
    Supports revenue tracking, subscription management, and invoice creation.
    """
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        stripe.api_key = self.config.credentials.get("api_key")
        
    async def validate_connection(self) -> bool:
        """Validate connection by retrieving account details."""
        try:
            stripe.Account.retrieve()
            return True
        except Exception as e:
            logger.error(f"Stripe connection validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """Execute Stripe specific actions."""
        if action_name == "get_revenue_snapshot":
            return await self._get_revenue_snapshot(params)
        elif action_name == "create_invoice":
            return await self._create_invoice(params)
        elif action_name == "issue_refund":
            return await self._issue_refund(params)
        else:
            raise ValueError(f"Action '{action_name}' not supported by Stripe.")

    async def _get_revenue_snapshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch a summary of recent revenue."""
        # Note: In a real implementation, we would use stripe.Balance.retrieve()
        # and stripe.Charge.list() to calculate these values.
        balance = stripe.Balance.retrieve()
        return {
            "available": [{"amount": b.amount / 100, "currency": b.currency} for b in balance.available],
            "pending": [{"amount": b.amount / 100, "currency": b.currency} for b in balance.pending]
        }

    async def _create_invoice(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create and finalize an invoice."""
        customer_id = params.get("customer_id")
        amount = params.get("amount") # Not directly used in create_invoice usually, but kept for context
        
        invoice = stripe.Invoice.create(customer=customer_id, description=params.get("description"))
        finalized = stripe.Invoice.finalize_invoice(invoice.id)
        
        return {
            "id": finalized.id,
            "status": finalized.status,
            "url": finalized.hosted_invoice_url,
            "amount": finalized.amount_due / 100
        }

    async def _issue_refund(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Refund a specific payment."""
        charge_id = params.get("charge_id")
        refund = stripe.Refund.create(charge=charge_id)
        return {
            "id": refund.id,
            "status": refund.status,
            "amount": refund.amount / 100
        }

    @property
    def capabilities(self) -> List[str]:
        return ["get_revenue_snapshot", "create_invoice", "issue_refund"]
