from datetime import date, datetime, timedelta
import unittest

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db import models  # noqa: F401
from app.db.base import Base
from app.domain.payment import PaymentKind
from app.repositories.billing import (
    BillingRepository,
    InsufficientMinutesError,
    InvalidPaymentStateError,
    ManualTransferCodeUnavailableError,
)


class BillingRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def test_free_access_grants_trial_minutes_once(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            repository.ensure_free_access("user-123")
            repository.ensure_free_access("user-123")
            access = repository.access_summary("user-123")

            self.assertEqual(access["plan_key"], "free")
            self.assertFalse(access["is_pro"])
            self.assertEqual(access["minutes"]["subscription_minutes"], 10)

    def test_sandbox_subscription_activation_grants_pro_minutes(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            order = repository.activate_package_now(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            access = repository.access_summary("user-123")

            self.assertEqual(order.status, "success")
            self.assertTrue(access["is_pro"])
            self.assertEqual(access["plan_key"], "pro_1_month")
            self.assertGreaterEqual(access["minutes"]["subscription_minutes"], 300)

    def test_manual_transfer_order_uses_unique_amount(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            self.assertEqual(order.provider, "manual_transfer")
            self.assertEqual(order.status, "pending")
            self.assertEqual(order.base_amount_idr, 49000)
            self.assertIsNotNone(order.unique_code)
            self.assertEqual(order.amount_idr, 49000 + order.unique_code)

    def test_repeat_checkout_for_same_pending_package_returns_existing_order(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            first = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            second = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            self.assertEqual(first.id, second.id)
            self.assertEqual(first.unique_code, second.unique_code)

    def test_concurrent_checkout_cannot_reuse_active_unique_code(self):
        # Simulates two near-simultaneous checkouts both computing the same
        # "free" unique code before either commits: the DB constraint should
        # reject the second insert, and the retry loop should recover with a
        # different code instead of leaving two active orders with the same
        # transfer amount.
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            codes = iter([101, 101, 102])
            repository._next_manual_transfer_unique_code = lambda: next(codes)

            first = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            second = repository.create_manual_transfer_order(
                user_id="user-456",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            self.assertEqual(first.unique_code, 101)
            self.assertEqual(second.unique_code, 102)
            self.assertNotEqual(first.amount_idr, second.amount_idr)

    def test_confirm_records_chosen_destination_bank(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            target = settings.manual_transfer_accounts[-1]

            repository.confirm_manual_transfer(
                user_id="user-123",
                order_id=order.id,
                transfer_date=date.today(),
                sender_name="QA Sender",
                target_bank=target["bank_name"],
            )

            self.assertEqual(order.status, "confirmed")
            self.assertEqual(order.metadata_json["bank_name"], target["bank_name"])
            self.assertEqual(
                order.metadata_json["bank_account_number"], target["bank_account_number"]
            )

    def test_confirm_rejects_unknown_destination_bank(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            with self.assertRaises(InvalidPaymentStateError):
                repository.confirm_manual_transfer(
                    user_id="user-123",
                    order_id=order.id,
                    transfer_date=date.today(),
                    sender_name="QA Sender",
                    target_bank="Bank Tidak Terdaftar",
                )

    def test_cancel_pending_order_releases_unique_code(self):
        original_min = settings.manual_transfer_unique_code_min
        original_max = settings.manual_transfer_unique_code_max
        settings.manual_transfer_unique_code_min = 101
        settings.manual_transfer_unique_code_max = 101

        try:
            with self.SessionLocal() as db:
                repository = BillingRepository(db)
                order = repository.create_manual_transfer_order(
                    user_id="user-123",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )

                cancelled = repository.cancel_manual_transfer_order(user_id="user-123", order_id=order.id)

                self.assertEqual(cancelled.status, "failed")
                self.assertTrue(cancelled.metadata_json["cancelled_by_user"])

                # The single available code (101) was cancelled-and-released, so a
                # brand new order can claim it instead of hitting a 503.
                replacement = repository.create_manual_transfer_order(
                    user_id="user-456",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )
                self.assertEqual(replacement.unique_code, 101)
        finally:
            settings.manual_transfer_unique_code_min = original_min
            settings.manual_transfer_unique_code_max = original_max

    def test_cancel_confirmed_order_before_approval_succeeds(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            repository.confirm_manual_transfer(
                user_id="user-123",
                order_id=order.id,
                transfer_date=date.today(),
                target_bank=settings.manual_transfer_bank_name,
            )

            cancelled = repository.cancel_manual_transfer_order(user_id="user-123", order_id=order.id)

            self.assertEqual(cancelled.status, "failed")

    def test_cancel_approved_order_is_rejected(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            repository.approve_manual_order(order_id=order.id, approved_by="Admin")

            with self.assertRaises(InvalidPaymentStateError):
                repository.cancel_manual_transfer_order(user_id="user-123", order_id=order.id)

    def test_cancel_order_owned_by_another_user_raises(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            with self.assertRaises(KeyError):
                repository.cancel_manual_transfer_order(user_id="user-999", order_id=order.id)

    def test_list_user_payment_orders_scopes_to_user(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            mine_first = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            mine_second = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_3_months",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            repository.create_manual_transfer_order(
                user_id="user-999",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            orders = repository.list_user_payment_orders("user-123")

            self.assertEqual([order.id for order in orders], [mine_second.id, mine_first.id])

    def test_manual_transfer_unique_code_skips_active_orders(self):
        original_min = settings.manual_transfer_unique_code_min
        original_max = settings.manual_transfer_unique_code_max
        settings.manual_transfer_unique_code_min = 101
        settings.manual_transfer_unique_code_max = 102

        try:
            with self.SessionLocal() as db:
                repository = BillingRepository(db)

                first = repository.create_manual_transfer_order(
                    user_id="user-123",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )
                second = repository.create_manual_transfer_order(
                    user_id="user-456",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )

                self.assertNotEqual(first.unique_code, second.unique_code)
                self.assertEqual({first.unique_code, second.unique_code}, {101, 102})
        finally:
            settings.manual_transfer_unique_code_min = original_min
            settings.manual_transfer_unique_code_max = original_max

    def test_manual_transfer_unique_code_can_reuse_inactive_orders(self):
        original_min = settings.manual_transfer_unique_code_min
        original_max = settings.manual_transfer_unique_code_max
        settings.manual_transfer_unique_code_min = 101
        settings.manual_transfer_unique_code_max = 101

        try:
            with self.SessionLocal() as db:
                repository = BillingRepository(db)

                failed = repository.create_manual_transfer_order(
                    user_id="user-123",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )
                repository.reject_manual_order(failed.id, approved_by="Admin", notes="Expired")
                replacement = repository.create_manual_transfer_order(
                    user_id="user-456",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )

                self.assertEqual(failed.unique_code, 101)
                self.assertEqual(replacement.unique_code, 101)
        finally:
            settings.manual_transfer_unique_code_min = original_min
            settings.manual_transfer_unique_code_max = original_max

    def test_manual_transfer_unique_code_raises_when_active_range_is_full(self):
        original_min = settings.manual_transfer_unique_code_min
        original_max = settings.manual_transfer_unique_code_max
        settings.manual_transfer_unique_code_min = 101
        settings.manual_transfer_unique_code_max = 101

        try:
            with self.SessionLocal() as db:
                repository = BillingRepository(db)

                repository.create_manual_transfer_order(
                    user_id="user-123",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )

                with self.assertRaises(ManualTransferCodeUnavailableError):
                    repository.create_manual_transfer_order(
                        user_id="user-456",
                        package_key="pro_1_month",
                        payment_kind=PaymentKind.SUBSCRIPTION,
                    )
        finally:
            settings.manual_transfer_unique_code_min = original_min
            settings.manual_transfer_unique_code_max = original_max

    def test_stale_manual_transfer_order_expires_and_releases_unique_code(self):
        original_min = settings.manual_transfer_unique_code_min
        original_max = settings.manual_transfer_unique_code_max
        settings.manual_transfer_unique_code_min = 101
        settings.manual_transfer_unique_code_max = 101

        try:
            with self.SessionLocal() as db:
                repository = BillingRepository(db)
                order = repository.create_manual_transfer_order(
                    user_id="user-123",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )
                order.created_at = datetime.utcnow() - timedelta(
                    hours=settings.manual_transfer_expire_hours + 1
                )
                db.commit()

                expired_count = repository.expire_stale_manual_transfer_orders()
                replacement = repository.create_manual_transfer_order(
                    user_id="user-456",
                    package_key="pro_1_month",
                    payment_kind=PaymentKind.SUBSCRIPTION,
                )

                self.assertEqual(expired_count, 1)
                self.assertEqual(order.status, "expired")
                self.assertEqual(replacement.unique_code, 101)
        finally:
            settings.manual_transfer_unique_code_min = original_min
            settings.manual_transfer_unique_code_max = original_max

    def test_stale_manual_transfer_order_cannot_be_confirmed(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            order.created_at = datetime.utcnow() - timedelta(
                hours=settings.manual_transfer_expire_hours + 1
            )
            db.commit()

            with self.assertRaises(InvalidPaymentStateError):
                repository.confirm_manual_transfer(
                    user_id="user-123",
                    order_id=order.id,
                    transfer_date=date.today(),
                    sender_name="QA Sender",
                    target_bank="Bank Jago",
                )

            self.assertEqual(order.status, "expired")

    def test_stale_manual_transfer_order_cannot_be_approved(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            order.created_at = datetime.utcnow() - timedelta(
                hours=settings.manual_transfer_expire_hours + 1
            )
            db.commit()

            with self.assertRaises(InvalidPaymentStateError):
                repository.approve_manual_order(order.id, approved_by="Admin")

            self.assertEqual(order.status, "expired")

    def test_get_manual_payment_order_expires_stale_pending_order(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)
            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            order.created_at = datetime.utcnow() - timedelta(
                hours=settings.manual_transfer_expire_hours + 1
            )
            db.commit()

            detail = repository.get_manual_payment_order(order.id)

            self.assertEqual(detail.status, "expired")
            self.assertEqual(detail.metadata_json["expiry_reason"], "manual_transfer_confirmation_window_elapsed")

    def test_manual_transfer_approval_is_idempotent(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            first = repository.approve_manual_order(order.id, approved_by="Admin")
            second = repository.approve_manual_order(order.id, approved_by="Admin")
            subscriptions = db.execute(
                select(models.UserSubscriptionModel).where(
                    models.UserSubscriptionModel.user_id == "user-123",
                    models.UserSubscriptionModel.plan_key == "pro_1_month",
                )
            ).scalars().all()

            self.assertEqual(first.status, "success")
            self.assertEqual(second.status, "success")
            self.assertEqual(len(subscriptions), 1)

    def test_manual_transfer_cannot_be_completed_by_sandbox_endpoint(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )

            with self.assertRaises(InvalidPaymentStateError):
                repository.complete_sandbox_order(user_id="user-123", order_id=order.id)

    def test_get_manual_payment_order_rejects_sandbox_order(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            manual_order = repository.create_manual_transfer_order(
                user_id="user-123",
                package_key="pro_1_month",
                payment_kind=PaymentKind.SUBSCRIPTION,
            )
            sandbox_order = repository.create_sandbox_order(
                user_id="user-123",
                package_key="topup_60",
                payment_kind=PaymentKind.TOPUP,
            )

            self.assertEqual(repository.get_manual_payment_order(manual_order.id).id, manual_order.id)

            with self.assertRaises(KeyError):
                repository.get_manual_payment_order(sandbox_order.id)

    def test_topup_and_consumption_use_subscription_before_topup(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            repository.ensure_free_access("user-123")
            repository.activate_package_now(
                user_id="user-123",
                package_key="topup_60",
                payment_kind=PaymentKind.TOPUP,
            )
            consumption = repository.consume_minutes("user-123", 12, related_session_id="session-1")
            access = repository.access_summary("user-123")

            self.assertEqual(consumption["subscription_minutes_used"], 10)
            self.assertEqual(consumption["topup_minutes_used"], 2)
            self.assertEqual(access["minutes"]["topup_minutes"], 58)

    def test_consumption_raises_when_minutes_empty(self):
        with self.SessionLocal() as db:
            repository = BillingRepository(db)

            with self.assertRaises(InsufficientMinutesError):
                repository.consume_minutes("user-123", 11)


if __name__ == "__main__":
    unittest.main()
