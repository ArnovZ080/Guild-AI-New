import os
import json
import time
import httpx
from typing import Dict, Any, Optional
from services.core.logging import logger
from services.core.agents.secrets import SecretManager

class OAuthService:
    """
    Centralized service for handling OAuth 2.0 flows across multiple platforms.
    """
    
    # Platform configurations
    PLATFORMS = {
        "google": {
            "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "scopes": [
                "https://www.googleapis.com/auth/calendar",
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/userinfo.email"
            ]
        },
        "hubspot": {
            "auth_url": "https://app.hubspot.com/oauth/authorize",
            "token_url": "https://api.hubapi.com/oauth/v1/token",
            "scopes": ["crm.objects.contacts.read", "crm.objects.contacts.write"]
        },
        "twitter": {
            "auth_url": "https://twitter.com/i/oauth2/authorize",
            "token_url": "https://api.twitter.com/2/oauth2/token",
            "scopes": ["tweet.read", "tweet.write", "users.read", "offline.access"]
        }
    }

    def __init__(self, secret_manager: SecretManager):
        self.secret_manager = secret_manager
        self.redirect_uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8001/oauth/callback")

    def get_authorize_url(self, platform: str) -> str:
        """Generate the authorization URL for a specific platform."""
        if platform not in self.PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")
        
        config = self.PLATFORMS[platform]
        client_id = os.getenv(f"{platform.upper()}_CLIENT_ID")
        
        if not client_id:
            logger.error(f"Missing client ID for {platform}")
            raise ValueError(f"{platform.upper()}_CLIENT_ID environment variable not set.")

        params = {
            "client_id": client_id,
            "redirect_uri": f"{self.redirect_uri}/{platform}",
            "response_type": "code",
            "scope": " ".join(config["scopes"]),
            "access_type": "offline",  # For Google refresh tokens
            "prompt": "consent",
            "state": os.urandom(16).hex()  # In production, store this state to verify callback
        }
        
        # Twitter specific tweaks
        if platform == "twitter":
            params["code_challenge"] = "challenge"  # Should be dynamic PKCE
            params["code_challenge_method"] = "plain"

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{config['auth_url']}?{query_string}"

    async def exchange_code_for_token(self, platform: str, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access and refresh tokens."""
        if platform not in self.PLATFORMS:
            raise ValueError(f"Unsupported platform: {platform}")

        config = self.PLATFORMS[platform]
        client_id = os.getenv(f"{platform.upper()}_CLIENT_ID")
        client_secret = os.getenv(f"{platform.upper()}_CLIENT_SECRET")

        async with httpx.AsyncClient() as client:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": f"{self.redirect_uri}/{platform}",
                "grant_type": "authorization_code"
            }
            
            response = await client.post(config["token_url"], data=data)
            
            if response.status_code != 200:
                logger.error(f"Failed to exchange code for {platform}: {response.text}")
                raise Exception(f"Token exchange failed: {response.text}")
            
            token_data = response.json()
            
            # Store tokens securely
            self._save_platform_tokens(platform, token_data)
            
            return token_data

    async def refresh_token(self, platform: str) -> Optional[str]:
        """Refresh the access token for a specific platform."""
        tokens = self.secret_manager.get_secret(f"oauth_{platform}")
        if not tokens or "refresh_token" not in tokens:
            logger.warning(f"No refresh token found for {platform}")
            return None

        config = self.PLATFORMS[platform]
        client_id = os.getenv(f"{platform.upper()}_CLIENT_ID")
        client_secret = os.getenv(f"{platform.upper()}_CLIENT_SECRET")

        async with httpx.AsyncClient() as client:
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": tokens["refresh_token"],
                "grant_type": "refresh_token"
            }
            
            response = await client.post(config["token_url"], data=data)
            
            if response.status_code != 200:
                logger.error(f"Failed to refresh token for {platform}: {response.text}")
                return None
            
            refresh_data = response.json()
            # Merge new data with old to preserve some fields if necessary
            new_tokens = {**tokens, **refresh_data}
            self._save_platform_tokens(platform, new_tokens)
            
            return new_tokens.get("access_token")

    async def get_valid_access_token(self, platform: str) -> Optional[str]:
        """Retrieve a valid access token, refreshing it if necessary."""
        token = self.get_access_token(platform)
        if token:
            return token
        
        # If expired or missing, try to refresh
        logger.info(f"Access token for {platform} expired or missing. Attempting refresh...")
        return await self.refresh_token(platform)

    def _save_platform_tokens(self, platform: str, token_data: Dict[str, Any]):
        """Save token data to SecretManager."""
        # Calculate expiry time
        if "expires_in" in token_data:
            token_data["expires_at"] = int(time.time()) + token_data["expires_in"]
        
        self.secret_manager.store_secret(f"oauth_{platform}", token_data)
        logger.info(f"OAuth tokens updated for {platform}")

    def get_access_token(self, platform: str) -> Optional[str]:
        """Retrieve the current access token, or None if not found/expired."""
        tokens = self.secret_manager.get_secret(f"oauth_{platform}")
        if not tokens:
            return None
        
        # Check expiry
        expires_at = tokens.get("expires_at")
        if expires_at and time.time() > (expires_at - 60):  # 1 min buffer
            logger.info(f"Token for {platform} is expired or expiring soon.")
            return None
            
        return tokens.get("access_token")
