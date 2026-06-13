from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass
class SmokeResult:
    name: str
    status: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


def normalize_api_base_url(value: str) -> str:
    base = value.rstrip("/")
    if base.endswith("/api"):
        return base
    return f"{base}/api"


def normalize_web_base_url(value: str) -> str:
    return value.rstrip("/")


def join_url(base_url: str, path: str) -> str:
    return urljoin(f"{base_url.rstrip('/')}/", path.lstrip("/"))


def request_json(
    method: str,
    url: str,
    payload: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
    timeout: int = 10,
) -> tuple[int, dict[str, Any], float]:
    body = None
    request_headers = {"Accept": "application/json", **(headers or {})}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"

    request = Request(url, data=body, headers=request_headers, method=method)
    started_at = time.perf_counter()
    with urlopen(request, timeout=timeout) as response:
        response_body = response.read().decode("utf-8")
        elapsed_ms = round((time.perf_counter() - started_at) * 1000)
        return response.status, json.loads(response_body), elapsed_ms


def request_text(url: str, timeout: int = 10) -> tuple[int, str, float]:
    request = Request(url, headers={"Accept": "text/html"}, method="GET")
    started_at = time.perf_counter()
    with urlopen(request, timeout=timeout) as response:
        response_body = response.read(500_000).decode("utf-8", errors="replace")
        elapsed_ms = round((time.perf_counter() - started_at) * 1000)
        return response.status, response_body, elapsed_ms


def request_text_with_headers(url: str, timeout: int = 10) -> tuple[int, str, dict[str, str], float]:
    request = Request(url, headers={"Accept": "text/html"}, method="GET")
    started_at = time.perf_counter()
    with urlopen(request, timeout=timeout) as response:
        response_body = response.read(500_000).decode("utf-8", errors="replace")
        elapsed_ms = round((time.perf_counter() - started_at) * 1000)
        return response.status, response_body, dict(response.headers.items()), elapsed_ms


def api_check(name: str, api_base_url: str, path: str, validate) -> SmokeResult:
    url = join_url(api_base_url, path)
    try:
        status, payload, elapsed_ms = request_json("GET", url)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SmokeResult(
            name=name,
            status="fail",
            message=f"GET {path} failed.",
            details={"url": url, "error": safe_error(exc)},
        )

    issue = validate(payload)
    return SmokeResult(
        name=name,
        status="fail" if issue else "pass",
        message=issue or f"GET {path} returned expected payload.",
        details={"url": url, "status_code": status, "duration_ms": elapsed_ms},
    )


def admin_post_check(
    name: str,
    api_base_url: str,
    path: str,
    payload: dict[str, Any],
    admin_api_key: str,
    validate,
) -> SmokeResult:
    url = join_url(api_base_url, path)
    try:
        status, response_payload, elapsed_ms = request_json(
            "POST",
            url,
            payload=payload,
            headers={"x-admin-api-key": admin_api_key},
        )
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SmokeResult(
            name=name,
            status="fail",
            message=f"POST {path} failed.",
            details={"url": url, "error": safe_error(exc)},
        )

    issue = validate(response_payload)
    return SmokeResult(
        name=name,
        status="fail" if issue else "pass",
        message=issue or f"POST {path} returned expected payload.",
        details={"url": url, "status_code": status, "duration_ms": elapsed_ms},
    )


def admin_get_check(name: str, api_base_url: str, path: str, admin_api_key: str, validate) -> SmokeResult:
    url = join_url(api_base_url, path)
    try:
        status, payload, elapsed_ms = request_json(
            "GET",
            url,
            headers={"x-admin-api-key": admin_api_key},
        )
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SmokeResult(
            name=name,
            status="fail",
            message=f"GET {path} failed.",
            details={"url": url, "error": safe_error(exc)},
        )

    issue = validate(payload)
    return SmokeResult(
        name=name,
        status="fail" if issue else "pass",
        message=issue or f"GET {path} returned expected payload.",
        details={"url": url, "status_code": status, "duration_ms": elapsed_ms},
    )


def web_check(name: str, web_base_url: str, path: str, expected_text: str) -> SmokeResult:
    url = join_url(web_base_url, path)
    try:
        status, body, elapsed_ms = request_text(url)
    except (HTTPError, URLError, TimeoutError) as exc:
        return SmokeResult(
            name=name,
            status="fail",
            message=f"GET {path} failed.",
            details={"url": url, "error": safe_error(exc)},
        )

    if expected_text not in body:
        return SmokeResult(
            name=name,
            status="fail",
            message=f"GET {path} did not include expected text.",
            details={"url": url, "status_code": status, "expected_text": expected_text},
        )

    return SmokeResult(
        name=name,
        status="pass",
        message=f"GET {path} rendered expected text.",
        details={"url": url, "status_code": status, "duration_ms": elapsed_ms},
    )


def web_security_headers_check(web_base_url: str) -> SmokeResult:
    url = join_url(web_base_url, "/")
    try:
        status, _body, headers, elapsed_ms = request_text_with_headers(url)
    except (HTTPError, URLError, TimeoutError) as exc:
        return SmokeResult(
            name="web_security_headers",
            status="fail",
            message="GET / failed while checking web security headers.",
            details={"url": url, "error": safe_error(exc)},
        )

    normalized_headers = {key.lower(): value for key, value in headers.items()}
    expected_headers = {
        "x-content-type-options": "nosniff",
        "x-frame-options": "DENY",
        "referrer-policy": "strict-origin-when-cross-origin",
        "permissions-policy": "camera=(), microphone=(self), geolocation=()",
    }
    missing_or_wrong = {
        key: {"expected": value, "actual": normalized_headers.get(key)}
        for key, value in expected_headers.items()
        if normalized_headers.get(key) != value
    }

    if missing_or_wrong:
        return SmokeResult(
            name="web_security_headers",
            status="fail",
            message="Web response is missing required security headers.",
            details={"url": url, "status_code": status, "headers": missing_or_wrong},
        )

    return SmokeResult(
        name="web_security_headers",
        status="pass",
        message="Web response includes required security headers.",
        details={"url": url, "status_code": status, "duration_ms": elapsed_ms},
    )


def safe_error(exc: Exception) -> str:
    if isinstance(exc, HTTPError):
        return f"HTTP {exc.code}: {exc.reason}"
    return f"{exc.__class__.__name__}: {exc}"


def validate_health(payload: dict[str, Any]) -> Optional[str]:
    if payload.get("status") != "ok":
        return "Health status is not ok."
    if payload.get("service") != "conversease-api":
        return "Health service name is unexpected."
    return None


def validate_ready(payload: dict[str, Any]) -> Optional[str]:
    if payload.get("status") != "ready":
        return "Readiness status is not ready."
    checks = payload.get("checks", {})
    if checks.get("database") != "ok" or checks.get("migrations") != "ok":
        return "Readiness checks are not all ok."
    return None


def validate_metrics(payload: dict[str, Any]) -> Optional[str]:
    if payload.get("service") != "conversease-api":
        return "Metrics service name is unexpected."
    if "requests" not in payload:
        return "Metrics response has no requests object."
    return None


def courses_requires_auth_check(api_base_url: str) -> SmokeResult:
    """GET /courses is per-user (unlock/access data) and must reject anonymous calls."""
    name = "api_courses_requires_auth"
    url = join_url(api_base_url, "/courses")
    try:
        status, _, elapsed_ms = request_json("GET", url)
    except HTTPError as exc:
        if exc.code == 401:
            return SmokeResult(
                name=name,
                status="pass",
                message="GET /courses correctly requires authentication.",
                details={"url": url, "status_code": exc.code},
            )
        return SmokeResult(
            name=name,
            status="fail",
            message=f"GET /courses returned unexpected status {exc.code}.",
            details={"url": url, "status_code": exc.code},
        )
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return SmokeResult(
            name=name,
            status="fail",
            message="GET /courses failed.",
            details={"url": url, "error": safe_error(exc)},
        )
    return SmokeResult(
        name=name,
        status="fail",
        message=f"GET /courses must require authentication but returned {status}.",
        details={"url": url, "status_code": status, "duration_ms": elapsed_ms},
    )


def validate_lesson(payload: dict[str, Any]) -> Optional[str]:
    lesson = payload.get("data", {})
    if lesson.get("slug") != "saying-hello-and-goodbye":
        return "Expected A1 starter lesson did not load."
    if lesson.get("status") != "published":
        return "Starter lesson is not published."
    return None


def validate_level_test(payload: dict[str, Any]) -> Optional[str]:
    test = payload.get("data", {})
    if test.get("level_code") != "A1":
        return "A1 level test did not load."
    if test.get("status") != "published":
        return "A1 level test is not published."
    sections = test.get("sections", [])
    if len(sections) != 7:
        return f"A1 level test should have 7 sections, got {len(sections)}."
    return None


def validate_plans(payload: dict[str, Any]) -> Optional[str]:
    plans = payload.get("data", [])
    keys = {plan.get("key") for plan in plans}
    if "free" not in keys or "pro_1_month" not in keys:
        return "Expected free and pro_1_month plans are missing."
    return None


def validate_email_templates(payload: dict[str, Any]) -> Optional[str]:
    templates = payload.get("data", [])
    keys = {template.get("template_key") for template in templates}
    expected_keys = {
        "auth_verify_email",
        "minutes_low",
        "payment_manual_approved",
        "payment_manual_rejected",
    }
    missing_keys = expected_keys - keys
    if missing_keys:
        return f"Expected email templates are missing: {sorted(missing_keys)}."
    return None


def validate_rendered_email(payload: dict[str, Any], expected_template_key: str = "minutes_low") -> Optional[str]:
    data = payload.get("data", {})
    if data.get("template_key") != expected_template_key:
        return "Rendered email template key is unexpected."
    if data.get("unresolved_variables"):
        return "Rendered email has unresolved variables."
    return None


def run_smoke(api_base_url: str, web_base_url: str, admin_api_key: str = "") -> list[SmokeResult]:
    results = [
        api_check("api_health", api_base_url, "/health", validate_health),
        api_check("api_ready", api_base_url, "/ready", validate_ready),
        api_check("api_metrics", api_base_url, "/metrics", validate_metrics),
        courses_requires_auth_check(api_base_url),
        api_check("api_starter_lesson", api_base_url, "/lessons/saying-hello-and-goodbye", validate_lesson),
        api_check("api_a1_level_test", api_base_url, "/level-tests/A1", validate_level_test),
        api_check("api_plans", api_base_url, "/plans", validate_plans),
        web_check("web_home", web_base_url, "/", "Conversease"),
        web_security_headers_check(web_base_url),
        web_check("web_login", web_base_url, "/login", "Login"),
        web_check("web_pricing", web_base_url, "/pricing", "Pilih akses belajar"),
    ]

    if admin_api_key:
        results.extend(
            [
                admin_get_check(
                    "admin_email_templates",
                    api_base_url,
                    "/admin/email-templates",
                    admin_api_key,
                    validate_email_templates,
                ),
                admin_post_check(
                    "admin_render_test_email",
                    api_base_url,
                    "/admin/test-email/render",
                    {"template_key": "minutes_low"},
                    admin_api_key,
                    validate_rendered_email,
                ),
                admin_post_check(
                    "admin_render_payment_approved_email",
                    api_base_url,
                    "/admin/test-email/render",
                    {"template_key": "payment_manual_approved"},
                    admin_api_key,
                    lambda payload: validate_rendered_email(payload, "payment_manual_approved"),
                ),
                admin_post_check(
                    "admin_render_payment_rejected_email",
                    api_base_url,
                    "/admin/test-email/render",
                    {"template_key": "payment_manual_rejected"},
                    admin_api_key,
                    lambda payload: validate_rendered_email(payload, "payment_manual_rejected"),
                ),
            ]
        )

    return results


def build_report(results: Sequence[SmokeResult]) -> dict[str, Any]:
    counts = {"pass": 0, "fail": 0}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "fail" if counts["fail"] else "pass",
        "summary": counts,
        "checks": [asdict(result) for result in results],
    }


def print_text_report(report: dict[str, Any]) -> None:
    print(f"Release smoke: {report['status'].upper()}")
    for result in report["checks"]:
        print(f"- {result['status'].upper():<4} {result['name']}: {result['message']}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run Conversease post-deploy HTTP smoke checks.")
    parser.add_argument(
        "--api-base-url",
        default=os.getenv("NEXT_PUBLIC_API_BASE_URL") or os.getenv("API_BASE_URL") or "http://127.0.0.1:8000",
        help="API base URL. Accepts either https://api.example.com or https://api.example.com/api.",
    )
    parser.add_argument(
        "--web-base-url",
        default=os.getenv("PUBLIC_APP_URL") or "http://localhost:3000",
        help="Web app base URL.",
    )
    parser.add_argument(
        "--admin-api-key",
        default=os.getenv("PAYMENT_ADMIN_API_KEY", ""),
        help="Optional admin API key for admin diagnostics smoke checks.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format. Defaults to json for deploy automation.",
    )
    args = parser.parse_args(argv)

    api_base_url = normalize_api_base_url(args.api_base_url)
    web_base_url = normalize_web_base_url(args.web_base_url)
    report = build_report(run_smoke(api_base_url, web_base_url, args.admin_api_key))

    if args.format == "text":
        print_text_report(report)
    else:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
