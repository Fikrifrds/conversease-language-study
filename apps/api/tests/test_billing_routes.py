import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.security import create_access_token
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.domain.payment import PaymentKind
from app.main import create_app
from app.repositories.billing import BillingRepository
from app.services.email_delivery import EmailDeliveryResult


class BillingRoutesTest(unittest.TestCase):
    def setUp(self):
        self.original_admin_key = settings.payment_admin_api_key
        settings.payment_admin_api_key = "test-admin-key-with-32-chars"
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def tearDown(self):
        settings.payment_admin_api_key = self.original_admin_key

    def admin_headers(self) -> dict[str, str]:
        return {"x-admin-api-key": settings.payment_admin_api_key}

    def client(self) -> TestClient:
        def override_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        app = create_app()
        app.dependency_overrides[get_db] = override_db
        return TestClient(app)

    def seed_user_and_sandbox_order(self) -> str:
        with self.SessionLocal() as db:
            now = datetime.utcnow()
            db.add(
                models.UserModel(
                    id="user-123",
                    name="QA Tester",
                    email="qa-billing@example.local",
                    password_hash="hashed",
                    email_verified_at=now,
                    created_at=now,
                    updated_at=now,
                )
            )
            order = BillingRepository(db).create_sandbox_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            db.commit()
            return order.id

    def seed_user_and_manual_order(self) -> str:
        with self.SessionLocal() as db:
            now = datetime.utcnow()
            db.add(
                models.UserModel(
                    id="user-123",
                    name="QA Tester",
                    email="qa-billing@example.local",
                    password_hash="hashed",
                    email_verified_at=now,
                    created_at=now,
                    updated_at=now,
                )
            )
            order = BillingRepository(db).create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            db.commit()
            return order.id

    def seed_second_user(self) -> None:
        with self.SessionLocal() as db:
            now = datetime.utcnow()
            db.add(
                models.UserModel(
                    id="user-456",
                    name="Other User",
                    email="other-billing@example.local",
                    password_hash="hashed",
                    email_verified_at=now,
                    created_at=now,
                    updated_at=now,
                )
            )
            db.commit()

    def test_sandbox_checkout_complete_is_disabled_in_production(self):
        client = self.client()
        order_id = self.seed_user_and_sandbox_order()
        token = create_access_token("user-123")
        original_app_env = settings.app_env
        settings.app_env = "production"

        try:
            response = client.post(
                f"/api/billing/checkout/{order_id}/sandbox-complete",
                headers={"Authorization": f"Bearer {token}"},
            )
        finally:
            settings.app_env = original_app_env
            client.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Sandbox checkout is disabled")

    def test_sandbox_checkout_complete_stays_available_for_local_qa(self):
        client = self.client()
        order_id = self.seed_user_and_sandbox_order()
        token = create_access_token("user-123")
        original_app_env = settings.app_env
        settings.app_env = "development"

        try:
            response = client.post(
                f"/api/billing/checkout/{order_id}/sandbox-complete",
                headers={"Authorization": f"Bearer {token}"},
            )
        finally:
            settings.app_env = original_app_env
            client.app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["status"], "success")

    def test_manual_transfer_checkout_returns_503_when_unique_codes_are_full(self):
        client = self.client()
        self.seed_user_and_sandbox_order()
        token = create_access_token("user-123")
        original_min = settings.manual_transfer_unique_code_min
        original_max = settings.manual_transfer_unique_code_max
        settings.manual_transfer_unique_code_min = 101
        settings.manual_transfer_unique_code_max = 101

        try:
            first = client.post(
                "/api/billing/checkout",
                headers={"Authorization": f"Bearer {token}"},
                json={"package_key": "pro_1_month", "payment_kind": "subscription"},
            )
            second = client.post(
                "/api/billing/checkout",
                headers={"Authorization": f"Bearer {token}"},
                json={"package_key": "pro_1_month", "payment_kind": "subscription"},
            )
        finally:
            settings.manual_transfer_unique_code_min = original_min
            settings.manual_transfer_unique_code_max = original_max
            client.app.dependency_overrides.clear()

        self.assertEqual(first.status_code, 200)
        self.assertIsNotNone(first.json()["data"]["expires_at"])
        self.assertEqual(second.status_code, 503)
        self.assertEqual(
            second.json()["detail"],
            "Manual transfer unique codes are temporarily unavailable",
        )

    def test_user_can_get_own_manual_transfer_order_from_checkout_url(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        token = create_access_token("user-123")

        response = client.get(
            f"/api/billing/checkout/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["id"], order_id)
        self.assertEqual(data["status"], "pending")
        self.assertIsNotNone(data["expires_at"])

    def test_user_cannot_get_another_users_manual_transfer_order(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        self.seed_second_user()
        token = create_access_token("user-456")

        response = client.get(
            f"/api/billing/checkout/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 404)

    def test_user_get_manual_transfer_order_expires_stale_pending_order(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        token = create_access_token("user-123")
        with self.SessionLocal() as db:
            order = db.get(models.PaymentOrderModel, order_id)
            assert order is not None
            order.created_at = datetime.utcnow() - timedelta(
                hours=settings.manual_transfer_expire_hours + 1
            )
            db.commit()

        response = client.get(
            f"/api/billing/checkout/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["status"], "expired")
        self.assertEqual(
            data["metadata"]["expiry_reason"],
            "manual_transfer_confirmation_window_elapsed",
        )

    def test_admin_get_manual_transfer_expires_stale_pending_order(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        with self.SessionLocal() as db:
            order = db.get(models.PaymentOrderModel, order_id)
            assert order is not None
            order.created_at = datetime.utcnow() - timedelta(
                hours=settings.manual_transfer_expire_hours + 1
            )
            db.commit()

        response = client.get(
            f"/api/admin/payment-orders/{order_id}",
            headers=self.admin_headers(),
        )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["status"], "expired")
        self.assertIsNone(data["expires_at"])
        self.assertEqual(
            data["metadata"]["expiry_reason"],
            "manual_transfer_confirmation_window_elapsed",
        )

    def test_admin_approve_manual_transfer_sends_user_success_email(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        delivery = AsyncMock(
            return_value=EmailDeliveryResult(
                sent=True,
                provider="resend",
                provider_id="email-payment-approved",
            )
        )

        with patch("app.api.routes.billing.EmailDeliveryService") as delivery_service:
            delivery_service.return_value.send_email = delivery
            response = client.post(
                f"/api/admin/payment-orders/{order_id}/approve",
                headers=self.admin_headers(),
                json={"approved_by": "QA Admin", "notes": "Nominal cocok"},
            )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["metadata"]["customer_decision_email"]["sent"], True)
        self.assertEqual(data["metadata"]["customer_decision_email"]["attempt_count"], 1)
        self.assertEqual(
            data["metadata"]["customer_decision_email"]["template_key"],
            "payment_manual_approved",
        )
        delivery.assert_awaited_once()
        call_kwargs = delivery.await_args.kwargs
        self.assertEqual(call_kwargs["recipient_email"], "qa-billing@example.local")
        self.assertIn("sudah disetujui", call_kwargs["subject"])
        self.assertIn("Pro 1 Month", call_kwargs["text_body"])
        self.assertEqual(
            call_kwargs["idempotency_key"],
            f"user-123:payment_manual_approved:{order_id}",
        )

    def test_admin_approve_manual_transfer_does_not_resend_success_email(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        delivery = AsyncMock(
            return_value=EmailDeliveryResult(
                sent=True,
                provider="resend",
                provider_id="email-payment-approved",
            )
        )

        with patch("app.api.routes.billing.EmailDeliveryService") as delivery_service:
            delivery_service.return_value.send_email = delivery
            first = client.post(
                f"/api/admin/payment-orders/{order_id}/approve",
                headers=self.admin_headers(),
                json={"approved_by": "QA Admin", "notes": "Nominal cocok"},
            )
            second = client.post(
                f"/api/admin/payment-orders/{order_id}/approve",
                headers=self.admin_headers(),
                json={"approved_by": "QA Admin", "notes": "Klik ulang"},
            )

        client.app.dependency_overrides.clear()
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        delivery.assert_awaited_once()

    def test_admin_approve_manual_transfer_records_failed_user_email_delivery(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        delivery = AsyncMock(
            return_value=EmailDeliveryResult(
                sent=False,
                provider="resend",
                error="RESEND_API_KEY is not configured",
            )
        )

        with patch("app.api.routes.billing.EmailDeliveryService") as delivery_service:
            delivery_service.return_value.send_email = delivery
            response = client.post(
                f"/api/admin/payment-orders/{order_id}/approve",
                headers=self.admin_headers(),
                json={"approved_by": "QA Admin", "notes": "Nominal cocok"},
            )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["metadata"]["customer_decision_email"]["sent"], False)
        self.assertEqual(
            data["metadata"]["customer_decision_email"]["error"],
            "RESEND_API_KEY is not configured",
        )

    def test_admin_reject_manual_transfer_sends_user_rejection_email(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        delivery = AsyncMock(
            return_value=EmailDeliveryResult(
                sent=True,
                provider="resend",
                provider_id="email-payment-rejected",
            )
        )

        with patch("app.api.routes.billing.EmailDeliveryService") as delivery_service:
            delivery_service.return_value.send_email = delivery
            response = client.post(
                f"/api/admin/payment-orders/{order_id}/reject",
                headers=self.admin_headers(),
                json={"approved_by": "QA Admin", "notes": "Nominal tidak cocok"},
            )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["metadata"]["customer_decision_email"]["sent"], True)
        self.assertEqual(
            data["metadata"]["customer_decision_email"]["template_key"],
            "payment_manual_rejected",
        )
        delivery.assert_awaited_once()
        call_kwargs = delivery.await_args.kwargs
        self.assertEqual(call_kwargs["recipient_email"], "qa-billing@example.local")
        self.assertIn("perlu dicek ulang", call_kwargs["subject"])
        self.assertIn("Nominal tidak cocok", call_kwargs["text_body"])
        self.assertEqual(
            call_kwargs["idempotency_key"],
            f"user-123:payment_manual_rejected:{order_id}",
        )

    def test_admin_resend_decision_email_for_approved_manual_transfer(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()
        delivery = AsyncMock(
            side_effect=[
                EmailDeliveryResult(
                    sent=True,
                    provider="resend",
                    provider_id="email-payment-approved",
                ),
                EmailDeliveryResult(
                    sent=True,
                    provider="resend",
                    provider_id="email-payment-approved-resend",
                ),
            ]
        )

        with patch("app.api.routes.billing.EmailDeliveryService") as delivery_service:
            delivery_service.return_value.send_email = delivery
            approve_response = client.post(
                f"/api/admin/payment-orders/{order_id}/approve",
                headers=self.admin_headers(),
                json={"approved_by": "QA Admin", "notes": "Nominal cocok"},
            )
            resend_response = client.post(
                f"/api/admin/payment-orders/{order_id}/resend-decision-email",
                headers=self.admin_headers(),
                json={"requested_by": "QA Admin"},
            )

        client.app.dependency_overrides.clear()
        self.assertEqual(approve_response.status_code, 200)
        self.assertEqual(resend_response.status_code, 200)
        data = resend_response.json()["data"]
        self.assertTrue(data["email"]["sent"])
        self.assertEqual(data["order"]["metadata"]["customer_decision_email"]["attempt_count"], 2)
        self.assertEqual(
            data["order"]["metadata"]["customer_decision_email"]["trigger"],
            "resend:qa-admin",
        )
        self.assertEqual(
            delivery.await_args_list[1].kwargs["idempotency_key"],
            f"user-123:payment_manual_approved:{order_id}:resend:qa-admin:2",
        )

    def test_admin_resend_decision_email_rejects_pending_order(self):
        client = self.client()
        order_id = self.seed_user_and_manual_order()

        response = client.post(
            f"/api/admin/payment-orders/{order_id}/resend-decision-email",
            headers=self.admin_headers(),
            json={"requested_by": "QA Admin"},
        )

        client.app.dependency_overrides.clear()
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
