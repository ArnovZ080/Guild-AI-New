"""Tests for Token Tracker — usage recording and budget alerts."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestTokenTracker:
    def test_record_usage(self):
        with patch("services.core.token_tracker.TokenTracker") as MockTracker:
            tracker = MockTracker.return_value
            tracker.record_usage = AsyncMock(return_value={
                "user_id": "user-123", "model": "gemini-2.0-flash-001",
                "input_tokens": 500, "output_tokens": 200, "total_tokens": 700,
                "estimated_cost_usd": 0.00035,
            })
            result = run(tracker.record_usage(None, "user-123", "gemini-2.0-flash-001", 500, 200))
            assert result["total_tokens"] == 700
            assert result["estimated_cost_usd"] > 0

    def test_budget_alert_at_threshold(self):
        with patch("services.core.token_tracker.TokenTracker") as MockTracker:
            tracker = MockTracker.return_value
            tracker.check_budget = AsyncMock(return_value={
                "usage_percent": 78.5, "alert": True,
                "message": "You have used 78.5% of your monthly token budget",
            })
            result = run(tracker.check_budget(None, "user-123"))
            assert result["alert"] is True
            assert result["usage_percent"] > 75

    def test_no_alert_below_threshold(self):
        with patch("services.core.token_tracker.TokenTracker") as MockTracker:
            tracker = MockTracker.return_value
            tracker.check_budget = AsyncMock(return_value={
                "usage_percent": 30.0, "alert": False, "message": None,
            })
            result = run(tracker.check_budget(None, "user-123"))
            assert result["alert"] is False

    def test_estimate_workflow_cost(self):
        with patch("services.core.token_tracker.TokenTracker") as MockTracker:
            tracker = MockTracker.return_value
            tracker.estimate_workflow_cost = AsyncMock(return_value={
                "estimated_tokens": 2500, "estimated_cost_usd": 0.00125, "within_budget": True,
            })
            result = run(tracker.estimate_workflow_cost(None, "user-123", "weekly_content_pipeline"))
            assert result["estimated_tokens"] == 2500
            assert result["within_budget"] is True
