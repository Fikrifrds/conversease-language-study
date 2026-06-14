"""In-process LLM usage + cost observability.

Every successful LLM call records its token usage here. An admin endpoint reads
the aggregates so operators can watch spend without a third-party tool.

Scope: this is an in-memory, per-process aggregate (like the rate limiter). It
resets on restart and is not shared across workers — enough for beta cost
visibility. Durable per-user cost analytics can later sink the same events to a
database or a log-based metric.
"""
from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Estimated price in USD per 1,000,000 tokens (input, output). Matched by a
# case-insensitive substring of the model id; the first match wins. These are
# approximations for cost visibility, not billing.
MODEL_PRICES_USD_PER_MTOK: tuple[tuple[str, float, float], ...] = (
    ("llama-3.3-70b", 0.88, 0.88),
    ("llama-3.1-8b", 0.18, 0.18),
    ("gpt-4.1-mini", 0.40, 1.60),
    ("gpt-4.1", 2.00, 8.00),
    ("gpt-4o-mini", 0.15, 0.60),
)
DEFAULT_PRICE_USD_PER_MTOK = (0.50, 1.50)


def _prices_for(model: str) -> tuple[float, float]:
    needle = (model or "").lower()
    for key, prompt_price, completion_price in MODEL_PRICES_USD_PER_MTOK:
        if key in needle:
            return prompt_price, completion_price
    return DEFAULT_PRICE_USD_PER_MTOK


def estimate_cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    prompt_price, completion_price = _prices_for(model)
    return (
        prompt_tokens * prompt_price + completion_tokens * completion_price
    ) / 1_000_000


@dataclass
class UsageBucket:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0

    def add(self, prompt: int, completion: int, total: int, cost: float) -> None:
        self.calls += 1
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.total_tokens += total
        self.estimated_cost_usd += cost

    def as_dict(self) -> Dict[str, Any]:
        return {
            "calls": self.calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": round(self.estimated_cost_usd, 4),
        }


@dataclass
class LlmUsageRegistry:
    _lock: threading.Lock = field(default_factory=threading.Lock)
    total: UsageBucket = field(default_factory=UsageBucket)
    by_model: Dict[str, UsageBucket] = field(default_factory=lambda: defaultdict(UsageBucket))
    by_day: Dict[str, UsageBucket] = field(default_factory=lambda: defaultdict(UsageBucket))
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def record(
        self,
        *,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: Optional[int] = None,
    ) -> None:
        prompt = max(0, int(prompt_tokens or 0))
        completion = max(0, int(completion_tokens or 0))
        total = int(total_tokens) if total_tokens is not None else prompt + completion
        cost = estimate_cost_usd(model, prompt, completion)
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        model_key = f"{provider}:{model}"
        with self._lock:
            self.total.add(prompt, completion, total, cost)
            self.by_model[model_key].add(prompt, completion, total, cost)
            self.by_day[day].add(prompt, completion, total, cost)

    def snapshot(self) -> Dict[str, Any]:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with self._lock:
            return {
                "since": self.started_at.isoformat(),
                "total": self.total.as_dict(),
                "today": self.by_day.get(today, UsageBucket()).as_dict(),
                "by_model": {key: bucket.as_dict() for key, bucket in sorted(self.by_model.items())},
                "by_day": {day: bucket.as_dict() for day, bucket in sorted(self.by_day.items())},
            }

    def reset(self) -> None:
        with self._lock:
            self.total = UsageBucket()
            self.by_model = defaultdict(UsageBucket)
            self.by_day = defaultdict(UsageBucket)
            self.started_at = datetime.now(timezone.utc)


llm_usage_registry = LlmUsageRegistry()


def record_llm_usage_from_raw(*, provider: str, model: str, raw: Optional[Dict[str, Any]]) -> None:
    """Record usage from an OpenAI-compatible response body's `usage` block.

    Never raises: usage tracking must not break an LLM call.
    """
    try:
        usage = (raw or {}).get("usage") or {}
        llm_usage_registry.record(
            provider=provider,
            model=model,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens"),
        )
    except Exception:  # noqa: BLE001 - observability must be side-effect-safe
        pass
