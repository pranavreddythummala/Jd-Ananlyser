"""
Shared helper for making LLM calls across nodes.

Keeps the actual anthropic client + API call logic in one place so
individual nodes just describe what prompt to send and how to parse
the response, without repeating client setup.
"""

import json
import logging

import anthropic

from src.config import MODEL_NAME

logger = logging.getLogger(__name__)

_client = anthropic.Anthropic()


def call_llm(prompt: str, max_tokens: int = 1024, model: str | None = None) -> str:
    """Send a prompt to Claude, return the raw text response."""
    response = _client.messages.create(
        model=model or MODEL_NAME,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def call_llm_for_lines(prompt: str, max_tokens: int = 1024) -> list[str]:
    """
    Send a prompt expecting a plain line-per-item response
    (used by jd_parser fallback, qualification_extractor).
    """
    text = call_llm(prompt, max_tokens=max_tokens)
    lines = [line.strip("- ").strip() for line in text.splitlines()]
    result = [line for line in lines if line]

    if not result:
        logger.warning("call_llm_for_lines: LLM returned no usable lines")

    return result


def call_llm_for_json(prompt: str, max_tokens: int = 1024) -> dict:
    """
    Send a prompt expecting a JSON object response
    (used by skill_ranker).
    """
    text = call_llm(prompt, max_tokens=max_tokens)
    cleaned = text.strip()

    # Strip markdown code fences if the model wraps the JSON in them
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.error("call_llm_for_json: failed to parse LLM response as JSON: %r", text)
        raise