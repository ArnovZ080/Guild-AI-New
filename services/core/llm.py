"""
Guild-AI LLM Client
Primary: Vertex AI (Gemini 2.0 Flash / Gemini 2.0 Pro)
Fallback: Anthropic Claude (circuit breaker only)
No OpenAI. No Ollama.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
import logging

from services.core.config import settings

logger = logging.getLogger(__name__)


class ModelTier(Enum):
    FLASH = "flash"   # Fast, cheap — evaluations, simple content, routing
    PRO = "pro"       # Powerful — orchestration, strategy, long-form


# Semantic routing keywords → PRO tier
_PRO_KEYWORDS = {
    "strategy", "strategic", "business plan", "competitive analysis",
    "financial forecast", "market research", "investor", "fundraising",
    "architecture", "complex", "deep analysis", "evaluate", "orchestrat",
    "long-form", "comprehensive", "roadmap",
}


def classify_tier(goal: str) -> ModelTier:
    """Return PRO if the goal matches strategic keywords, else FLASH."""
    lower = goal.lower()
    for kw in _PRO_KEYWORDS:
        if kw in lower:
            return ModelTier.PRO
    return ModelTier.FLASH


class LLMClient:
    """
    Async LLM client.
    Primary: Vertex AI Gemini (Flash for simple, Pro for complex).
    Fallback: Anthropic Claude (circuit breaker — 3 consecutive failures).
    """

    def __init__(self):
        self._failure_count = 0
        self._failure_threshold = 3
        self._reset_timeout = 60
        self._next_retry_time = datetime.min
        self._vertex_available = False
        self._anthropic_client = None
        self._init_clients()

    def _init_clients(self):
        """Initialize Vertex AI and Anthropic clients."""
        # Primary: Vertex AI
        try:
            import vertexai
            vertexai.init(
                project=settings.GCP_PROJECT_ID,
                location=settings.GCP_LOCATION,
            )
            self._vertex_available = True
            logger.info("Vertex AI initialized (project=%s, location=%s).",
                        settings.GCP_PROJECT_ID, settings.GCP_LOCATION)
        except Exception as e:
            logger.warning("Vertex AI init failed: %s. Will rely on fallback.", e)

        # Fallback: Anthropic Claude
        try:
            import anthropic
            if settings.ANTHROPIC_API_KEY:
                self._anthropic_client = anthropic.AsyncAnthropic(
                    api_key=settings.ANTHROPIC_API_KEY,
                )
                logger.info("Anthropic Claude fallback initialized.")
            else:
                logger.warning("ANTHROPIC_API_KEY not set. No fallback available.")
        except ImportError:
            logger.warning("anthropic package not installed. No fallback available.")

    # ── Public API ──

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        tier: ModelTier = ModelTier.FLASH,
        max_tokens: int = 4096,
    ) -> str:
        """
        Generate a chat completion.
        Returns the text response. Raises RuntimeError if all providers fail.
        """
        # Circuit breaker check
        if self._failure_count >= self._failure_threshold:
            if datetime.now() < self._next_retry_time:
                logger.warning("Circuit breaker OPEN. Routing to Anthropic Claude.")
                return await self._anthropic_fallback(messages, temperature, max_tokens)
            else:
                logger.info("Circuit breaker half-open. Attempting Vertex AI...")

        # Primary: Vertex AI
        try:
            result = await self._vertex_generate(messages, temperature, tier, max_tokens)
            self._mark_success()
            return result
        except Exception as e:
            logger.error("Vertex AI generation failed: %s", e)
            self._mark_failure()
            return await self._anthropic_fallback(messages, temperature, max_tokens)

    # ── Vertex AI ──

    async def _vertex_generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        tier: ModelTier,
        max_tokens: int,
    ) -> str:
        """Generate using Vertex AI Gemini."""
        from vertexai.generative_models import GenerativeModel, GenerationConfig

        model_name = (
            settings.GEMINI_PRO_MODEL if tier == ModelTier.PRO
            else settings.GEMINI_FLASH_MODEL
        )

        # Separate system instruction from conversation contents
        system_instruction = None
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            text = msg.get("content", "")
            if role == "system":
                system_instruction = text
            elif role == "user":
                contents.append({"role": "user", "parts": [{"text": text}]})
            elif role == "assistant":
                contents.append({"role": "model", "parts": [{"text": text}]})

        # Build model (with or without system instruction)
        model_kwargs = {}
        if system_instruction:
            model_kwargs["system_instruction"] = system_instruction
        model = GenerativeModel(model_name, **model_kwargs)

        config = GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        response = await model.generate_content_async(
            contents=contents,
            generation_config=config,
        )
        return response.text

    # ── Anthropic Fallback ──

    async def _anthropic_fallback(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Fallback to Anthropic Claude when Vertex AI is down."""
        if not self._anthropic_client:
            raise RuntimeError(
                "All LLM providers unavailable. "
                "Vertex AI failed and no Anthropic fallback configured."
            )

        logger.info("Using Anthropic Claude fallback.")

        system_msg = None
        api_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                api_messages.append(msg)

        kwargs = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "messages": api_messages,
            "temperature": temperature,
        }
        if system_msg:
            kwargs["system"] = system_msg

        response = await self._anthropic_client.messages.create(**kwargs)
        return response.content[0].text

    # ── Circuit Breaker ──

    def _mark_success(self):
        self._failure_count = 0

    def _mark_failure(self):
        self._failure_count += 1
        if self._failure_count >= self._failure_threshold:
            self._next_retry_time = datetime.now() + timedelta(
                seconds=self._reset_timeout
            )
            logger.error(
                "Circuit breaker TRIPPED. Redirecting to Anthropic for %ds.",
                self._reset_timeout,
            )


# Global client
default_llm = LLMClient()
