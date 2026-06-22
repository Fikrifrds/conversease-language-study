import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
SMOKE_PATH = REPO_ROOT / "scripts" / "release_smoke.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("release_smoke", SMOKE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReleaseSmokeTest(unittest.TestCase):
    def setUp(self):
        self.smoke = load_smoke_module()

    def test_normalize_api_base_url_accepts_plain_or_api_base(self):
        self.assertEqual(
            self.smoke.normalize_api_base_url("https://api.conversease.com"),
            "https://api.conversease.com/api",
        )
        self.assertEqual(
            self.smoke.normalize_api_base_url("https://api.conversease.com/api"),
            "https://api.conversease.com/api",
        )

    def test_build_report_fails_when_any_check_fails(self):
        report = self.smoke.build_report(
            [
                self.smoke.SmokeResult("health", "pass", "ok"),
                self.smoke.SmokeResult("ready", "fail", "not ready"),
            ]
        )

        self.assertEqual(report["status"], "fail")
        self.assertEqual(report["summary"], {"pass": 1, "fail": 1})

    def test_level_test_validator_requires_seven_sections(self):
        payload = {
            "data": {
                "language": "english",
                "level_code": "A1",
                "attempt_level_code": "A1",
                "status": "published",
                "sections": [{"key": str(index)} for index in range(7)],
            }
        }

        self.assertIsNone(self.smoke.validate_level_test(payload))

    def test_rendered_email_validator_rejects_unresolved_variables(self):
        payload = {
            "data": {
                "template_key": "minutes_low",
                "unresolved_variables": ["remaining_minutes"],
            }
        }

        self.assertEqual(
            self.smoke.validate_rendered_email(payload),
            "Rendered email has unresolved variables.",
        )

    def test_email_template_validator_requires_manual_payment_templates(self):
        payload = {
            "data": [
                {"template_key": "auth_verify_email"},
                {"template_key": "minutes_low"},
            ]
        }

        issue = self.smoke.validate_email_templates(payload)

        self.assertIsNotNone(issue)
        self.assertIn("payment_manual_approved", issue)
        self.assertIn("payment_manual_rejected", issue)

    def test_web_security_headers_check_passes_with_required_headers(self):
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(self), geolocation=()",
        }

        with patch.object(
            self.smoke,
            "request_text_with_headers",
            return_value=(200, "<html>Conversease</html>", headers, 12),
        ):
            result = self.smoke.web_security_headers_check("https://app.conversease.com")

        self.assertEqual(result.status, "pass")

    def test_web_security_headers_check_fails_when_header_is_missing(self):
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
        }

        with patch.object(
            self.smoke,
            "request_text_with_headers",
            return_value=(200, "<html>Conversease</html>", headers, 12),
        ):
            result = self.smoke.web_security_headers_check("https://app.conversease.com")

        self.assertEqual(result.status, "fail")
        self.assertIn("referrer-policy", result.details["headers"])


if __name__ == "__main__":
    unittest.main()
