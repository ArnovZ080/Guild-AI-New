"""
Centralized JSON extraction utility for LLM responses.
Replaces duplicated _extract_json / _parse_json methods across agent files.
"""
import json
import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def extract_json_from_llm_response(
    text: str,
    fallback: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Extract a JSON object from an LLM response string.

    Handles:
    1. ```json ... ``` fenced code blocks
    2. ``` ... ``` generic fenced code blocks
    3. Raw JSON objects (outermost { ... })
    4. Graceful fallback to empty dict or provided fallback

    Args:
        text: The raw LLM response string.
        fallback: Optional dict to return if extraction fails.
                  Defaults to empty dict.

    Returns:
        Parsed JSON as a dictionary.
    """
    if fallback is None:
        fallback = {}

    if not text or not isinstance(text, str):
        return fallback

    # Strategy 1: ```json ... ``` block
    json_block_match = re.search(r'```json\s*\n?(.*?)```', text, re.DOTALL)
    if json_block_match:
        try:
            return json.loads(json_block_match.group(1).strip())
        except (json.JSONDecodeError, ValueError):
            pass

    # Strategy 2: ``` ... ``` generic block (may contain JSON)
    generic_block_match = re.search(r'```\s*\n?(.*?)```', text, re.DOTALL)
    if generic_block_match:
        candidate = generic_block_match.group(1).strip()
        if candidate.startswith('{'):
            try:
                return json.loads(candidate)
            except (json.JSONDecodeError, ValueError):
                pass

    # Strategy 3: Find outermost { ... } in raw text
    if '{' in text:
        try:
            start = text.index('{')
            # Find matching closing brace by counting depth
            depth = 0
            end = start
            for i, ch in enumerate(text[start:], start):
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        end = i
                        break

            if end > start:
                return json.loads(text[start:end + 1])
        except (json.JSONDecodeError, ValueError, IndexError):
            pass

    # Strategy 4: Fallback
    logger.debug("JSON extraction failed, returning fallback")
    return fallback
