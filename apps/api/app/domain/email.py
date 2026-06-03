from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re
from typing import Dict, Optional


class EmailStatus(str, Enum):
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    FAILED = "failed"
    SUPPRESSED = "suppressed"


class EmailCategory(str, Enum):
    AUTH = "auth"
    PAYMENT = "payment"
    SUBSCRIPTION = "subscription"
    LEARNING = "learning"
    EVALUATION = "evaluation"
    MINUTES = "minutes"
    ADMIN = "admin"


@dataclass(frozen=True)
class EmailTemplate:
    template_key: str
    category: EmailCategory
    subject: str
    preheader: str
    html_body: str
    text_body: str
    cta_label: str
    cta_url: str
    language_code: str = "id"
    version: int = 1
    is_active: bool = True


@dataclass(frozen=True)
class EmailEvent:
    template_key: str
    recipient_email: str
    payload: Dict[str, str]
    idempotency_key: str
    status: EmailStatus = EmailStatus.QUEUED
    scheduled_at: Optional[datetime] = None


def build_idempotency_key(user_id: str, template_key: str, event_id: str) -> str:
    return f"{user_id}:{template_key}:{event_id}"


def render_template(template: str, payload: Dict[str, str]) -> str:
    rendered = template
    for key, value in payload.items():
        rendered = rendered.replace("{{ " + key + " }}", value)
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def unresolved_template_variables(rendered_template: str) -> list[str]:
    return sorted(set(re.findall(r"{{\s*([a-zA-Z0-9_]+)\s*}}", rendered_template)))
