from dataclasses import dataclass
from typing import Optional

from app.core.config import settings
from app.domain.users import User
from app.services.email_delivery import EmailDeliveryResult, EmailDeliveryService


@dataclass(frozen=True)
class AuthEmailResult:
    sent: bool
    provider: str
    error: Optional[str] = None
    url: Optional[str] = None


class AuthEmailService:
    def __init__(self, delivery: Optional[EmailDeliveryService] = None) -> None:
        self.delivery = delivery or EmailDeliveryService()

    async def send_verification_email(self, user: User, token: str) -> AuthEmailResult:
        verify_url = f"{settings.public_app_url.rstrip('/')}/verify-email?token={token}"
        result = await self.delivery.send_email(
            recipient_email=user.email,
            subject="Verifikasi email Conversease kamu",
            html_body=(
                f"<p>Hi {escape_text(user.name)},</p>"
                "<p>Klik tombol berikut untuk verifikasi email Conversease kamu.</p>"
                f'<p><a href="{verify_url}">Verifikasi Email</a></p>'
                "<p>Jika kamu tidak membuat akun Conversease, abaikan email ini.</p>"
            ),
            text_body=(
                f"Hi {user.name}, buka link berikut untuk verifikasi email Conversease kamu: "
                f"{verify_url}"
            ),
            idempotency_key=f"auth-verify:{user.id}:{token[:12]}",
        )
        return self._result(result, verify_url)

    async def send_password_reset_email(self, user: User, token: str) -> AuthEmailResult:
        reset_url = f"{settings.public_app_url.rstrip('/')}/reset-password?token={token}"
        result = await self.delivery.send_email(
            recipient_email=user.email,
            subject="Reset password Conversease",
            html_body=(
                f"<p>Hi {escape_text(user.name)},</p>"
                "<p>Klik tombol berikut untuk membuat password baru.</p>"
                f'<p><a href="{reset_url}">Reset Password</a></p>'
                "<p>Jika kamu tidak meminta reset password, abaikan email ini.</p>"
            ),
            text_body=f"Hi {user.name}, buka link berikut untuk reset password Conversease: {reset_url}",
            idempotency_key=f"auth-reset:{user.id}:{token[:12]}",
        )
        return self._result(result, reset_url)

    def _result(self, result: EmailDeliveryResult, url: str) -> AuthEmailResult:
        return AuthEmailResult(
            sent=result.sent,
            provider=result.provider,
            error=result.error,
            url=url if not settings.is_production else None,
        )


def escape_text(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
