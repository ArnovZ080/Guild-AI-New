"""Unit tests for the Meta loop: crypto, state, banding, dedupe logic."""
import pytest

from services.core.security.crypto import encrypt, decrypt
from services.core.integrations import oauth_state
from services.core.ingestion.service import _score_band
from services.core.ingestion.models import EngagementEvent


def test_crypto_roundtrip():
    assert decrypt(encrypt("page-token-123")) == "page-token-123"


def test_state_single_use():
    s = oauth_state.create_state("u1", "meta")
    assert oauth_state.pop_state(s) == {"user_id": "u1", "platform": "meta"}
    assert oauth_state.pop_state(s) is None


def test_state_unknown():
    assert oauth_state.pop_state("nonsense") is None


@pytest.mark.parametrize("likes,comments,expected", [
    (50, 5, "excellent"), (10, 1, "good"), (3, 0, "neutral"),
    (1, 0, "poor"), (0, 0, "failed"),
])
def test_score_band(likes, comments, expected):
    assert _score_band(likes, comments) == expected


def test_engagement_event_shape():
    ev = EngagementEvent(platform="instagram", content_item_id="c1",
                         platform_post_id="p1", type="comment", event_id="e1",
                         engaged_user={"name": "Sam"}, text="love this!")
    assert ev.metrics == {} and ev.engaged_user["name"] == "Sam"
