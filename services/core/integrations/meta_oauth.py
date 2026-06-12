"""Meta OAuth: code -> long-lived user token -> page token + IG account, persisted per user."""
import logging
from datetime import datetime, timedelta
from typing import Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.config import settings
from services.core.db.models import ConnectedIntegration
from services.core.security.crypto import encrypt

logger = logging.getLogger(__name__)

GRAPH = "https://graph.facebook.com/v21.0"
SCOPES = (
    "pages_show_list,pages_manage_posts,pages_read_engagement,"
    "instagram_basic,instagram_content_publish,business_management"
)


def authorize_url(state: str) -> str:
    return (
        "https://www.facebook.com/v21.0/dialog/oauth"
        f"?client_id={settings.META_APP_ID}"
        f"&redirect_uri={settings.META_REDIRECT_URI}"
        f"&state={state}&scope={SCOPES}&response_type=code"
    )


async def complete_connection(db: AsyncSession, user_id: str, code: str) -> ConnectedIntegration:
    """Run the full exchange chain and upsert the user's Meta integration row."""
    async with httpx.AsyncClient(timeout=15) as client:
        # 1. code -> short-lived user token
        r = await client.get(f"{GRAPH}/oauth/access_token", params={
            "client_id": settings.META_APP_ID,
            "client_secret": settings.META_APP_SECRET,
            "redirect_uri": settings.META_REDIRECT_URI,
            "code": code,
        })
        r.raise_for_status()
        short_token = r.json()["access_token"]

        # 2. short-lived -> long-lived user token (~60 days)
        r = await client.get(f"{GRAPH}/oauth/access_token", params={
            "grant_type": "fb_exchange_token",
            "client_id": settings.META_APP_ID,
            "client_secret": settings.META_APP_SECRET,
            "fb_exchange_token": short_token,
        })
        r.raise_for_status()
        data = r.json()
        user_token = data["access_token"]
        expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 5184000))

        # 3. Pages (the page access token is the publish credential)
        r = await client.get(f"{GRAPH}/me/accounts", params={
            "fields": "id,name,access_token", "access_token": user_token,
        })
        r.raise_for_status()
        pages = r.json().get("data", [])
        if not pages:
            raise ValueError("no_facebook_page: this account manages no Facebook Pages")
        page = pages[0]  # v1: first page; all recorded for a future picker

        # 4. Linked Instagram Business account (optional)
        r = await client.get(f"{GRAPH}/{page['id']}", params={
            "fields": "instagram_business_account{id,username}",
            "access_token": page["access_token"],
        })
        r.raise_for_status()
        ig = r.json().get("instagram_business_account") or {}

    # 5. Upsert
    result = await db.execute(select(ConnectedIntegration).where(
        ConnectedIntegration.user_id == user_id,
        ConnectedIntegration.platform == "meta",
    ))
    row: Optional[ConnectedIntegration] = result.scalars().first()
    if row is None:
        row = ConnectedIntegration(user_id=user_id, platform="meta")
        db.add(row)

    row.status = "connected"
    row.oauth_tokens_encrypted = {
        "user_token": encrypt(user_token),
        "page_token": encrypt(page["access_token"]),
        "expires_at": expires_at.isoformat(),
    }
    row.config = {
        "page_id": page["id"],
        "page_name": page.get("name", ""),
        "ig_user_id": ig.get("id"),
        "ig_username": ig.get("username"),
        "available_pages": [{"id": p["id"], "name": p.get("name", "")} for p in pages],
        "scopes": SCOPES.split(","),
    }
    await db.commit()
    await db.refresh(row)
    logger.info("Meta connected for user %s (page=%s, ig=%s)", user_id, page["id"], ig.get("id"))
    return row
