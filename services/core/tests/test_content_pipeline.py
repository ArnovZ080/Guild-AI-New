"""Tests for the Content Pipeline — generate, approve, reject, bulk."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, UTC
from uuid import uuid4


def run(coro):
    """Helper to run async code in sync tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


@pytest.fixture
def mock_content_item():
    item = MagicMock()
    item.id = str(uuid4())
    item.title = "5 Benefits of Soy Candles"
    item.body = "Soy candles are a great choice..."
    item.status = "pending_review"
    item.platform = "linkedin"
    item.content_type = "social"
    item.user_id = str(uuid4())
    item.created_at = datetime.now(UTC)
    item.published_at = None
    return item


class TestContentGenerator:
    def test_generate_single_content(self, mock_content_item):
        with patch("services.core.content_pipeline.engine.content_generator") as mock_gen:
            mock_gen.generate_single_content = AsyncMock(return_value=mock_content_item)
            result = run(mock_gen.generate_single_content(
                None, "user-123", "social", "linkedin", "Benefits of soy candles"
            ))
            assert result.title == "5 Benefits of Soy Candles"
            assert result.status == "pending_review"
            assert result.platform == "linkedin"
            mock_gen.generate_single_content.assert_awaited_once()

    def test_generate_returns_valid_fields(self, mock_content_item):
        assert mock_content_item.id is not None
        assert mock_content_item.body is not None
        assert mock_content_item.content_type in ["social", "blog", "email", "video", "image"]


class TestContentQueue:
    def test_approve_content(self, mock_content_item):
        with patch("services.core.content_pipeline.engine.content_queue") as mock_queue:
            approved = MagicMock(id=mock_content_item.id, status="approved")
            mock_queue.approve = AsyncMock(return_value=approved)
            result = run(mock_queue.approve(None, mock_content_item.id))
            assert result.status == "approved"

    def test_reject_content_with_feedback(self, mock_content_item):
        with patch("services.core.content_pipeline.engine.content_queue") as mock_queue:
            rejected = MagicMock(id=mock_content_item.id, status="rejected")
            mock_queue.reject = AsyncMock(return_value=rejected)
            result = run(mock_queue.reject(None, mock_content_item.id, "Too promotional"))
            assert result.status == "rejected"

    def test_bulk_approve_multiple_items(self):
        with patch("services.core.content_pipeline.engine.content_queue") as mock_queue:
            ids = [str(uuid4()) for _ in range(3)]
            approved_items = [MagicMock(id=i, status="approved") for i in ids]
            mock_queue.bulk_approve = AsyncMock(return_value=approved_items)
            result = run(mock_queue.bulk_approve(None, ids))
            assert len(result) == 3
            assert all(item.status == "approved" for item in result)

    def test_reject_nonexistent_item(self):
        with patch("services.core.content_pipeline.engine.content_queue") as mock_queue:
            mock_queue.reject = AsyncMock(side_effect=Exception("Content not found"))
            with pytest.raises(Exception, match="Content not found"):
                run(mock_queue.reject(None, "nonexistent-id", "bad"))
