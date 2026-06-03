import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
PREFLIGHT_PATH = REPO_ROOT / "scripts" / "release_preflight.py"


def load_preflight_module():
    spec = importlib.util.spec_from_file_location("release_preflight", PREFLIGHT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReleasePreflightTest(unittest.TestCase):
    def setUp(self):
        self.preflight = load_preflight_module()

    def test_redacts_database_credentials(self):
        details = self.preflight.redact_database_url(
            "postgresql+psycopg://user:secret-password@db.example.com:5432/conversease"
        )

        self.assertEqual(details["drivername"], "postgresql+psycopg")
        self.assertEqual(details["host"], "db.example.com")
        self.assertEqual(details["port"], 5432)
        self.assertEqual(details["database"], "conversease")
        self.assertNotIn("secret-password", str(details))

    def test_summary_can_treat_warnings_as_failures(self):
        results = [
            self.preflight.CheckResult("config", "pass", "ok"),
            self.preflight.CheckResult("optional", "warn", "missing optional provider"),
        ]

        relaxed = self.preflight.summarize(results, strict_warnings=False)
        strict = self.preflight.summarize(results, strict_warnings=True)

        self.assertEqual(relaxed["status"], "pass")
        self.assertEqual(strict["status"], "fail")

    def test_web_runtime_config_warns_when_missing_in_development(self):
        settings = SimpleNamespace(
            api_base_url="http://localhost:8000",
            is_production=False,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.dict(self.preflight.os.environ, {}, clear=True):
                result = self.preflight.check_web_runtime_config(settings, Path(tmp_dir))

        self.assertEqual(result.status, "warn")
        self.assertEqual(
            result.details["expected_next_public_api_base_url"],
            "http://localhost:8000/api",
        )

    def test_web_runtime_config_reads_next_public_api_base_url_from_dotenv(self):
        settings = SimpleNamespace(
            api_base_url="http://localhost:8000",
            is_production=False,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / ".env").write_text(
                "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api\n",
                encoding="utf-8",
            )
            with patch.dict(self.preflight.os.environ, {}, clear=True):
                result = self.preflight.check_web_runtime_config(settings, root)

        self.assertEqual(result.status, "pass")
        self.assertEqual(
            result.details["configured_next_public_api_base_url"],
            "http://localhost:8000/api",
        )

    def test_web_runtime_config_fails_when_missing_in_production(self):
        settings = SimpleNamespace(
            api_base_url="https://api.conversease.com",
            is_production=True,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.dict(self.preflight.os.environ, {}, clear=True):
                result = self.preflight.check_web_runtime_config(settings, Path(tmp_dir))

        self.assertEqual(result.status, "fail")

    def test_web_runtime_config_requires_matching_production_api_url(self):
        settings = SimpleNamespace(
            api_base_url="https://api.conversease.com",
            is_production=True,
        )

        with patch.dict(
            self.preflight.os.environ,
            {"NEXT_PUBLIC_API_BASE_URL": "https://wrong.conversease.com/api"},
            clear=True,
        ):
            result = self.preflight.check_web_runtime_config(settings)

        self.assertEqual(result.status, "fail")
        self.assertIn(
            "NEXT_PUBLIC_API_BASE_URL must match API_BASE_URL plus /api",
            result.details["issues"],
        )

    def test_web_runtime_config_accepts_matching_production_api_url(self):
        settings = SimpleNamespace(
            api_base_url="https://api.conversease.com",
            is_production=True,
        )

        with patch.dict(
            self.preflight.os.environ,
            {"NEXT_PUBLIC_API_BASE_URL": "https://api.conversease.com/api"},
            clear=True,
        ):
            result = self.preflight.check_web_runtime_config(settings)

        self.assertEqual(result.status, "pass")

    def test_email_template_preflight_passes_with_sample_variables(self):
        settings = SimpleNamespace(public_app_url="https://app.conversease.com")

        result = self.preflight.check_email_templates(settings, REPO_ROOT)

        self.assertEqual(result.status, "pass")
        self.assertGreaterEqual(result.details["template_count"], 1)

    def test_backup_tooling_warns_in_development_when_postgres_tools_missing(self):
        bash_path = shutil.which("bash")
        if bash_path is None:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            scripts_dir = root / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "backup_postgres.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n")
            (scripts_dir / "verify_postgres_backup.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n")

            def fake_which(tool_name):
                if tool_name == "bash":
                    return bash_path
                return None

            with patch.object(self.preflight.shutil, "which", side_effect=fake_which):
                result = self.preflight.check_backup_tooling(root, production=False)

        self.assertEqual(result.status, "warn")
        self.assertEqual(result.details["missing_tools"], ["pg_dump", "pg_restore"])

    def test_backup_tooling_fails_in_production_when_postgres_tools_missing(self):
        bash_path = shutil.which("bash")
        if bash_path is None:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            scripts_dir = root / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "backup_postgres.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n")
            (scripts_dir / "verify_postgres_backup.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n")

            def fake_which(tool_name):
                if tool_name == "bash":
                    return bash_path
                return None

            with patch.object(self.preflight.shutil, "which", side_effect=fake_which):
                result = self.preflight.check_backup_tooling(root, production=True)

        self.assertEqual(result.status, "fail")


if __name__ == "__main__":
    unittest.main()
