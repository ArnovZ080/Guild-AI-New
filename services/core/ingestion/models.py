"""Normalized engagement events — the shared shape for polling AND future webhooks."""
from typing import Dict, Optional
from pydantic import BaseModel, Field


class EngagementEvent(BaseModel):
    platform: str                       # "facebook" | "instagram"
    content_item_id: str
    platform_post_id: str
    type: str                           # "comment" | "reaction_summary"
    event_id: str                       # platform-unique id (comment id / synthetic)
    engaged_user: Dict[str, str] = Field(default_factory=dict)
    text: str = ""
    occurred_at: str = ""
    metrics: Dict[str, int] = Field(default_factory=dict)
