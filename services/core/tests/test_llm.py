"""
Tests for the LLM client — model routing, circuit breaker, message conversion.
"""
import pytest
from unittest.mock import MagicMock, patch
from services.core.llm import LLMClient, ModelTier, classify_tier


@pytest.mark.skip(reason="Legacy LLM interface replaced by Vertex AI")
class TestModelRouting:
    """Test the semantic tier classifier."""

    def test_flash_for_standard_tasks(self):
        assert classify_tier("Write a blog post about SEO") == ModelTier.FLASH
        assert classify_tier("Create social media copy") == ModelTier.FLASH

    def test_pro_for_strategic_tasks(self):
        assert classify_tier("Build a business plan for Q4") == ModelTier.PRO
        assert classify_tier("Perform a competitive analysis") == ModelTier.PRO
        assert classify_tier("Create a financial forecast") == ModelTier.PRO
        assert classify_tier("Design system architecture review") == ModelTier.PRO

    def test_model_assignment(self):
        flash = LLMClient(tier=ModelTier.FLASH)
        assert "flash" in flash.model.lower()

        pro = LLMClient(tier=ModelTier.PRO)
        assert "pro" in pro.model.lower()


@pytest.mark.skip(reason="Legacy LLM interface replaced by Vertex AI")
class TestMessageConversion:
    """Test OpenAI-style to Gemini conversion."""

    def test_simple_user_message(self):
        messages = [{"role": "user", "content": "Hello"}]
        contents = LLMClient._convert_messages(messages)
        assert len(contents) == 1
        assert contents[0].role == "user"

    def test_system_message_prepended(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"},
        ]
        contents = LLMClient._convert_messages(messages)
        assert len(contents) == 1
        assert "helpful assistant" in contents[0].parts[0].text

    def test_assistant_mapped_to_model(self):
        messages = [
            {"role": "user", "content": "Hey"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
        ]
        contents = LLMClient._convert_messages(messages)
        assert len(contents) == 3
        assert contents[1].role == "model"

    def test_system_only_becomes_user(self):
        messages = [{"role": "system", "content": "You are a bot."}]
        contents = LLMClient._convert_messages(messages)
        assert len(contents) == 1
        assert contents[0].role == "user"


@pytest.mark.skip(reason="Legacy LLM interface replaced by Vertex AI")
class TestCircuitBreaker:
    """Test circuit breaker logic."""

    def test_initial_state(self):
        client = LLMClient()
        assert client._failure_count == 0

    def test_failure_tracking(self):
        client = LLMClient()
        client._mark_failure()
        assert client._failure_count == 1

    def test_success_resets(self):
        client = LLMClient()
        client._mark_failure()
        client._mark_failure()
        client._mark_success()
        assert client._failure_count == 0
