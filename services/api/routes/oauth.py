from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from typing import Dict, Any
from services.core.integrations.oauth import OAuthService
from services.core.agents.secrets import SecretManager
from services.core.logging import logger

router = APIRouter(prefix="/oauth", tags=["oauth"])
secret_manager = SecretManager()
oauth_service = OAuthService(secret_manager)

@router.get("/authorize/{platform}")
async def authorize(platform: str):
    """Start the OAuth flow for a platform."""
    try:
        url = oauth_service.get_authorize_url(platform)
        return {"auth_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to generate auth URL: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/callback/{platform}")
async def callback(platform: str, code: str, state: str = None):
    """Handle the OAuth callback and exchange code for tokens."""
    try:
        token_data = await oauth_service.exchange_code_for_token(platform, code)
        
        # Return a simple HTML page that closes the popup
        html_content = f"""
        <html>
            <body style="background: #0a0a0b; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
                <div style="text-align: center;">
                    <div style="color: #10b981; font-size: 48px; margin-bottom: 20px;">✓</div>
                    <h2 style="margin: 0;">{platform.capitalize()} Connected!</h2>
                    <p style="color: #9ca3af; font-size: 14px;">This window will close automatically.</p>
                </div>
                <script>
                    setTimeout(() => {{
                        window.close();
                    }}, 2000);
                </script>
            </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"OAuth callback failed for {platform}: {e}")
        error_html = f"""
        <html>
            <body style="background: #0a0a0b; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
                <div style="text-align: center;">
                    <div style="color: #ef4444; font-size: 48px; margin-bottom: 20px;">✕</div>
                    <h2 style="margin: 0;">Authentication Failed</h2>
                    <p style="color: #9ca3af; font-size: 14px;">{str(e)}</p>
                    <button onclick="window.close()" style="margin-top: 20px; background: white; color: black; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">Close Window</button>
                </div>
            </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=error_html, status_code=500)

@router.get("/status/{platform}")
async def get_oauth_status(platform: str):
    """Check if a platform is connected via OAuth and if the token is valid."""
    token = oauth_service.get_access_token(platform)
    is_connected = token is not None
    
    return {
        "platform": platform,
        "is_connected": is_connected,
        "needs_refresh": not is_connected and secret_manager.get_secret(f"oauth_{platform}") is not None
    }

@router.post("/refresh/{platform}")
async def refresh_token(platform: str):
    """Manually trigger a token refresh."""
    token = await oauth_service.refresh_token(platform)
    if not token:
        raise HTTPException(status_code=400, detail="Failed to refresh token. Re-authorization may be required.")
    
    return {"status": "success", "message": "Token refreshed."}
