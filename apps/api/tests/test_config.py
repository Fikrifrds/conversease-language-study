import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pydantic import ValidationError

from app.core.config import Settings


class ConfigTest(unittest.TestCase):
    def test_development_allows_sqlite_default_without_env_file(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings(_env_file=None)

        self.assertEqual(settings.app_env, "development")
        self.assertTrue(settings.database_url.startswith("sqlite"))

    def test_development_env_file_can_use_local_postgres(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env"
            env_path.write_text(
                "APP_ENV=development\n"
                "DATABASE_URL=postgresql+psycopg://conversease:conversease@localhost:5432/conversease_db\n",
                encoding="utf-8",
            )

            with patch.dict(os.environ, {}, clear=True):
                settings = Settings(_env_file=env_path)

        self.assertEqual(settings.app_env, "development")
        self.assertEqual(
            settings.database_url,
            "postgresql+psycopg://conversease:conversease@localhost:5432/conversease_db",
        )

    def test_production_rejects_sqlite_and_weak_secret(self):
        with self.assertRaises(ValidationError):
            Settings(
                app_env="production",
                public_app_url="http://localhost:3000",
                api_base_url="http://localhost:8000",
                database_url="sqlite:///tmp.db",
                jwt_secret="dev-secret",
                cors_origins_raw="http://localhost:3000",
            )

    def test_production_rejects_example_placeholder_secrets(self):
        with self.assertRaises(ValidationError) as context:
            Settings(
                app_env="production",
                public_app_url="https://app.conversease.com",
                api_base_url="https://api.conversease.com",
                database_url="postgresql+psycopg://user:pass@db:5432/conversease",
                release_version="2026.06.03",
                jwt_secret="replace-with-at-least-32-random-characters",
                cors_origins_raw="https://app.conversease.com",
                google_oauth_client_id="<google-oauth-client-id>",
                google_oauth_client_secret="<google-oauth-client-secret>",
                payment_admin_api_key="replace-with-at-least-24-random-characters",
                resend_api_key="<resend-api-key>",
            )

        message = str(context.exception)
        self.assertIn("JWT_SECRET must not use a placeholder value", message)
        self.assertIn("PAYMENT_ADMIN_API_KEY must not use a placeholder value", message)
        self.assertIn("RESEND_API_KEY must not use a placeholder value", message)
        self.assertIn("Google OAuth credentials must not use placeholder values", message)

    def test_production_accepts_postgres_https_and_strong_secret(self):
        settings = Settings(
            app_env="production",
            public_app_url="https://app.conversease.com",
            api_base_url="https://api.conversease.com",
            database_url="postgresql+psycopg://user:pass@db:5432/conversease",
            release_version="2026.06.03",
            jwt_secret="x" * 40,
            cors_origins_raw="https://app.conversease.com",
            google_oauth_client_id="1234567890-abcdef.apps.googleusercontent.com",
            google_oauth_client_secret="GOCSPX-production-oauth-secret",
            payment_admin_api_key="payment-admin-key-with-32-chars",
            resend_api_key="re_test_123",
        )

        self.assertTrue(settings.is_production)
        self.assertEqual(settings.cors_origins, ["https://app.conversease.com"])

    def test_production_rejects_invalid_rate_limit_config(self):
        with self.assertRaises(ValidationError) as context:
            Settings(
                app_env="production",
                public_app_url="https://app.conversease.com",
                api_base_url="https://api.conversease.com",
                database_url="postgresql+psycopg://user:pass@db:5432/conversease",
                release_version="2026.06.03",
                jwt_secret="x" * 40,
                cors_origins_raw="https://app.conversease.com",
                google_oauth_client_id="1234567890-abcdef.apps.googleusercontent.com",
                google_oauth_client_secret="GOCSPX-production-oauth-secret",
                payment_admin_api_key="payment-admin-key-with-32-chars",
                resend_api_key="re_test_123",
                rate_limit_window_seconds=0,
            )

        self.assertIn("RATE_LIMIT_WINDOW_SECONDS must be positive", str(context.exception))

    def test_production_rejects_invalid_manual_transfer_expiry(self):
        with self.assertRaises(ValidationError) as context:
            Settings(
                app_env="production",
                public_app_url="https://app.conversease.com",
                api_base_url="https://api.conversease.com",
                database_url="postgresql+psycopg://user:pass@db:5432/conversease",
                release_version="2026.06.03",
                jwt_secret="x" * 40,
                cors_origins_raw="https://app.conversease.com",
                google_oauth_client_id="1234567890-abcdef.apps.googleusercontent.com",
                google_oauth_client_secret="GOCSPX-production-oauth-secret",
                payment_admin_api_key="payment-admin-key-with-32-chars",
                resend_api_key="re_test_123",
                manual_transfer_expire_hours=0,
            )

        self.assertIn("MANUAL_TRANSFER_EXPIRE_HOURS must be positive", str(context.exception))


if __name__ == "__main__":
    unittest.main()
