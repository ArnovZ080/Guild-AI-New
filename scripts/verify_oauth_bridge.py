import asyncio
import os
import time
from services.core.integrations.oauth import OAuthService
from services.core.agents.secrets import SecretManager

# Setup environment variables for testing
os.environ["GOOGLE_CLIENT_ID"] = "google_id_123"
os.environ["HUBSPOT_CLIENT_ID"] = "hubspot_id_123"
os.environ["TWITTER_CLIENT_ID"] = "twitter_id_123"
os.environ["OAUTH_REDIRECT_URI"] = "http://localhost:8001/oauth/callback"

async def run_verification():
    print("--- Starting Universal OAuth Bridge Verification ---")
    
    secret_manager = SecretManager("/Users/arnovanzyl/.gemini/antigravity/scratch/data/test_oauth_secrets")
    oauth_service = OAuthService(secret_manager)
    
    # 1. Test Authorization URL Generation
    print("Step 1: Testing Auth URL Generation")
    google_url = oauth_service.get_authorize_url("google")
    print(f"✓ Google URL generated: {google_url[:50]}...")
    assert "google_id_123" in google_url
    assert "calendar" in google_url
    
    hubspot_url = oauth_service.get_authorize_url("hubspot")
    print(f"✓ HubSpot URL generated: {hubspot_url[:50]}...")
    assert "hubspot_id_123" in hubspot_url
    
    twitter_url = oauth_service.get_authorize_url("twitter")
    print(f"✓ Twitter URL generated: {twitter_url[:50]}...")
    assert "twitter_id_123" in twitter_url
    
    # 2. Test Token Storage & Retrieval
    print("Step 2: Testing Token Storage & Retrieval")
    mock_token = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600
    }
    
    oauth_service._save_platform_tokens("google", mock_token)
    
    saved_token = oauth_service.get_access_token("google")
    assert saved_token == "test_access_token"
    print("✓ Token retrieval successful.")
    
    # 3. Test Token Expiry Handling
    print("Step 3: Testing Expiry Handling")
    expired_token = {
        "access_token": "expired_token",
        "expires_in": -10  # Already expired
    }
    oauth_service._save_platform_tokens("hubspot", expired_token)
    
    token_now = oauth_service.get_access_token("hubspot")
    assert token_now is None
    print("✓ Expiry detection successful.")
    
    print("--- OAuth Bridge Verification Completed Successfully ---")

if __name__ == "__main__":
    asyncio.run(run_verification())
