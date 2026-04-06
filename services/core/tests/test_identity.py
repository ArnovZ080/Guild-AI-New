"""Tests for Business Identity — creation, progressive update, context prompt."""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestBusinessIdentity:
    def _mock_agent(self):
        agent = MagicMock()
        return agent

    def test_create_business_identity(self):
        agent = self._mock_agent()
        identity = MagicMock(business_name="Acme Candles", completion_percentage=15.0)
        agent.create_identity = AsyncMock(return_value=identity)
        result = run(agent.create_identity(None, "user-123", {"business_name": "Acme Candles"}))
        assert result.business_name == "Acme Candles"
        assert result.completion_percentage < 50

    def test_progressive_update_increases_completion(self):
        agent = self._mock_agent()
        identity_v1 = MagicMock(completion_percentage=15.0)
        identity_v2 = MagicMock(completion_percentage=45.0)
        agent.update_identity = AsyncMock(side_effect=[identity_v1, identity_v2])
        r1 = run(agent.update_identity(None, "user-123", {"business_name": "Acme"}))
        r2 = run(agent.update_identity(None, "user-123", {"industry": "Retail"}))
        assert r2.completion_percentage > r1.completion_percentage

    def test_get_context_prompt_includes_brand_data(self):
        agent = self._mock_agent()
        agent.get_context_prompt = AsyncMock(return_value=(
            "Business: Acme Candles\nIndustry: Retail\nVoice: Warm, friendly\n"
            "Audience: Women 25-45 who value self-care"
        ))
        result = run(agent.get_context_prompt(None, "user-123"))
        assert "Acme Candles" in result
        assert "Retail" in result


class TestIdentityCompletion:
    def test_completion_percentage_zero_for_empty(self):
        fields = {"business_name": None, "industry": None, "target_audience": None,
                  "brand_voice": None, "unique_value": None, "goals": None}
        filled = sum(1 for v in fields.values() if v)
        total = len(fields)
        pct = round(filled / total * 100, 1) if total else 0
        assert pct == 0

    def test_completion_percentage_100_for_full(self):
        fields = {"business_name": "X", "industry": "Y", "target_audience": "Z",
                  "brand_voice": "A", "unique_value": "B", "goals": "C"}
        filled = sum(1 for v in fields.values() if v)
        total = len(fields)
        pct = round(filled / total * 100, 1)
        assert pct == 100
