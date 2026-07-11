import asyncio
import json
from fastapi.testclient import TestClient

# Mock DB and models to avoid complex setup
from unittest.mock import AsyncMock, patch

async def mock_get_current_user():
    from services.core.db.models import UserAccount
    return UserAccount(id="test-user-id", email="test@example.com")

async def test_flow():
    # Patch BusinessIdentityManager
    with patch("services.core.agents.identity.BusinessIdentityManager.get", new_callable=AsyncMock) as mock_get, \
         patch("services.core.agents.identity.BusinessIdentityManager.create_or_update", new_callable=AsyncMock) as mock_update:
        
        from services.core.db.models import BusinessIdentity
        fake_identity = BusinessIdentity(
            user_id="test-user-id",
            business_name="Test Business",
            knowledge_ledger={}
        )
        mock_get.return_value = fake_identity
        mock_update.return_value = fake_identity
        
        # Now import app and override dependency
        from services.api.main import app
        from services.api.middleware.auth import get_current_user
        app.dependency_overrides[get_current_user] = mock_get_current_user
        
        client = TestClient(app)
        
        print("--- Testing Chat with 'I don't know' ---")
        response = client.post("/api/v1/onboarding/chat", json={
            "message": "I don't know what my target audience is.",
            "history": []
        })
        print(response.status_code)
        print(response.json())
        
        print("--- Testing Chat with history ---")
        response2 = client.post("/api/v1/onboarding/chat", json={
            "message": "Actually, my target audience is small business owners.",
            "history": [
                {"role": "user", "content": "I don't know what my target audience is."},
                {"role": "assistant", "content": "Most owners haven't put this into words..."}
            ]
        })
        print(response2.status_code)
        print(response2.json())

if __name__ == "__main__":
    asyncio.run(test_flow())
