import unittest
from datetime import datetime, timedelta

from app.domain.minutes import (
    BalanceType,
    MinuteSource,
    MinuteTransaction,
    calculate_balance,
    plan_consumption,
    usage_transactions_for_consumption,
)


class MinuteRulesTest(unittest.TestCase):
    def test_subscription_minutes_are_consumed_before_topups(self):
        now = datetime.utcnow()
        balance = calculate_balance(
            [
                MinuteTransaction(
                    amount_minutes=10,
                    source=MinuteSource.SUBSCRIPTION_GRANT,
                    balance_type=BalanceType.SUBSCRIPTION,
                    created_at=now,
                    expires_at=now + timedelta(days=10),
                ),
                MinuteTransaction(
                    amount_minutes=30,
                    source=MinuteSource.TOPUP,
                    balance_type=BalanceType.TOPUP,
                    created_at=now,
                    expires_at=now + timedelta(days=365),
                ),
            ],
            now=now,
        )

        consumption = plan_consumption(balance, 25)

        self.assertTrue(consumption.allowed)
        self.assertEqual(consumption.subscription_minutes_used, 10)
        self.assertEqual(consumption.topup_minutes_used, 15)

    def test_expired_minutes_do_not_count(self):
        now = datetime.utcnow()
        balance = calculate_balance(
            [
                MinuteTransaction(
                    amount_minutes=300,
                    source=MinuteSource.SUBSCRIPTION_GRANT,
                    balance_type=BalanceType.SUBSCRIPTION,
                    created_at=now - timedelta(days=31),
                    expires_at=now - timedelta(days=1),
                )
            ],
            now=now,
        )

        self.assertEqual(balance.total_minutes, 0)

    def test_usage_transaction_amounts_are_negative(self):
        now = datetime.utcnow()
        consumption = plan_consumption(
            balance=calculate_balance(
                [
                    MinuteTransaction(
                        amount_minutes=20,
                        source=MinuteSource.SUBSCRIPTION_GRANT,
                        balance_type=BalanceType.SUBSCRIPTION,
                        created_at=now,
                    )
                ],
                now=now,
            ),
            requested_minutes=5,
        )

        transactions = usage_transactions_for_consumption(consumption, now, "session-1")

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].amount_minutes, -5)
        self.assertEqual(transactions[0].related_session_id, "session-1")


if __name__ == "__main__":
    unittest.main()

