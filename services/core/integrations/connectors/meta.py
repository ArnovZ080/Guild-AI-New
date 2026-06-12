"""Meta connector: real Facebook Page + Instagram publishing and engagement reading.

Loaded per-user via MetaConnector.for_user(db, user_id) — never via the generic
registry, which has no credentials.
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.config import settings
from services.core.db.models import ConnectedIntegration
from services.core.security.crypto import decrypt, encrypt
from services.core.ingestion.models import EngagementEvent

logger = logging.getLogger(__name__)
GRAPH = "https://graph.facebook.com/v21.0"


class NeedsReauth(Exception):
    """Token expired/revoked and could not be refreshed."""


class PublishPreconditionError(Exception):
    """Content can't be published as-is. .reason in {needs_image, no_instagram_account}."""
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class MetaConnector:
    def __init__(self, row: ConnectedIntegration, page_token: str):
        self.row = row
        self.page_id: str = row.config.get("page_id")
        self.ig_user_id: Optional[str] = row.config.get("ig_user_id")
        self._token = page_token

    # ── loading ──────────────────────────────────────────────────────────
    @classmethod
    async def for_user(cls, db: AsyncSession, user_id: str) -> Optional["MetaConnector"]:
        result = await db.execute(select(ConnectedIntegration).where(
            ConnectedIntegration.user_id == user_id,
            ConnectedIntegration.platform == "meta",
        ))
        row = result.scalars().first()
        if row is None or row.status == "disconnected":
            return None
        if row.status == "needs_reauth":
            raise NeedsReauth(user_id)

        tokens = row.oauth_tokens_encrypted or {}
        expires_at = datetime.fromisoformat(tokens.get("expires_at", "1970-01-01T00:00:00"))

        if expires_at < datetime.utcnow() + timedelta(days=7):
            try:
                tokens = await cls._refresh(db, row, tokens)
            except Exception as e:
                logger.warning("Meta token refresh failed for %s: %s", user_id, e)
                row.status = "needs_reauth"
                await db.commit()
                raise NeedsReauth(user_id)

        return cls(row, decrypt(tokens["page_token"]))

    @staticmethod
    async def _refresh(db: AsyncSession, row: ConnectedIntegration, tokens: dict) -> dict:
        """Extend the long-lived user token and re-derive the page token."""
        user_token = decrypt(tokens["user_token"])
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{GRAPH}/oauth/access_token", params={
                "grant_type": "fb_exchange_token",
                "client_id": settings.META_APP_ID,
                "client_secret": settings.META_APP_SECRET,
                "fb_exchange_token": user_token,
            })
            r.raise_for_status()
            data = r.json()
            new_user_token = data["access_token"]
            expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 5184000))

            r = await client.get(f"{GRAPH}/me/accounts", params={
                "fields": "id,access_token", "access_token": new_user_token,
            })
            r.raise_for_status()
            pages = {p["id"]: p["access_token"] for p in r.json().get("data", [])}
            page_token = pages.get(row.config.get("page_id"))
            if not page_token:
                raise ValueError("page no longer accessible")

        new_tokens = {
            "user_token": encrypt(new_user_token),
            "page_token": encrypt(page_token),
            "expires_at": expires_at.isoformat(),
        }
        row.oauth_tokens_encrypted = new_tokens
        await db.commit()
        return new_tokens

    # ── publishing ───────────────────────────────────────────────────────
    async def publish_post(self, content: str, media_urls: List[str],
                           title: Optional[str], platform_hint: str) -> dict:
        if platform_hint == "instagram":
            return await self._publish_instagram(content, media_urls)
        return await self._publish_facebook(content, media_urls)

    async def _publish_facebook(self, content: str, media_urls: List[str]) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            if media_urls:
                r = await client.post(f"{GRAPH}/{self.page_id}/photos", data={
                    "url": media_urls[0], "caption": content, "access_token": self._token,
                })
            else:
                r = await client.post(f"{GRAPH}/{self.page_id}/feed", data={
                    "message": content, "access_token": self._token,
                })
            r.raise_for_status()
            post_id = r.json().get("post_id") or r.json()["id"]
            perma = await client.get(f"{GRAPH}/{post_id}", params={
                "fields": "permalink_url", "access_token": self._token,
            })
            permalink = perma.json().get("permalink_url", "") if perma.status_code == 200 else ""
        return {"status": "published", "post_id": post_id,
                "permalink": permalink, "channel": "facebook"}

    async def _publish_instagram(self, content: str, media_urls: List[str]) -> dict:
        if not self.ig_user_id:
            raise PublishPreconditionError("no_instagram_account")
        if not media_urls:
            raise PublishPreconditionError("needs_image")
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(f"{GRAPH}/{self.ig_user_id}/media", data={
                "image_url": media_urls[0], "caption": content, "access_token": self._token,
            })
            r.raise_for_status()
            container_id = r.json()["id"]

            for _ in range(5):  # wait for Meta to fetch & process the image
                s = await client.get(f"{GRAPH}/{container_id}", params={
                    "fields": "status_code", "access_token": self._token,
                })
                if s.json().get("status_code") == "FINISHED":
                    break
                await asyncio.sleep(3)

            r = await client.post(f"{GRAPH}/{self.ig_user_id}/media_publish", data={
                "creation_id": container_id, "access_token": self._token,
            })
            r.raise_for_status()
            media_id = r.json()["id"]
            perma = await client.get(f"{GRAPH}/{media_id}", params={
                "fields": "permalink", "access_token": self._token,
            })
            permalink = perma.json().get("permalink", "") if perma.status_code == 200 else ""
        return {"status": "published", "post_id": media_id,
                "permalink": permalink, "channel": "instagram"}

    # ── engagement reading ───────────────────────────────────────────────
    async def fetch_engagement(self, post_id: str, channel: str,
                               content_item_id: str) -> List[EngagementEvent]:
        events: List[EngagementEvent] = []
        async with httpx.AsyncClient(timeout=15) as client:
            if channel == "instagram":
                r = await client.get(f"{GRAPH}/{post_id}/comments", params={
                    "fields": "id,username,text,timestamp", "access_token": self._token,
                })
                comments = r.json().get("data", []) if r.status_code == 200 else []
                for c in comments:
                    events.append(EngagementEvent(
                        platform="instagram", content_item_id=content_item_id,
                        platform_post_id=post_id, type="comment",
                        event_id=c["id"],
                        engaged_user={"name": c.get("username", ""),
                                      "handle": c.get("username", "")},
                        text=c.get("text", ""), occurred_at=c.get("timestamp", ""),
                    ))
                r = await client.get(f"{GRAPH}/{post_id}", params={
                    "fields": "like_count,comments_count", "access_token": self._token,
                })
                if r.status_code == 200:
                    d = r.json()
                    events.append(EngagementEvent(
                        platform="instagram", content_item_id=content_item_id,
                        platform_post_id=post_id, type="reaction_summary",
                        event_id=f"{post_id}:summary",
                        metrics={"likes": d.get("like_count", 0),
                                 "comments": d.get("comments_count", 0), "shares": 0},
                    ))
            else:  # facebook
                r = await client.get(f"{GRAPH}/{post_id}/comments", params={
                    "fields": "id,from{id,name},message,created_time",
                    "filter": "stream", "access_token": self._token,
                })
                comments = r.json().get("data", []) if r.status_code == 200 else []
                for c in comments:
                    frm = c.get("from") or {}
                    events.append(EngagementEvent(
                        platform="facebook", content_item_id=content_item_id,
                        platform_post_id=post_id, type="comment",
                        event_id=c["id"],
                        engaged_user={"name": frm.get("name", ""),
                                      "external_id": frm.get("id", "")},
                        text=c.get("message", ""), occurred_at=c.get("created_time", ""),
                    ))
                r = await client.get(f"{GRAPH}/{post_id}", params={
                    "fields": "shares,likes.summary(true),comments.summary(true)",
                    "access_token": self._token,
                })
                if r.status_code == 200:
                    d = r.json()
                    events.append(EngagementEvent(
                        platform="facebook", content_item_id=content_item_id,
                        platform_post_id=post_id, type="reaction_summary",
                        event_id=f"{post_id}:summary",
                        metrics={
                            "likes": (d.get("likes", {}).get("summary", {}) or {}).get("total_count", 0),
                            "comments": (d.get("comments", {}).get("summary", {}) or {}).get("total_count", 0),
                            "shares": (d.get("shares") or {}).get("count", 0),
                        },
                    ))
        return events
