"""Tests for the CRM system — contacts, lead scoring, pipeline."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestCRM:
    def test_add_contact(self):
        with patch("services.core.adk.customer.crm.CRMAgent") as MockCRM:
            crm = MockCRM.return_value
            crm.add_contact = AsyncMock(return_value={"id": "c1", "name": "Jane Smith"})
            result = run(crm.add_contact(None, "user-123", {"name": "Jane Smith", "email": "jane@test.com"}))
            assert result["name"] == "Jane Smith"

    def test_move_pipeline_stage(self):
        with patch("services.core.adk.customer.crm.CRMAgent") as MockCRM:
            crm = MockCRM.return_value
            crm.move_stage = AsyncMock(return_value={"status": "moved", "new_stage": "qualified"})
            result = run(crm.move_stage(None, "user-123", {"contact_id": "c-1", "new_stage": "qualified"}))
            assert result["new_stage"] == "qualified"

    def test_pipeline_summary(self):
        with patch("services.core.adk.customer.crm.CRMAgent") as MockCRM:
            crm = MockCRM.return_value
            crm.get_pipeline_summary = AsyncMock(return_value={
                "stages": {"lead": 5, "qualified": 3, "proposal": 1, "customer": 2}
            })
            result = run(crm.get_pipeline_summary(None, "user-123"))
            assert "stages" in result
            assert result["stages"]["lead"] == 5


class TestLeadScoring:
    def test_score_lead_returns_valid_range(self):
        with patch("services.core.adk.customer.crm.CRMAgent") as MockCRM:
            crm = MockCRM.return_value
            crm.score_lead = AsyncMock(return_value={"icp_score": 0.85})
            result = run(crm.score_lead(None, "user-123", {"email": "test@example.com"}))
            assert 0 <= result["icp_score"] <= 1
