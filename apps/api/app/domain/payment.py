from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class PaymentKind(str, Enum):
    SUBSCRIPTION = "subscription"
    TOPUP = "topup"


class PaymentStatus(str, Enum):
    CREATED = "created"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SUCCESS = "success"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass(frozen=True)
class CheckoutRequest:
    user_id: str
    package_key: str
    payment_kind: PaymentKind
    return_url: str


@dataclass(frozen=True)
class CheckoutSession:
    provider: str
    provider_reference: str
    checkout_url: str
    status: PaymentStatus
    metadata: Dict[str, str]


class PaymentProvider:
    async def create_checkout_session(self, request: CheckoutRequest) -> CheckoutSession:
        raise NotImplementedError

    async def verify_webhook(self, headers: Dict[str, str], payload: Dict[str, object]) -> bool:
        raise NotImplementedError

    async def normalize_webhook(self, payload: Dict[str, object]) -> Dict[str, Optional[str]]:
        raise NotImplementedError
