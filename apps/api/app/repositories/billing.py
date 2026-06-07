from datetime import date, datetime, time, timedelta
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.data.seed import SUBSCRIPTION_PLANS, TOPUP_PACKAGES
from app.db.models import MinuteLedgerEntryModel, PaymentOrderModel, UserSubscriptionModel
from app.domain.minutes import (
    BalanceType,
    MinuteSource,
    MinuteTransaction,
    calculate_balance,
    plan_consumption,
)
from app.domain.payment import PaymentKind, PaymentStatus


class InsufficientMinutesError(Exception):
    pass


class InvalidPaymentStateError(Exception):
    pass


class ManualTransferCodeUnavailableError(Exception):
    pass


MANUAL_TRANSFER_PROVIDER = "manual_transfer"
SANDBOX_PROVIDER = "sandbox"


class BillingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def expire_stale_manual_transfer_orders(
        self,
        now: Optional[datetime] = None,
        commit: bool = True,
    ) -> int:
        now = now or datetime.utcnow()
        cutoff = now - timedelta(hours=settings.manual_transfer_expire_hours)
        stale_orders = (
            self.db.execute(
                select(PaymentOrderModel).where(
                    PaymentOrderModel.provider == MANUAL_TRANSFER_PROVIDER,
                    PaymentOrderModel.status == PaymentStatus.PENDING.value,
                    PaymentOrderModel.created_at < cutoff,
                )
            )
            .scalars()
            .all()
        )

        for order in stale_orders:
            order.status = PaymentStatus.EXPIRED.value
            order.updated_at = now
            order.metadata_json = {
                **(order.metadata_json or {}),
                "expired_at": now.isoformat(),
                "expiry_reason": "manual_transfer_confirmation_window_elapsed",
            }

        if stale_orders:
            self.db.flush()
            if commit:
                self.db.commit()

        return len(stale_orders)

    def ensure_free_access(self, user_id: str) -> None:
        now = datetime.utcnow()
        existing = self.current_subscription(user_id, now=now)

        if existing is None:
            subscription = UserSubscriptionModel(
                id=f"sub-{uuid4().hex[:16]}",
                user_id=user_id,
                plan_key="free",
                status="active",
                starts_at=now,
                expires_at=None,
                created_at=now,
                updated_at=now,
            )
            self.db.add(subscription)

        has_free_grant = self.db.execute(
            select(MinuteLedgerEntryModel).where(
                MinuteLedgerEntryModel.user_id == user_id,
                MinuteLedgerEntryModel.source == MinuteSource.SUBSCRIPTION_GRANT.value,
                MinuteLedgerEntryModel.balance_type == BalanceType.SUBSCRIPTION.value,
                MinuteLedgerEntryModel.amount_minutes == 10,
            )
        ).scalar_one_or_none()

        if has_free_grant is None:
            self._add_minute_entry(
                user_id=user_id,
                amount_minutes=10,
                source=MinuteSource.SUBSCRIPTION_GRANT,
                balance_type=BalanceType.SUBSCRIPTION,
                expires_at=now + timedelta(days=30),
                created_at=now,
            )

        self.db.commit()

    def current_subscription(
        self,
        user_id: str,
        now: Optional[datetime] = None,
    ) -> Optional[UserSubscriptionModel]:
        now = now or datetime.utcnow()
        return self.db.execute(
            select(UserSubscriptionModel)
            .where(
                UserSubscriptionModel.user_id == user_id,
                UserSubscriptionModel.status == "active",
                (UserSubscriptionModel.expires_at.is_(None))
                | (UserSubscriptionModel.expires_at > now),
            )
            .order_by(UserSubscriptionModel.starts_at.desc())
            .limit(1)
        ).scalar_one_or_none()

    def is_pro(self, user_id: str, now: Optional[datetime] = None) -> bool:
        subscription = self.current_subscription(user_id, now=now)
        return bool(subscription) and subscription.plan_key != "free"

    def access_summary(self, user_id: str) -> dict:
        self.ensure_free_access(user_id)
        now = datetime.utcnow()
        subscription = self.current_subscription(user_id, now=now)
        plan = plan_by_key(subscription.plan_key if subscription else "free") or plan_by_key("free")
        balance = self.minute_balance(user_id, now=now)

        return {
            "plan_key": plan["key"],
            "plan_name": plan["name"],
            "is_pro": plan["key"] != "free",
            "status": subscription.status if subscription else "active",
            "expires_at": subscription.expires_at.isoformat() if subscription and subscription.expires_at else None,
            "minutes": {
                "subscription_minutes": balance.subscription_minutes,
                "topup_minutes": balance.topup_minutes,
                "total_minutes": balance.total_minutes,
            },
        }

    def minute_balance(self, user_id: str, now: Optional[datetime] = None):
        now = now or datetime.utcnow()
        transactions = [
            MinuteTransaction(
                amount_minutes=entry.amount_minutes,
                source=MinuteSource(entry.source),
                balance_type=BalanceType(entry.balance_type),
                created_at=entry.created_at,
                expires_at=entry.expires_at,
                related_session_id=entry.related_session_id,
            )
            for entry in self.db.execute(
                select(MinuteLedgerEntryModel)
                .where(MinuteLedgerEntryModel.user_id == user_id)
                .order_by(MinuteLedgerEntryModel.created_at.asc())
            )
            .scalars()
            .all()
        ]
        return calculate_balance(transactions, now=now)

    def consume_minutes(
        self,
        user_id: str,
        requested_minutes: int,
        related_session_id: Optional[str] = None,
    ) -> dict:
        self.ensure_free_access(user_id)
        now = datetime.utcnow()
        balance = self.minute_balance(user_id, now=now)
        consumption = plan_consumption(balance, requested_minutes)

        if not consumption.allowed:
            raise InsufficientMinutesError("Not enough Conversation Coach minutes")

        if consumption.subscription_minutes_used:
            self._add_minute_entry(
                user_id=user_id,
                amount_minutes=-consumption.subscription_minutes_used,
                source=MinuteSource.USAGE,
                balance_type=BalanceType.SUBSCRIPTION,
                related_session_id=related_session_id,
                created_at=now,
            )

        if consumption.topup_minutes_used:
            self._add_minute_entry(
                user_id=user_id,
                amount_minutes=-consumption.topup_minutes_used,
                source=MinuteSource.USAGE,
                balance_type=BalanceType.TOPUP,
                related_session_id=related_session_id,
                created_at=now,
            )

        self.db.commit()
        return {
            "requested_minutes": consumption.requested_minutes,
            "subscription_minutes_used": consumption.subscription_minutes_used,
            "topup_minutes_used": consumption.topup_minutes_used,
            "allowed": consumption.allowed,
        }

    def create_checkout_order(
        self,
        user_id: str,
        package_key: str,
        payment_kind: PaymentKind,
    ) -> PaymentOrderModel:
        return self.create_manual_transfer_order(
            user_id=user_id,
            package_key=package_key,
            payment_kind=payment_kind,
        )

    def create_manual_transfer_order(
        self,
        user_id: str,
        package_key: str,
        payment_kind: PaymentKind,
    ) -> PaymentOrderModel:
        package = package_by_key(package_key, payment_kind)
        if package is None:
            raise KeyError(package_key)

        now = datetime.utcnow()
        self.expire_stale_manual_transfer_orders(now=now, commit=False)
        order_id = f"order-{uuid4().hex[:16]}"
        base_amount_idr = int(package["price_idr"])
        unique_code = self._next_manual_transfer_unique_code()
        amount_idr = base_amount_idr + unique_code
        expires_at = now + timedelta(hours=settings.manual_transfer_expire_hours)
        order = PaymentOrderModel(
            id=order_id,
            user_id=user_id,
            package_key=package_key,
            payment_kind=payment_kind.value,
            status=PaymentStatus.PENDING.value,
            amount_idr=amount_idr,
            base_amount_idr=base_amount_idr,
            unique_code=unique_code,
            provider=MANUAL_TRANSFER_PROVIDER,
            provider_reference=f"manual-{unique_code}-{uuid4().hex[:10]}",
            checkout_url=f"/billing?order_id={order_id}",
            metadata_json={
                "package_name": package["name"],
                "base_amount_idr": base_amount_idr,
                "unique_code": unique_code,
                "bank_name": settings.manual_transfer_bank_name,
                "bank_account_number": settings.manual_transfer_account_number,
                "bank_account_holder": settings.manual_transfer_account_holder,
                "admin_email": settings.payment_admin_email,
                "confirmation_window": f"1x{settings.manual_transfer_expire_hours} jam",
                "expires_at": expires_at.isoformat(),
            },
            created_at=now,
            updated_at=now,
        )
        self.db.add(order)
        self.db.commit()
        return order

    def create_sandbox_order(
        self,
        user_id: str,
        package_key: str,
        payment_kind: PaymentKind,
    ) -> PaymentOrderModel:
        package = package_by_key(package_key, payment_kind)
        if package is None:
            raise KeyError(package_key)

        now = datetime.utcnow()
        order = PaymentOrderModel(
            id=f"order-{uuid4().hex[:16]}",
            user_id=user_id,
            package_key=package_key,
            payment_kind=payment_kind.value,
            status=PaymentStatus.PENDING.value,
            amount_idr=int(package["price_idr"]),
            base_amount_idr=int(package["price_idr"]),
            unique_code=None,
            provider=SANDBOX_PROVIDER,
            provider_reference=f"sandbox-{uuid4().hex[:16]}",
            checkout_url="/billing",
            metadata_json={"package_name": package["name"]},
            created_at=now,
            updated_at=now,
        )
        self.db.add(order)
        self.db.commit()
        return order

    def confirm_manual_transfer(
        self,
        user_id: str,
        order_id: str,
        transfer_date: date,
        sender_name: str,
        sender_bank: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> PaymentOrderModel:
        order = self.db.get(PaymentOrderModel, order_id)
        if order is None or order.user_id != user_id:
            raise KeyError(order_id)

        if order.provider != MANUAL_TRANSFER_PROVIDER:
            raise InvalidPaymentStateError("Only manual transfer orders can be confirmed")

        now = datetime.utcnow()
        if self._expire_pending_manual_transfer_order(order, now):
            self.db.commit()
            raise InvalidPaymentStateError("Payment order can no longer be confirmed")

        if order.status == PaymentStatus.SUCCESS.value:
            raise InvalidPaymentStateError("Payment order is already approved")

        if order.status in {PaymentStatus.FAILED.value, PaymentStatus.EXPIRED.value}:
            raise InvalidPaymentStateError("Payment order can no longer be confirmed")

        order.status = PaymentStatus.CONFIRMED.value
        order.transfer_date = datetime.combine(transfer_date, time.min)
        order.confirmed_at = order.confirmed_at or now
        order.updated_at = now
        order.metadata_json = {
            **(order.metadata_json or {}),
            "sender_name": sender_name.strip(),
            "sender_bank": (sender_bank or "").strip(),
            "transfer_date": transfer_date.isoformat(),
            "user_notes": (notes or "").strip(),
        }
        self.db.commit()
        return order

    def complete_sandbox_order(self, user_id: str, order_id: str) -> PaymentOrderModel:
        order = self.db.get(PaymentOrderModel, order_id)
        if order is None or order.user_id != user_id:
            raise KeyError(order_id)

        if order.provider != SANDBOX_PROVIDER:
            raise InvalidPaymentStateError("Only sandbox orders can be completed here")

        if order.status == PaymentStatus.SUCCESS.value:
            return order

        now = datetime.utcnow()
        order.status = PaymentStatus.SUCCESS.value
        order.updated_at = now

        if order.payment_kind == PaymentKind.SUBSCRIPTION.value:
            self._activate_subscription(user_id=user_id, plan_key=order.package_key, now=now)
        elif order.payment_kind == PaymentKind.TOPUP.value:
            self._grant_topup(user_id=user_id, topup_key=order.package_key, now=now)

        self.db.commit()
        return order

    def activate_package_now(
        self,
        user_id: str,
        package_key: str,
        payment_kind: PaymentKind,
    ) -> PaymentOrderModel:
        order = self.create_sandbox_order(
            user_id=user_id,
            package_key=package_key,
            payment_kind=payment_kind,
        )
        return self.complete_sandbox_order(user_id=user_id, order_id=order.id)

    def approve_manual_order(
        self,
        order_id: str,
        approved_by: str,
        notes: Optional[str] = None,
    ) -> PaymentOrderModel:
        order = self.db.get(PaymentOrderModel, order_id)
        if order is None:
            raise KeyError(order_id)

        if order.provider != MANUAL_TRANSFER_PROVIDER:
            raise InvalidPaymentStateError("Only manual transfer orders can be approved")

        now = datetime.utcnow()
        if self._expire_pending_manual_transfer_order(order, now):
            self.db.commit()
            raise InvalidPaymentStateError("Payment order can no longer be approved")

        if order.status == PaymentStatus.SUCCESS.value:
            return order

        if order.status in {PaymentStatus.FAILED.value, PaymentStatus.EXPIRED.value}:
            raise InvalidPaymentStateError("Payment order can no longer be approved")

        order.status = PaymentStatus.SUCCESS.value
        order.approved_at = now
        order.approved_by = approved_by.strip() or "admin"
        order.admin_notes = (notes or "").strip() or None
        order.updated_at = now

        if order.payment_kind == PaymentKind.SUBSCRIPTION.value:
            self._activate_subscription(user_id=order.user_id, plan_key=order.package_key, now=now)
        elif order.payment_kind == PaymentKind.TOPUP.value:
            self._grant_topup(user_id=order.user_id, topup_key=order.package_key, now=now)

        self.db.commit()
        return order

    def reject_manual_order(
        self,
        order_id: str,
        approved_by: str,
        notes: Optional[str] = None,
    ) -> PaymentOrderModel:
        order = self.db.get(PaymentOrderModel, order_id)
        if order is None:
            raise KeyError(order_id)

        if order.provider != MANUAL_TRANSFER_PROVIDER:
            raise InvalidPaymentStateError("Only manual transfer orders can be rejected")

        if order.status == PaymentStatus.SUCCESS.value:
            raise InvalidPaymentStateError("Approved payment orders cannot be rejected")

        now = datetime.utcnow()
        order.status = PaymentStatus.FAILED.value
        order.approved_by = approved_by.strip() or "admin"
        order.admin_notes = (notes or "").strip() or None
        order.updated_at = now
        self.db.commit()
        return order

    def get_manual_payment_order(self, order_id: str) -> PaymentOrderModel:
        order = self.db.get(PaymentOrderModel, order_id)
        if order is None or order.provider != MANUAL_TRANSFER_PROVIDER:
            raise KeyError(order_id)

        now = datetime.utcnow()
        if self._expire_pending_manual_transfer_order(order, now):
            self.db.commit()

        return order

    def get_user_manual_payment_order(self, user_id: str, order_id: str) -> PaymentOrderModel:
        order = self.db.get(PaymentOrderModel, order_id)
        if order is None or order.provider != MANUAL_TRANSFER_PROVIDER or order.user_id != user_id:
            raise KeyError(order_id)

        now = datetime.utcnow()
        if self._expire_pending_manual_transfer_order(order, now):
            self.db.commit()

        return order

    def list_payment_orders(
        self,
        status: Optional[str] = None,
        unique_code: Optional[int] = None,
        limit: int = 50,
    ) -> list[PaymentOrderModel]:
        self.expire_stale_manual_transfer_orders()
        query = select(PaymentOrderModel).where(PaymentOrderModel.provider == MANUAL_TRANSFER_PROVIDER)

        if status:
            query = query.where(PaymentOrderModel.status == status)

        if unique_code is not None:
            query = query.where(PaymentOrderModel.unique_code == unique_code)

        return (
            self.db.execute(query.order_by(PaymentOrderModel.updated_at.desc()).limit(limit))
            .scalars()
            .all()
        )

    def _activate_subscription(self, user_id: str, plan_key: str, now: datetime) -> None:
        plan = plan_by_key(plan_key)
        if plan is None:
            raise KeyError(plan_key)

        for subscription in self.db.execute(
            select(UserSubscriptionModel).where(
                UserSubscriptionModel.user_id == user_id,
                UserSubscriptionModel.status == "active",
                UserSubscriptionModel.plan_key != "free",
            )
        ).scalars():
            subscription.status = "replaced"
            subscription.updated_at = now

        duration_months = int(plan["duration_months"])
        expires_at = now + timedelta(days=max(duration_months, 1) * 30)
        subscription = UserSubscriptionModel(
            id=f"sub-{uuid4().hex[:16]}",
            user_id=user_id,
            plan_key=plan_key,
            status="active",
            starts_at=now,
            expires_at=expires_at,
            created_at=now,
            updated_at=now,
        )
        self.db.add(subscription)

        monthly_minutes = int(plan["monthly_minutes"])
        if monthly_minutes:
            self._add_minute_entry(
                user_id=user_id,
                amount_minutes=monthly_minutes,
                source=MinuteSource.SUBSCRIPTION_GRANT,
                balance_type=BalanceType.SUBSCRIPTION,
                expires_at=now + timedelta(days=30),
                created_at=now,
            )

    def _grant_topup(self, user_id: str, topup_key: str, now: datetime) -> None:
        topup = topup_by_key(topup_key)
        if topup is None:
            raise KeyError(topup_key)

        self._add_minute_entry(
            user_id=user_id,
            amount_minutes=int(topup["minutes"]),
            source=MinuteSource.TOPUP,
            balance_type=BalanceType.TOPUP,
            expires_at=now + timedelta(days=365),
            created_at=now,
        )

    def _add_minute_entry(
        self,
        user_id: str,
        amount_minutes: int,
        source: MinuteSource,
        balance_type: BalanceType,
        created_at: datetime,
        expires_at: Optional[datetime] = None,
        related_session_id: Optional[str] = None,
    ) -> MinuteLedgerEntryModel:
        entry = MinuteLedgerEntryModel(
            id=f"min-{uuid4().hex[:16]}",
            user_id=user_id,
            amount_minutes=amount_minutes,
            source=source.value,
            balance_type=balance_type.value,
            related_session_id=related_session_id,
            expires_at=expires_at,
            created_at=created_at,
        )
        self.db.add(entry)
        return entry

    def _next_manual_transfer_unique_code(self) -> int:
        minimum = settings.manual_transfer_unique_code_min
        maximum = settings.manual_transfer_unique_code_max
        span = maximum - minimum + 1
        active_statuses = [PaymentStatus.PENDING.value, PaymentStatus.CONFIRMED.value]
        used_codes = {
            code
            for code in self.db.execute(
                select(PaymentOrderModel.unique_code).where(
                    PaymentOrderModel.provider == MANUAL_TRANSFER_PROVIDER,
                    PaymentOrderModel.status.in_(active_statuses),
                    PaymentOrderModel.unique_code.is_not(None),
                )
            ).scalars()
            if code is not None
        }

        start = minimum + (uuid4().int % span)
        for offset in range(span):
            code = minimum + ((start - minimum + offset) % span)
            if code not in used_codes:
                return code

        raise ManualTransferCodeUnavailableError("No manual transfer unique codes available")

    def _manual_transfer_is_expired(self, order: PaymentOrderModel, now: datetime) -> bool:
        return order.created_at + timedelta(hours=settings.manual_transfer_expire_hours) < now

    def _expire_pending_manual_transfer_order(self, order: PaymentOrderModel, now: datetime) -> bool:
        if order.status != PaymentStatus.PENDING.value or not self._manual_transfer_is_expired(order, now):
            return False

        order.status = PaymentStatus.EXPIRED.value
        order.updated_at = now
        order.metadata_json = {
            **(order.metadata_json or {}),
            "expired_at": now.isoformat(),
            "expiry_reason": "manual_transfer_confirmation_window_elapsed",
        }
        return True


def plan_by_key(plan_key: str) -> Optional[dict]:
    return next((plan for plan in SUBSCRIPTION_PLANS if plan["key"] == plan_key), None)


def topup_by_key(topup_key: str) -> Optional[dict]:
    return next((topup for topup in TOPUP_PACKAGES if topup["key"] == topup_key), None)


def package_by_key(package_key: str, payment_kind: PaymentKind) -> Optional[dict]:
    if payment_kind == PaymentKind.SUBSCRIPTION:
        return plan_by_key(package_key)
    if payment_kind == PaymentKind.TOPUP:
        return topup_by_key(package_key)
    return None
