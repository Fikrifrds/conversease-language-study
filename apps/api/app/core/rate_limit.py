from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.observability import current_request_id, security_headers


AUTH_RATE_LIMIT_PATHS = {
    "/api/auth/register",
    "/api/auth/login",
    "/api/auth/forgot-password",
    "/api/auth/reset-password",
    "/api/auth/verify-email",
    "/api/auth/google/session",
    "/api/auth/request-email-verification",
}


@dataclass
class RateLimitBucket:
    window_started_at: float
    count: int


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self.buckets: dict[str, RateLimitBucket] = {}

    def hit(self, key: str, *, limit: int, window_seconds: int, now: Optional[float] = None) -> int:
        current_time = now if now is not None else time.monotonic()
        bucket = self.buckets.get(key)

        if bucket is None or current_time - bucket.window_started_at >= window_seconds:
            self.buckets[key] = RateLimitBucket(window_started_at=current_time, count=1)
            return limit - 1

        bucket.count += 1
        return limit - bucket.count

    def reset(self) -> None:
        self.buckets.clear()


rate_limiter = InMemoryRateLimiter()


@dataclass
class FailedLoginEntry:
    window_started_at: float
    count: int


class LoginAttemptTracker:
    """Tracks consecutive failed logins per account so a single email can be
    locked out across all source IPs. Distinct from the rate limiter: only
    failures count, and a success clears the account's counter.
    """

    def __init__(self) -> None:
        self.entries: dict[str, FailedLoginEntry] = {}

    def is_locked(self, key: str, *, max_attempts: int, window_seconds: int, now: Optional[float] = None) -> bool:
        current_time = now if now is not None else time.monotonic()
        entry = self.entries.get(key)
        if entry is None:
            return False
        if current_time - entry.window_started_at >= window_seconds:
            del self.entries[key]
            return False
        return entry.count >= max_attempts

    def register_failure(self, key: str, *, window_seconds: int, now: Optional[float] = None) -> None:
        current_time = now if now is not None else time.monotonic()
        entry = self.entries.get(key)
        if entry is None or current_time - entry.window_started_at >= window_seconds:
            self.entries[key] = FailedLoginEntry(window_started_at=current_time, count=1)
            return
        entry.count += 1

    def reset_key(self, key: str) -> None:
        self.entries.pop(key, None)

    def reset(self) -> None:
        self.entries.clear()


login_attempts = LoginAttemptTracker()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rule = rate_limit_rule(request)
        if not settings.rate_limit_enabled or rule is None:
            return await call_next(request)

        rule_name, limit = rule
        key = rate_limit_key(request, rule_name)
        remaining = rate_limiter.hit(
            key,
            limit=limit,
            window_seconds=settings.rate_limit_window_seconds,
        )

        if remaining < 0:
            request_id = current_request_id() or request.headers.get("x-request-id", "")
            headers = {
                **security_headers(),
                "retry-after": str(settings.rate_limit_window_seconds),
                "x-ratelimit-limit": str(limit),
                "x-ratelimit-remaining": "0",
            }
            if request_id:
                headers["x-request-id"] = request_id

            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers=headers,
            )

        response = await call_next(request)
        response.headers["x-ratelimit-limit"] = str(limit)
        response.headers["x-ratelimit-remaining"] = str(max(remaining, 0))
        return response


def rate_limit_rule(request: Request) -> Optional[tuple[str, int]]:
    if request.method == "OPTIONS":
        return None

    path = request.url.path
    if path in AUTH_RATE_LIMIT_PATHS:
        return ("auth", settings.auth_rate_limit_requests)

    if path.startswith("/api/admin/"):
        return ("admin", settings.admin_rate_limit_requests)

    # Conversation turns each trigger a paid LLM/STT call. Limit POSTs to the
    # turn endpoints so abuse cannot burn provider cost unbounded.
    if request.method == "POST" and _is_conversation_turn_path(path):
        return ("conversation", settings.conversation_rate_limit_requests)

    return None


def _is_conversation_turn_path(path: str) -> bool:
    # Conversation Coach turns.
    if path.startswith("/api/conversation-sessions/") and (
        path.endswith("/turns") or path.endswith("/turns/audio")
    ):
        return True
    # Conversation Partner turns (each one costs STT + LLM + TTS).
    if path.startswith("/api/conversation-partner/sessions/") and path.endswith("/turns/audio"):
        return True
    return False


def rate_limit_key(request: Request, rule_name: str) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    client_ip = forwarded_for.split(",")[0].strip()
    if not client_ip and request.client:
        client_ip = request.client.host
    if not client_ip:
        client_ip = "unknown"

    # Conversation turns share one bucket per client (the path carries a dynamic
    # session id), so the limit applies across all of a user's sessions.
    if rule_name == "conversation":
        return f"{rule_name}:{client_ip}"

    return f"{rule_name}:{client_ip}:{request.url.path}"
