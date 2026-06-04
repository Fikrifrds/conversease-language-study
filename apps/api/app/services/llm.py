from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.domain.ai import ChatMessage, LLMProvider, LLMResult, ModelConfig


class LLMError(Exception):
    pass


class TogetherProvider(LLMProvider):
    """Together AI chat completions (OpenAI-compatible API)."""

    def __init__(self, *, api_key: str, base_url: str, timeout_seconds: int) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model_config: ModelConfig,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> LLMResult:
        payload: Dict[str, Any] = {
            "model": model_config.model,
            "messages": [{"role": message.role, "content": message.content} for message in messages],
            "temperature": model_config.temperature,
            "max_tokens": model_config.max_tokens,
        }
        if response_schema is not None:
            payload["response_format"] = {
                "type": "json_schema",
                "schema": response_schema,
            }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                response = await client.post(
                    f"{self._base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                body = response.json()
        except httpx.HTTPError as exc:
            raise LLMError("together_request_failed") from exc
        except ValueError as exc:
            raise LLMError("together_response_invalid_json") from exc

        choices = body.get("choices") or []
        if not choices:
            raise LLMError("together_response_empty")

        content = (choices[0].get("message") or {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMError("together_content_empty")

        return LLMResult(content=content, raw=body)


def get_llm_provider() -> Optional[LLMProvider]:
    """Return a configured provider, or None when LLM is not set up."""
    if settings.llm_default_provider == "together" and settings.together_api_key:
        return TogetherProvider(
            api_key=settings.together_api_key,
            base_url=settings.together_api_base_url,
            timeout_seconds=settings.together_timeout_seconds,
        )
    return None
