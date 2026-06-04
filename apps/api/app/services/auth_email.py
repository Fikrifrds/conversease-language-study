from dataclasses import dataclass
from typing import Optional

from app.core.config import settings
from app.domain.email import branded_email_html
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
            html_body=branded_email_html(
                public_app_url=settings.public_app_url,
                preheader="Satu langkah lagi untuk mulai belajar lewat percakapan.",
                title="Verifikasi email kamu",
                body_html=(
                    f'<p style="margin: 0 0 14px;">Hi {escape_text(user.name)},</p>'
                    '<p style="margin: 0 0 18px;">Klik tombol di bawah untuk mengaktifkan akun '
                    "Conversease kamu dan mulai mission pertama.</p>"
                ),
                cta_label="Verifikasi Email",
                cta_url=verify_url,
                footer_note="Jika kamu tidak membuat akun Conversease, abaikan email ini.",
            ),
            text_body=(
                f"Hi {user.name},\n\n"
                "Klik link berikut untuk verifikasi email Conversease kamu:\n"
                f"{verify_url}\n\n"
                "Jika kamu tidak membuat akun Conversease, abaikan email ini."
            ),
            idempotency_key=f"auth-verify:{user.id}:{token[:12]}",
        )
        return self._result(result, verify_url)

    async def send_password_reset_email(self, user: User, token: str) -> AuthEmailResult:
        reset_url = f"{settings.public_app_url.rstrip('/')}/reset-password?token={token}"
        result = await self.delivery.send_email(
            recipient_email=user.email,
            subject="Reset password Conversease",
            html_body=branded_email_html(
                public_app_url=settings.public_app_url,
                preheader="Buat password baru untuk akun Conversease kamu.",
                title="Reset password Conversease",
                body_html=(
                    f'<p style="margin: 0 0 14px;">Hi {escape_text(user.name)},</p>'
                    '<p style="margin: 0 0 18px;">Klik tombol di bawah untuk membuat password '
                    "baru. Link ini hanya untuk permintaan reset password terbaru.</p>"
                ),
                cta_label="Reset Password",
                cta_url=reset_url,
                footer_note="Jika kamu tidak meminta reset password, abaikan email ini.",
            ),
            text_body=(
                f"Hi {user.name},\n\n"
                "Klik link berikut untuk reset password Conversease:\n"
                f"{reset_url}\n\n"
                "Jika kamu tidak meminta reset password, abaikan email ini."
            ),
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
