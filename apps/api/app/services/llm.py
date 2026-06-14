from __future__ import annotations

import asyncio
import logging
import random
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.core.llm_usage import record_llm_usage_from_raw
from app.domain.ai import ChatMessage, LLMProvider, LLMResult, ModelConfig


class LLMError(Exception):
    pass


logger = logging.getLogger(__name__)


class TogetherProvider(LLMProvider):
    """Together AI chat completions (OpenAI-compatible API)."""

    def __init__(self, *, api_key: str, base_url: str, timeout_seconds: int) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout_seconds)
        return self._client

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
            # Together's broadly supported JSON mode. The callers' parsers are
            # lenient, so we ask for a JSON object rather than a strict schema
            # (which some Together models reject with a 400).
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        request_url = f"{self._base_url}/v1/chat/completions"
        client = self._get_client()

        # Three tries: enough to absorb a transient 429/5xx/timeout (common cause
        # of the conversation partner falling back) plus one retry after dropping
        # response_format if the model rejects JSON mode.
        last_error: Optional[Exception] = None
        for attempt in range(3):
            started = asyncio.get_running_loop().time()
            try:
                response = await client.post(
                    request_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                body = response.json()
                elapsed_ms = int((asyncio.get_running_loop().time() - started) * 1000)
                logger.info(
                    "llm_together_ok model=%s tokens=%s attempt=%s duration_ms=%s",
                    model_config.model,
                    model_config.max_tokens,
                    attempt + 1,
                    elapsed_ms,
                )
                break
            except httpx.HTTPStatusError as exc:
                elapsed_ms = int((asyncio.get_running_loop().time() - started) * 1000)
                status = exc.response.status_code
                logger.warning(
                    "llm_together_status_error model=%s status=%s attempt=%s duration_ms=%s",
                    model_config.model,
                    status,
                    attempt + 1,
                    elapsed_ms,
                )
                last_error = exc
                # A 400 may mean the model rejected JSON mode: drop it and retry.
                if status == 400 and "response_format" in payload and attempt < 2:
                    payload.pop("response_format", None)
                    continue
                retryable = status in {408, 429, 500, 502, 503, 504}
                if retryable and attempt < 2:
                    await asyncio.sleep(0.35 + random.random() * 0.5)
                    continue
                raise LLMError(f"together_status_{status}") from exc
            except httpx.HTTPError as exc:
                elapsed_ms = int((asyncio.get_running_loop().time() - started) * 1000)
                logger.warning(
                    "llm_together_http_error model=%s attempt=%s duration_ms=%s",
                    model_config.model,
                    attempt + 1,
                    elapsed_ms,
                )
                last_error = exc
                if attempt < 2:
                    await asyncio.sleep(0.35 + random.random() * 0.5)
                    continue
                raise LLMError("together_request_failed") from exc
            except ValueError as exc:
                last_error = exc
                raise LLMError("together_response_invalid_json") from exc
        else:
            raise LLMError("together_request_failed") from last_error

        choices = body.get("choices") or []
        if not choices:
            raise LLMError("together_response_empty")

        content = (choices[0].get("message") or {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMError("together_content_empty")

        record_llm_usage_from_raw(provider="together", model=model_config.model, raw=body)
        return LLMResult(content=content, raw=body)


class OpenAIProvider(LLMProvider):
    def __init__(self, *, api_key: str, base_url: str, timeout_seconds: int) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout_seconds)
        return self._client

    async def generate_chat_completion(
        self,
        messages: List[ChatMessage],
        model_config: ModelConfig,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> LLMResult:
        schema_payload: Optional[Dict[str, Any]] = None
        if response_schema is not None:
            schema_payload = {
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "schema": response_schema,
                    "strict": True,
                },
            }

        payload: Dict[str, Any] = {
            "model": model_config.model,
            "messages": [{"role": message.role, "content": message.content} for message in messages],
            "temperature": model_config.temperature,
            "max_tokens": model_config.max_tokens,
        }
        if schema_payload is not None:
            payload["response_format"] = schema_payload

        prefer_json_object = model_config.model.startswith("gpt-4.1-")
        if prefer_json_object and response_schema is not None:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        request_url = f"{self._base_url}/v1/chat/completions"
        client = self._get_client()

        # Three tries: absorb a transient 429 (rate limit) / 5xx / timeout — the
        # common cause of the conversation partner falling back — plus a retry
        # after relaxing a rejected strict schema to JSON mode.
        last_error: Optional[Exception] = None
        for attempt in range(3):
            started = asyncio.get_running_loop().time()
            try:
                response = await client.post(
                    request_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                body = response.json()
                elapsed_ms = int((asyncio.get_running_loop().time() - started) * 1000)
                logger.info(
                    "llm_openai_ok model=%s tokens=%s attempt=%s duration_ms=%s",
                    model_config.model,
                    model_config.max_tokens,
                    attempt + 1,
                    elapsed_ms,
                )
                break
            except httpx.HTTPStatusError as exc:
                elapsed_ms = int((asyncio.get_running_loop().time() - started) * 1000)
                status = exc.response.status_code
                detail = ""
                try:
                    detail = " ".join(exc.response.text[:300].split())
                except Exception:
                    detail = ""
                logger.warning(
                    "llm_openai_status_error model=%s status=%s attempt=%s duration_ms=%s detail=%s",
                    model_config.model,
                    status,
                    attempt + 1,
                    elapsed_ms,
                    detail,
                )
                last_error = exc
                schema_rejected = (
                    status == 400
                    and isinstance(payload.get("response_format"), dict)
                    and payload["response_format"].get("type") == "json_schema"
                    and attempt < 2
                    and any(
                        needle in detail.lower()
                        for needle in (
                            "response_format",
                            "json_schema",
                            "schema",
                            "invalid",
                        )
                    )
                )
                if schema_rejected:
                    payload["response_format"] = {"type": "json_object"}
                    await asyncio.sleep(0.1)
                    continue
                retryable = status in {408, 429, 500, 502, 503, 504}
                if retryable and attempt < 2:
                    await asyncio.sleep(0.35 + random.random() * 0.5)
                    continue
                raise LLMError(f"openai_status_{status}") from exc
            except httpx.HTTPError as exc:
                elapsed_ms = int((asyncio.get_running_loop().time() - started) * 1000)
                logger.warning(
                    "llm_openai_http_error model=%s attempt=%s duration_ms=%s",
                    model_config.model,
                    attempt + 1,
                    elapsed_ms,
                )
                last_error = exc
                if attempt < 2:
                    await asyncio.sleep(0.35 + random.random() * 0.5)
                    continue
                raise LLMError("openai_request_failed") from exc
            except ValueError as exc:
                last_error = exc
                raise LLMError("openai_response_invalid_json") from exc
        else:
            raise LLMError("openai_request_failed") from last_error

        choices = body.get("choices") or []
        if not choices:
            raise LLMError("openai_response_empty")

        content = (choices[0].get("message") or {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMError("openai_content_empty")

        record_llm_usage_from_raw(provider="openai", model=model_config.model, raw=body)
        return LLMResult(content=content, raw=body)


_together_singleton: Optional[TogetherProvider] = None
_openai_singleton: Optional[OpenAIProvider] = None


def get_llm_provider() -> Optional[LLMProvider]:
    """Return a configured provider, or None when LLM is not set up."""
    if settings.llm_default_provider == "together" and settings.together_api_key:
        global _together_singleton
        if _together_singleton is None:
            _together_singleton = TogetherProvider(
                api_key=settings.together_api_key,
                base_url=settings.together_api_base_url,
                timeout_seconds=settings.together_timeout_seconds,
            )
        return _together_singleton
    if settings.llm_default_provider == "openai" and settings.openai_api_key:
        global _openai_singleton
        if _openai_singleton is None:
            _openai_singleton = OpenAIProvider(
                api_key=settings.openai_api_key,
                base_url=settings.openai_api_base_url,
                timeout_seconds=settings.openai_timeout_seconds,
            )
        return _openai_singleton
    return None
