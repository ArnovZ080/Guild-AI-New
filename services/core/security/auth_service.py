import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..agents.models import AuthorizationRequest, TaskStatus

logger = logging.getLogger(__name__)

class HumanAuthorizationService:
    """
    Service to manage sensitive action authorizations (HITL).
    Implements tiered safety thresholds for financial actions.
    """
    
    _requests: Dict[str, AuthorizationRequest] = {}
    _thresholds: Dict[str, float] = {
        "financial": 0.0,  # Default to Hard HITL as per user request
    }

    @classmethod
    def set_threshold(cls, category: str, amount: float):
        """Set the 'Green Zone' threshold for a category."""
        cls._thresholds[category] = amount
        logger.info(f"Threshold for {category} set to {amount}")

    @classmethod
    def should_require_approval(cls, action_type: str, params: Dict[str, Any]) -> bool:
        """
        Determine if an action requires human approval based on type and amount.
        """
        # Red Zone: High-sensitivity actions always require approval
        sensitive_actions = ["issue_refund", "change_settings", "delete_data"]
        if any(action in params.get("action", "") for action in sensitive_actions):
            return True

        if action_type == "financial":
            amount = params.get("amount", 0.0)
            threshold = cls._thresholds.get("financial", 0.0)
            return amount > threshold

        # Default: Require approval for unknown sensitive types
        return action_type in ["financial", "security", "broadcast"]

    @classmethod
    def create_request(cls, task_id: str, agent_id: str, action_type: str, description: str, params: Dict[str, Any]) -> str:
        """Create a new authorization request and queue it."""
        request_id = str(uuid.uuid4())
        request = AuthorizationRequest(
            id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            action_type=action_type,
            description=description,
            params=params,
            status="pending",
            created_at=datetime.utcnow().isoformat()
        )
        cls._requests[request_id] = request
        logger.info(f"Created authorization request {request_id} for {action_type}")
        return request_id

    @classmethod
    def get_request(cls, request_id: str) -> Optional[AuthorizationRequest]:
        return cls._requests.get(request_id)

    @classmethod
    def list_pending(cls) -> List[AuthorizationRequest]:
        return [r for r in cls._requests.values() if r.status == "pending"]

    @classmethod
    def authorize(cls, request_id: str) -> bool:
        """Approve a request."""
        if request_id in cls._requests:
            cls._requests[request_id].status = "approved"
            return True
        return False

    @classmethod
    def deny(cls, request_id: str) -> bool:
        """Reject a request."""
        if request_id in cls._requests:
            cls._requests[request_id].status = "rejected"
            return True
        return False
