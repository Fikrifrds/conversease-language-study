import unittest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.config import settings
from app.domain.email import EmailCategory, EmailTemplate, unresolved_template_variables
from app.domain.users import User
from app.main import create_app
from app.services.auth_email import AuthEmailService
from app.services.email_delivery import EmailDeliveryResult


class EmailRoutesTest(unittest.TestCase):
    def setUp(self):
        self.original_admin_key = settings.payment_admin_api_key
        self.original_admin_email = settings.payment_admin_email
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
        settings.payment_admin_email = "denahku.team@gmail.com"
        self.client = TestClient(create_app())

    def tearDown(self):
        settings.payment_admin_api_key = self.original_admin_key
        settings.payment_admin_email = self.original_admin_email

    def admin_headers(self) -> dict[str, str]:
        return {"x-admin-api-key": settings.payment_admin_api_key}

    def test_unresolved_template_variables_are_detected(self):
        unresolved = unresolved_template_variables("Hi {{ name }}, open {{cta_url}}.")

        self.assertEqual(unresolved, ["cta_url", "name"])

    def test_render_test_email_uses_default_variables(self):
        response = self.client.post(
            "/api/admin/test-email/render",
            headers=self.admin_headers(),
            json={"template_key": "auth_verify_email"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["template_key"], "auth_verify_email")
        self.assertEqual(data["unresolved_variables"], [])
        self.assertIn("QA Admin", data["html_body"])
        self.assertIn("https://conversease.com/logo.svg", data["html_body"])
        self.assertIn("Verifikasi email Conversease kamu", data["html_body"])
        self.assertIn("verify-email?token=test-token", data["cta_url"])

    def test_render_test_email_returns_404_for_unknown_template(self):
        response = self.client.post(
            "/api/admin/test-email/render",
            headers=self.admin_headers(),
            json={"template_key": "missing-template"},
        )

        self.assertEqual(response.status_code, 404)

    def test_send_test_email_uses_admin_email_by_default(self):
        delivery = AsyncMock(
            return_value=EmailDeliveryResult(
                sent=True,
                provider="resend",
                provider_id="email-test-123",
            )
        )

        with patch("app.api.routes.email.EmailDeliveryService") as delivery_service:
            delivery_service.return_value.send_email = delivery
            response = self.client.post(
                "/api/admin/test-email/send",
                headers=self.admin_headers(),
                json={"template_key": "minutes_low"},
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["recipient_email"], "denahku.team@gmail.com")
        self.assertTrue(data["delivery"]["sent"])
        delivery.assert_awaited_once()
        call_kwargs = delivery.await_args.kwargs
        self.assertEqual(call_kwargs["recipient_email"], "denahku.team@gmail.com")
        self.assertTrue(call_kwargs["idempotency_key"].startswith("admin-test-email:"))

    def test_send_test_email_rejects_unresolved_template(self):
        broken_template = EmailTemplate(
            template_key="broken_template",
            category=EmailCategory.ADMIN,
            subject="Broken {{ missing_subject }}",
            preheader="Broken",
            html_body="<p>Missing {{ missing_html }}</p>",
            text_body="Missing {{ missing_text }}",
            cta_label="Open",
            cta_url="{{ missing_url }}",
        )

        with patch("app.api.routes.email.EMAIL_TEMPLATES", [broken_template]):
            response = self.client.post(
                "/api/admin/test-email/send",
                headers=self.admin_headers(),
                json={"template_key": "broken_template"},
            )

        self.assertEqual(response.status_code, 422)
        detail = response.json()["detail"]
        self.assertEqual(detail["message"], "Email template has unresolved variables")
        self.assertEqual(
            detail["unresolved_variables"],
            ["missing_html", "missing_subject", "missing_text", "missing_url"],
        )


class AuthEmailServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_password_reset_email_uses_branded_layout(self):
        delivery = AsyncMock(
            return_value=EmailDeliveryResult(
                sent=True,
                provider="resend",
                provider_id="email-test-123",
            )
        )
        service = AuthEmailService(delivery=type("Delivery", (), {"send_email": delivery})())
        user = User(
            id="user-test123",
            name="Fikri Firdaus",
            email="fikri@example.com",
            email_verified_at=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        await service.send_password_reset_email(user, "reset-token-test")

        call_kwargs = delivery.await_args.kwargs
        self.assertIn("https://conversease.com/logo.svg", call_kwargs["html_body"])
        self.assertIn("Reset password Conversease", call_kwargs["html_body"])
        self.assertIn("reset-password?token=reset-token-test", call_kwargs["html_body"])
        self.assertIn("Jika kamu tidak meminta reset password", call_kwargs["text_body"])


if __name__ == "__main__":
    unittest.main()
