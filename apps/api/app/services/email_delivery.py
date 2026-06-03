from dataclasses import dataclass
from typing import Optional

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class EmailDeliveryResult:
    sent: bool
    provider: str
    provider_id: Optional[str] = None
    error: Optional[str] = None


class EmailDeliveryService:
    async def send_email(
        self,
        recipient_email: str,
        subject: str,
        html_body: str,
        text_body: str,
        reply_to: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> EmailDeliveryResult:
        if not settings.resend_api_key:
            return EmailDeliveryResult(
                sent=False,
                provider="resend",
                error="RESEND_API_KEY is not configured",
            )

        payload = {
            "from": settings.email_from,
            "to": [recipient_email],
            "subject": subject,
            "html": html_body,
            "text": text_body,
        }

        if reply_to or settings.email_reply_to:
            payload["reply_to"] = reply_to or settings.email_reply_to

        try:
            headers = {"Authorization": f"Bearer {settings.resend_api_key}"}
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    "https://api.resend.com/emails",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            return EmailDeliveryResult(sent=False, provider="resend", error=str(exc))

        data = response.json()
        return EmailDeliveryResult(
            sent=True,
            provider="resend",
            provider_id=data.get("id"),
        )
