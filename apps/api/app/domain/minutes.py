from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Iterable, List, Optional


class BalanceType(str, Enum):
    SUBSCRIPTION = "subscription"
    TOPUP = "topup"


class MinuteSource(str, Enum):
    SUBSCRIPTION_GRANT = "subscription_grant"
    TOPUP = "topup"
    USAGE = "usage"
    REFUND = "refund"
    ADMIN_ADJUSTMENT = "admin_adjustment"
    EXPIRY = "expiry"


@dataclass(frozen=True)
class MinuteTransaction:
    amount_minutes: int
    source: MinuteSource
    balance_type: BalanceType
    created_at: datetime
    expires_at: Optional[datetime] = None
    related_session_id: Optional[str] = None


@dataclass(frozen=True)
class MinuteBalance:
    subscription_minutes: int
    topup_minutes: int

    @property
    def total_minutes(self) -> int:
        return self.subscription_minutes + self.topup_minutes


@dataclass(frozen=True)
class MinuteConsumption:
    requested_minutes: int
    subscription_minutes_used: int
    topup_minutes_used: int
    allowed: bool

    @property
    def total_used(self) -> int:
        return self.subscription_minutes_used + self.topup_minutes_used


def calculate_balance(
    transactions: Iterable[MinuteTransaction],
    now: Optional[datetime] = None,
) -> MinuteBalance:
    now = now or datetime.utcnow()
    subscription = 0
    topup = 0

    for transaction in transactions:
        if transaction.expires_at and transaction.expires_at <= now:
            continue

        if transaction.balance_type == BalanceType.SUBSCRIPTION:
            subscription += transaction.amount_minutes
        elif transaction.balance_type == BalanceType.TOPUP:
            topup += transaction.amount_minutes

    return MinuteBalance(
        subscription_minutes=max(subscription, 0),
        topup_minutes=max(topup, 0),
    )


def plan_consumption(balance: MinuteBalance, requested_minutes: int) -> MinuteConsumption:
    if requested_minutes <= 0:
        return MinuteConsumption(0, 0, 0, True)

    subscription_used = min(balance.subscription_minutes, requested_minutes)
    remaining = requested_minutes - subscription_used
    topup_used = min(balance.topup_minutes, remaining)

    return MinuteConsumption(
        requested_minutes=requested_minutes,
        subscription_minutes_used=subscription_used,
        topup_minutes_used=topup_used,
        allowed=(subscription_used + topup_used) >= requested_minutes,
    )


def usage_transactions_for_consumption(
    consumption: MinuteConsumption,
    created_at: datetime,
    related_session_id: Optional[str] = None,
) -> List[MinuteTransaction]:
    transactions: List[MinuteTransaction] = []

    if consumption.subscription_minutes_used:
        transactions.append(
            MinuteTransaction(
                amount_minutes=-consumption.subscription_minutes_used,
                source=MinuteSource.USAGE,
                balance_type=BalanceType.SUBSCRIPTION,
                created_at=created_at,
                related_session_id=related_session_id,
            )
        )

    if consumption.topup_minutes_used:
        transactions.append(
            MinuteTransaction(
                amount_minutes=-consumption.topup_minutes_used,
                source=MinuteSource.USAGE,
                balance_type=BalanceType.TOPUP,
                created_at=created_at,
                related_session_id=related_session_id,
            )
        )

    return transactions

