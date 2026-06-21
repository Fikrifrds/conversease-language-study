from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"


@dataclass
class CheckResult:
    name: str
    status: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


def ensure_api_import_path(root: Path = REPO_ROOT) -> None:
    api_path = str(root / "apps" / "api")
    if api_path not in sys.path:
        sys.path.insert(0, api_path)


def safe_exception_message(exc: Exception) -> str:
    errors = getattr(exc, "errors", None)
    if callable(errors):
        try:
            messages = [
                str(error.get("msg", exc.__class__.__name__))
                for error in errors(include_url=False, include_input=False)
            ]
        except TypeError:
            messages = []
        if messages:
            return "; ".join(messages)

    first_line = str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__
    return f"{exc.__class__.__name__}: {first_line}"


def redact_database_url(database_url: str) -> dict[str, Any]:
    try:
        from sqlalchemy.engine import make_url

        url = make_url(database_url)
        return {
            "drivername": url.drivername,
            "host": url.host,
            "port": url.port,
            "database": url.database,
        }
    except Exception:
        scheme = database_url.split(":", 1)[0] if ":" in database_url else "unknown"
        return {"drivername": scheme, "host": None, "port": None, "database": None}


def check_runtime_config(root: Path = REPO_ROOT) -> tuple[CheckResult, Optional[Any]]:
    ensure_api_import_path(root)
    try:
        from app.core.config import settings
    except Exception as exc:
        return (
            CheckResult(
                name="runtime_config",
                status="fail",
                message="Runtime configuration could not be loaded.",
                details={"error": safe_exception_message(exc)},
            ),
            None,
        )

    return (
        CheckResult(
            name="runtime_config",
            status="pass",
            message="Runtime configuration loaded successfully.",
            details={
                "app_env": settings.app_env,
                "release_version": settings.release_version,
                "public_app_url": settings.public_app_url,
                "api_base_url": settings.api_base_url,
                "cors_origins_count": len(settings.cors_origins),
                "database": redact_database_url(settings.database_url),
            },
        ),
        settings,
    )


def check_manual_transfer_readiness(settings: Optional[Any]) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="manual_transfer_readiness",
            status="skip",
            message="Skipped because runtime configuration did not load.",
        )

    missing = []
    for field_name in (
        "payment_admin_email",
        "payment_admin_api_key",
        "manual_transfer_bank_name",
        "manual_transfer_account_number",
        "manual_transfer_account_holder",
        "resend_api_key",
    ):
        if not getattr(settings, field_name):
            missing.append(field_name.upper())

    if missing:
        status = "fail" if settings.is_production else "warn"
        return CheckResult(
            name="manual_transfer_readiness",
            status=status,
            message="Manual transfer beta payment flow is missing required configuration.",
            details={"missing": missing},
        )

    return CheckResult(
        name="manual_transfer_readiness",
        status="pass",
        message="Manual transfer, admin approval, and email notification settings are present.",
        details={
            "bank_name": settings.manual_transfer_bank_name,
            "admin_email": settings.payment_admin_email,
            "unique_code_min": settings.manual_transfer_unique_code_min,
            "unique_code_max": settings.manual_transfer_unique_code_max,
        },
    )


def expected_next_public_api_base_url(settings: Any) -> str:
    return f"{settings.api_base_url.rstrip('/')}/api"


def dotenv_paths(root: Path = REPO_ROOT) -> list[Path]:
    return [root / ".env.local", root / ".env"]


def dotenv_value(key: str, root: Path = REPO_ROOT) -> str:
    for env_path in dotenv_paths(root):
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            name, value = line.split("=", 1)
            if name.strip() != key:
                continue

            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            return value

    return ""


def env_or_dotenv_value(key: str, root: Path = REPO_ROOT) -> str:
    return os.getenv(key, "").strip() or dotenv_value(key, root).strip()


def check_web_runtime_config(settings: Optional[Any], root: Path = REPO_ROOT) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="web_runtime_config",
            status="skip",
            message="Skipped because runtime configuration did not load.",
        )

    configured_url = env_or_dotenv_value("NEXT_PUBLIC_API_BASE_URL", root).rstrip("/")
    expected_url = expected_next_public_api_base_url(settings)
    details = {
        "next_public_api_base_url_configured": bool(configured_url),
        "expected_next_public_api_base_url": expected_url,
    }

    if not configured_url:
        return CheckResult(
            name="web_runtime_config",
            status="fail" if settings.is_production else "warn",
            message=(
                "NEXT_PUBLIC_API_BASE_URL must be set for production web builds."
                if settings.is_production
                else "NEXT_PUBLIC_API_BASE_URL is not set; the web app will use the local dev fallback."
            ),
            details=details,
        )

    issues = []
    parsed = urlparse(configured_url)
    if not parsed.scheme or not parsed.netloc:
        issues.append("NEXT_PUBLIC_API_BASE_URL must be an absolute URL")

    if not configured_url.endswith("/api"):
        issues.append("NEXT_PUBLIC_API_BASE_URL must include the /api path")

    if settings.is_production and parsed.scheme != "https":
        issues.append("NEXT_PUBLIC_API_BASE_URL must use https in production")

    if settings.is_production and parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        issues.append("NEXT_PUBLIC_API_BASE_URL must not point to localhost in production")

    if settings.is_production and configured_url != expected_url:
        issues.append("NEXT_PUBLIC_API_BASE_URL must match API_BASE_URL plus /api")

    if issues:
        return CheckResult(
            name="web_runtime_config",
            status="fail" if settings.is_production else "warn",
            message="Web runtime API base URL is not release-ready.",
            details={**details, "configured_next_public_api_base_url": configured_url, "issues": issues},
        )

    return CheckResult(
        name="web_runtime_config",
        status="pass",
        message="Web runtime API base URL is configured correctly.",
        details={**details, "configured_next_public_api_base_url": configured_url},
    )


def check_optional_automation_integrations(settings: Optional[Any]) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="optional_automation_integrations",
            status="skip",
            message="Skipped because runtime configuration did not load.",
        )

    missing_groups = []
    if not settings.midtrans_server_key or not settings.midtrans_client_key:
        missing_groups.append("midtrans_checkout_webhook")
    if not settings.together_api_key or not settings.assemblyai_api_key or not settings.minimax_api_key:
        missing_groups.append("ai_stt_tts_automation")

    if missing_groups:
        return CheckResult(
            name="optional_automation_integrations",
            status="warn",
            message=(
                "Controlled beta can run without these integrations, but public automated "
                "checkout and official automated speaking assessment still need them."
            ),
            details={"missing_groups": missing_groups},
        )

    return CheckResult(
        name="optional_automation_integrations",
        status="pass",
        message="Midtrans and AI/STT/TTS integration credentials are configured.",
    )


def check_database_connectivity(settings: Optional[Any]) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="database_connectivity",
            status="skip",
            message="Skipped because runtime configuration did not load.",
        )

    try:
        from sqlalchemy import create_engine, text

        from app.db.session import engine_options

        engine = create_engine(settings.database_url, **engine_options(settings.database_url))
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        finally:
            engine.dispose()
    except Exception as exc:
        return CheckResult(
            name="database_connectivity",
            status="fail",
            message="Database connectivity check failed.",
            details={
                "error_type": exc.__class__.__name__,
                "database": redact_database_url(settings.database_url),
            },
        )

    return CheckResult(
        name="database_connectivity",
        status="pass",
        message="Database responded to SELECT 1.",
        details={"database": redact_database_url(settings.database_url)},
    )


def check_migration_head(settings: Optional[Any], root: Path = REPO_ROOT) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="migration_head",
            status="skip",
            message="Skipped because runtime configuration did not load.",
        )

    ensure_api_import_path(root)
    try:
        from alembic.config import Config
        from alembic.runtime.migration import MigrationContext
        from alembic.script import ScriptDirectory
        from sqlalchemy import create_engine

        from app.db.session import engine_options

        alembic_config = Config(str(root / "apps" / "api" / "alembic.ini"))
        alembic_config.set_main_option("sqlalchemy.url", settings.database_url)
        script = ScriptDirectory.from_config(alembic_config)
        expected_heads = set(script.get_heads())

        engine = create_engine(settings.database_url, **engine_options(settings.database_url))
        try:
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                applied_heads = set(context.get_current_heads())
        finally:
            engine.dispose()
    except Exception as exc:
        return CheckResult(
            name="migration_head",
            status="fail",
            message="Migration head check failed.",
            details={"error_type": exc.__class__.__name__},
        )

    pending_heads = sorted(expected_heads - applied_heads)
    unexpected_heads = sorted(applied_heads - expected_heads)
    ok = applied_heads == expected_heads and bool(expected_heads)
    return CheckResult(
        name="migration_head",
        status="pass" if ok else "fail",
        message=(
            "Database is at the latest Alembic migration head."
            if ok
            else "Database migration head does not match migration files."
        ),
        details={
            "applied_heads": sorted(applied_heads),
            "expected_heads": sorted(expected_heads),
            "pending_heads": pending_heads,
            "unexpected_heads": unexpected_heads,
        },
    )


def check_curriculum(root: Path = REPO_ROOT) -> CheckResult:
    ensure_api_import_path(root)
    try:
        from app.data.curriculum import validate_curriculum_content

        issues = validate_curriculum_content()
    except Exception as exc:
        return CheckResult(
            name="curriculum_content",
            status="fail",
            message="Curriculum validation could not run.",
            details={"error": safe_exception_message(exc)},
        )

    if issues:
        return CheckResult(
            name="curriculum_content",
            status="fail",
            message="Curriculum validation found release-blocking issues.",
            details={"issue_count": len(issues), "issues": issues[:20]},
        )

    return CheckResult(
        name="curriculum_content",
        status="pass",
        message="Authored curriculum structure and English final evaluation content are valid.",
    )


def check_content_release_readiness(root: Path = REPO_ROOT) -> CheckResult:
    ensure_api_import_path(root)
    try:
        from app.data.content_readiness import all_content_readiness_summary

        readiness = all_content_readiness_summary()
    except Exception as exc:
        return CheckResult(
            name="content_release_readiness",
            status="fail",
            message="Content release readiness could not run.",
            details={"error": safe_exception_message(exc)},
        )

    summary = readiness.get("summary", {})
    levels = []
    for level in readiness.get("levels", []):
        course = level.get("course", {})
        level_summary = level.get("summary", {})
        levels.append(
            {
                "language": course.get("language", ""),
                "level_code": course.get("level_code", ""),
                "planned_lesson_count": level_summary.get("planned_lesson_count", 0),
                "text_ready_count": level_summary.get("text_ready_count", 0),
                "audio_ready_count": level_summary.get("audio_ready_count", 0),
                "production_ready_count": level_summary.get("production_ready_count", 0),
                "missing_content_count": level_summary.get("missing_content_count", 0),
                "missing_audio_count": level_summary.get("missing_audio_count", 0),
            }
        )

    missing_content = int(summary.get("missing_content_count", 0) or 0)
    missing_audio = int(summary.get("missing_audio_count", 0) or 0)
    planned_lessons = int(summary.get("planned_lesson_count", 0) or 0)
    production_ready = int(summary.get("production_ready_count", 0) or 0)

    details = {
        "summary": summary,
        "levels": levels,
    }
    if missing_content or missing_audio or production_ready != planned_lessons:
        return CheckResult(
            name="content_release_readiness",
            status="fail",
            message="Full release requires every planned lesson to be text-ready, audio-ready, and production-ready.",
            details=details,
        )

    return CheckResult(
        name="content_release_readiness",
        status="pass",
        message="Every planned lesson is text-ready, audio-ready, and production-ready.",
        details=details,
    )


def content_audio_requirements(readiness: dict[str, Any]) -> dict[str, Any]:
    missing_levels: list[dict[str, Any]] = []
    languages: set[str] = set()

    for level in readiness.get("levels", []):
        course = level.get("course", {})
        summary = level.get("summary", {})
        missing_audio = int(summary.get("missing_audio_count", 0) or 0)
        if missing_audio <= 0:
            continue

        language = str(course.get("language") or "").strip().lower()
        if language:
            languages.add(language)
        missing_levels.append(
            {
                "language": language,
                "level_code": course.get("level_code", ""),
                "missing_audio_count": missing_audio,
                "planned_lesson_count": summary.get("planned_lesson_count", 0),
                "audio_ready_count": summary.get("audio_ready_count", 0),
            }
        )

    summary = readiness.get("summary", {})
    missing_audio_count = int(
        summary.get("missing_audio_count", sum(level["missing_audio_count"] for level in missing_levels)) or 0
    )
    return {
        "missing_audio_count": missing_audio_count,
        "languages": sorted(languages),
        "levels": missing_levels,
    }


def missing_audio_generation_fields(settings: Any, requirements: dict[str, Any]) -> list[str]:
    if int(requirements.get("missing_audio_count", 0) or 0) <= 0:
        return []

    missing_fields: list[str] = []
    for field_name in ("s3_bucket", "aws_access_key_id", "aws_secret_access_key", "aws_region"):
        if not getattr(settings, field_name, ""):
            missing_fields.append(field_name)

    languages = set(requirements.get("languages", []))
    if "english" in languages and not getattr(settings, "minimax_api_key", ""):
        missing_fields.append("minimax_api_key")
    if "arabic" in languages and not getattr(settings, "elevenlabs_api_key", ""):
        missing_fields.append("elevenlabs_api_key")

    unknown_languages = sorted(language for language in languages if language not in {"english", "arabic"})
    missing_fields.extend(f"tts_provider_for_{language}" for language in unknown_languages)
    return missing_fields


def check_audio_generation_config(settings: Optional[Any], root: Path = REPO_ROOT) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="audio_generation_config",
            status="skip",
            message="Audio generation configuration could not be checked because runtime configuration failed.",
        )

    ensure_api_import_path(root)
    try:
        from app.data.content_readiness import all_content_readiness_summary

        readiness = all_content_readiness_summary()
    except Exception as exc:
        return CheckResult(
            name="audio_generation_config",
            status="fail",
            message="Audio generation configuration could not be checked.",
            details={"error": safe_exception_message(exc)},
        )

    requirements = content_audio_requirements(readiness)
    missing_fields = missing_audio_generation_fields(settings, requirements)
    storage_fields = ("s3_bucket", "aws_access_key_id", "aws_secret_access_key", "aws_region")
    storage_missing = [field_name for field_name in storage_fields if not getattr(settings, field_name, "")]
    details = {
        "missing_audio_count": requirements["missing_audio_count"],
        "missing_audio_levels": requirements["levels"],
        "required_languages": requirements["languages"],
        "storage_configured": not storage_missing,
        "missing_fields": missing_fields,
    }

    if requirements["missing_audio_count"] <= 0:
        return CheckResult(
            name="audio_generation_config",
            status="pass",
            message="No lesson audio generation is required for the current content release.",
            details=details,
        )

    if missing_fields:
        return CheckResult(
            name="audio_generation_config",
            status="fail",
            message="Missing lesson audio cannot be regenerated with the current TTS/storage configuration.",
            details=details,
        )

    return CheckResult(
        name="audio_generation_config",
        status="pass",
        message="TTS providers and S3 storage are configured for the remaining lesson audio generation.",
        details=details,
    )


def default_email_template_variables(settings: Any) -> dict[str, str]:
    public_app_url = settings.public_app_url.rstrip("/")
    return {
        "name": "QA Admin",
        "cta_url": f"{public_app_url}/dashboard",
        "verify_url": f"{public_app_url}/verify-email?token=test-token",
        "dashboard_url": f"{public_app_url}/dashboard",
        "billing_url": f"{public_app_url}/billing",
        "remaining_minutes": "25",
        "package_name": "Pro 1 Month",
        "amount": "Rp49.492",
        "order_id": "order-test123",
        "admin_notes": "Nominal transfer sudah cocok.",
        "completed_level": "A1",
        "completed_level_title": "Start Simple Conversations",
        "next_level_message": "Level A2 sekarang terbuka.",
        "courses_url": f"{public_app_url}/courses",
    }


def check_email_templates(settings: Optional[Any], root: Path = REPO_ROOT) -> CheckResult:
    if settings is None:
        return CheckResult(
            name="email_templates",
            status="skip",
            message="Skipped because runtime configuration did not load.",
        )

    ensure_api_import_path(root)
    try:
        from app.data.seed import EMAIL_TEMPLATES
        from app.domain.email import render_template, unresolved_template_variables
    except Exception as exc:
        return CheckResult(
            name="email_templates",
            status="fail",
            message="Email template validation could not run.",
            details={"error": safe_exception_message(exc)},
        )

    variables = default_email_template_variables(settings)
    issues = []
    for template in EMAIL_TEMPLATES:
        rendered_parts = {
            "subject": render_template(template.subject, variables),
            "preheader": render_template(template.preheader, variables),
            "html_body": render_template(template.html_body, variables),
            "text_body": render_template(template.text_body, variables),
            "cta_url": render_template(template.cta_url, variables),
        }
        unresolved = sorted(
            set(
                variable
                for value in rendered_parts.values()
                for variable in unresolved_template_variables(value)
            )
        )
        empty_parts = [name for name, value in rendered_parts.items() if not value.strip()]
        if unresolved or empty_parts:
            issues.append(
                {
                    "template_key": template.template_key,
                    "unresolved_variables": unresolved,
                    "empty_parts": empty_parts,
                }
            )

    if issues:
        return CheckResult(
            name="email_templates",
            status="fail",
            message="Email templates have unresolved variables or empty required fields.",
            details={"issues": issues},
        )

    return CheckResult(
        name="email_templates",
        status="pass",
        message="Email templates render with the release preflight sample variables.",
        details={"template_count": len(EMAIL_TEMPLATES)},
    )


def check_backup_tooling(root: Path = REPO_ROOT, production: bool = False) -> CheckResult:
    backup_script = root / "scripts" / "backup_postgres.sh"
    verify_script = root / "scripts" / "verify_postgres_backup.sh"
    missing_files = [str(path.relative_to(root)) for path in (backup_script, verify_script) if not path.exists()]

    bash_path = shutil.which("bash")
    missing_tools = [tool for tool in ("pg_dump", "pg_restore") if shutil.which(tool) is None]

    if missing_files:
        return CheckResult(
            name="backup_tooling",
            status="fail",
            message="Backup scripts are missing.",
            details={"missing_files": missing_files},
        )

    if bash_path is None:
        return CheckResult(
            name="backup_tooling",
            status="fail",
            message="bash is required to validate backup scripts.",
        )

    syntax_check = subprocess.run(
        [bash_path, "-n", str(backup_script), str(verify_script)],
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )
    if syntax_check.returncode != 0:
        return CheckResult(
            name="backup_tooling",
            status="fail",
            message="Backup script shell syntax check failed.",
            details={"stderr": syntax_check.stderr.strip()},
        )

    if missing_tools:
        return CheckResult(
            name="backup_tooling",
            status="fail" if production else "warn",
            message="PostgreSQL backup/restore CLI tools are not fully available.",
            details={"missing_tools": missing_tools},
        )

    return CheckResult(
        name="backup_tooling",
        status="pass",
        message="Backup scripts and PostgreSQL backup/restore CLI tools are available.",
    )


def run_preflight(root: Path = REPO_ROOT) -> list[CheckResult]:
    config_result, settings = check_runtime_config(root)
    production = bool(settings and settings.is_production)
    return [
        config_result,
        check_web_runtime_config(settings),
        check_manual_transfer_readiness(settings),
        check_database_connectivity(settings),
        check_migration_head(settings, root),
        check_curriculum(root),
        check_content_release_readiness(root),
        check_audio_generation_config(settings, root),
        check_email_templates(settings, root),
        check_backup_tooling(root, production=production),
        check_optional_automation_integrations(settings),
    ]


def summarize(results: Sequence[CheckResult], strict_warnings: bool = False) -> dict[str, Any]:
    counts = {"pass": 0, "warn": 0, "fail": 0, "skip": 0}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1

    failure_count = counts["fail"] + (counts["warn"] if strict_warnings else 0)
    return {
        "status": "fail" if failure_count else "pass",
        "strict_warnings": strict_warnings,
        "counts": counts,
    }


def build_report(results: Sequence[CheckResult], strict_warnings: bool = False) -> dict[str, Any]:
    summary = summarize(results, strict_warnings=strict_warnings)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": summary["status"],
        "summary": summary,
        "checks": [asdict(result) for result in results],
    }


def print_text_report(report: dict[str, Any]) -> None:
    print(f"Release preflight: {report['status'].upper()}")
    for result in report["checks"]:
        print(f"- {result['status'].upper():<4} {result['name']}: {result['message']}")
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run Conversease production release preflight checks.")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Return a non-zero exit code when warning checks are present.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format. Defaults to json for CI/deploy automation.",
    )
    args = parser.parse_args(argv)

    results = run_preflight(REPO_ROOT)
    report = build_report(results, strict_warnings=args.strict_warnings)

    if args.format == "text":
        print_text_report(report)
    else:
        print(json.dumps(report, indent=2, sort_keys=True))

    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
