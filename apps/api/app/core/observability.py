import json
import logging
from collections import defaultdict
from threading import Lock
import time
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


request_id_context: ContextVar[str] = ContextVar("request_id", default="")


class RuntimeMetrics:
    def __init__(self, max_tracked_paths: int = 50) -> None:
        self.max_tracked_paths = max_tracked_paths
        self._lock = Lock()
        self.reset_for_tests()

    def reset_for_tests(self) -> None:
        with self._lock:
            self.started_at = time.time()
            self.total_requests = 0
            self.total_duration_ms = 0
            self.status_buckets: dict[str, int] = defaultdict(int)
            self.methods: dict[str, int] = defaultdict(int)
            self.paths: dict[str, int] = defaultdict(int)
            self.untracked_path_requests = 0

    def record(self, method: str, path: str, status_code: int, duration_ms: int) -> None:
        with self._lock:
            self.total_requests += 1
            self.total_duration_ms += duration_ms
            self.status_buckets[status_code_bucket(status_code)] += 1
            self.methods[method.upper()] += 1

            if path in self.paths or len(self.paths) < self.max_tracked_paths:
                self.paths[path] += 1
            else:
                self.untracked_path_requests += 1

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            average_duration_ms = (
                round(self.total_duration_ms / self.total_requests, 2)
                if self.total_requests
                else 0
            )
            return {
                "uptime_seconds": round(time.time() - self.started_at),
                "requests": {
                    "total": self.total_requests,
                    "average_duration_ms": average_duration_ms,
                    "status_buckets": dict(sorted(self.status_buckets.items())),
                    "methods": dict(sorted(self.methods.items())),
                    "paths": dict(sorted(self.paths.items())),
                    "untracked_path_requests": self.untracked_path_requests,
                },
            }


runtime_metrics = RuntimeMetrics()


def configure_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(message)s",
    )


def current_request_id() -> str:
    return request_id_context.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or f"req-{uuid4().hex[:16]}"
        request_id_context.set(request_id)
        started_at = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception:
            log_request(
                request=request,
                request_id=request_id,
                status_code=status_code,
                duration_ms=duration_ms(started_at),
                level=logging.ERROR,
                message="api_request_failed",
            )
            raise
        finally:
            duration = duration_ms(started_at)
            runtime_metrics.record(request.method, request.url.path, status_code, duration)
            if "response" in locals():
                response.headers["x-request-id"] = request_id
                apply_security_headers(response.headers)

                if settings.enable_request_logging:
                    log_request(
                        request=request,
                        request_id=request_id,
                        status_code=status_code,
                        duration_ms=duration,
                    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = current_request_id() or request.headers.get("x-request-id") or f"req-{uuid4().hex[:16]}"
    logging.getLogger("conversease.api").exception(
        json.dumps(
            {
                "event": "unhandled_exception",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "release_version": settings.release_version,
            }
        )
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
        },
        headers={
            "x-request-id": request_id,
            **security_headers(),
        },
    )


def security_headers() -> dict[str, str]:
    return {
        "x-content-type-options": "nosniff",
        "x-frame-options": "DENY",
        "referrer-policy": "strict-origin-when-cross-origin",
        "permissions-policy": "camera=(), microphone=(self), geolocation=()",
    }


def apply_security_headers(headers) -> None:
    for name, value in security_headers().items():
        headers[name] = value


def duration_ms(started_at: float) -> int:
    return round((time.perf_counter() - started_at) * 1000)


def status_code_bucket(status_code: int) -> str:
    if status_code < 100 or status_code > 599:
        return "unknown"
    return f"{status_code // 100}xx"


def log_request(
    request: Request,
    request_id: str,
    status_code: int,
    duration_ms: int,
    level: int = logging.INFO,
    message: str = "api_request",
) -> None:
    logging.getLogger("conversease.api").log(
        level,
        json.dumps(
            {
                "event": message,
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "release_version": settings.release_version,
            }
        ),
    )
