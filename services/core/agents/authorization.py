import uuid
from datetime import datetime
from typing import Dict, List, Optional
from services.core.agents.models import AuthorizationRequest
from services.core.logging import logger

class AuthorizationQueue:
    """
    Queue for human-in-the-loop authorization requests.
    """
    def __init__(self):
        self.requests: Dict[str, AuthorizationRequest] = {}

    def create_request(self, task_id: str, agent_id: str, action_type: str, description: str, params: Dict) -> AuthorizationRequest:
        req_id = str(uuid.uuid4())
        request = AuthorizationRequest(
            id=req_id,
            task_id=task_id,
            agent_id=agent_id,
            action_type=action_type,
            description=description,
            params=params,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.requests[req_id] = request
        logger.info(f"Authorization required: {description} (Type: {action_type})")
        return request

    def approve(self, request_id: str) -> bool:
        if request_id in self.requests:
            self.requests[request_id].status = "approved"
            logger.info(f"Authorized: {self.requests[request_id].description}")
            return True
        return False

    def reject(self, request_id: str):
         if request_id in self.requests:
            self.requests[request_id].status = "rejected"
            logger.info(f"Rejected: {self.requests[request_id].description}")

    def list_pending(self) -> List[AuthorizationRequest]:
        return [r for r in self.requests.values() if r.status == "pending"]

# Global instance
auth_queue = AuthorizationQueue()
