from dataclasses import dataclass
from typing import Optional

from app.core.config import settings
from app.domain.email import branded_email_html
from app.domain.users import User
from app.services.auth_email import escape_text
from app.services.email_delivery import EmailDeliveryResult, EmailDeliveryService


@dataclass(frozen=True)
class LearningEmailResult:
    sent: bool
    provider: str
    error: Optional[str] = None


class LearningEmailService:
    """Learning lifecycle emails (e.g. completing a level)."""

    def __init__(self, delivery: Optional[EmailDeliveryService] = None) -> None:
        self.delivery = delivery or EmailDeliveryService()

    async def send_level_completed_email(
        self,
        user: User,
        *,
        completed_level: str,
        completed_level_title: str,
        next_level: Optional[str],
        next_level_title: Optional[str],
    ) -> LearningEmailResult:
        courses_url = f"{settings.public_app_url.rstrip('/')}/courses"
        if next_level:
            next_line = (
                f"Level {escape_text(next_level)} ({escape_text(next_level_title or '')}) "
                "sekarang terbuka. Lanjutkan momentum kamu!"
            )
            cta_label = f"Mulai Level {next_level}"
            text_next = f"Level {next_level} sekarang terbuka. Lanjutkan: {courses_url}"
        else:
            next_line = (
                "Kamu sudah menyelesaikan level tertinggi yang tersedia. Luar biasa! "
                "Terus berlatih lewat Conversation Coach dan Partner."
            )
            cta_label = "Lihat Progress"
            text_next = f"Terus berlatih: {courses_url}"

        result = await self.delivery.send_email(
            recipient_email=user.email,
            subject=f"Selamat! Kamu menyelesaikan level {completed_level} 🎉",
            html_body=branded_email_html(
                public_app_url=settings.public_app_url,
                preheader=f"Level {completed_level} selesai. {('Level ' + next_level + ' terbuka.') if next_level else ''}",
                title=f"Level {completed_level} selesai!",
                body_html=(
                    f'<p style="margin: 0 0 14px;">Hi {escape_text(user.name)},</p>'
                    f'<p style="margin: 0 0 14px;">Selamat! Kamu sudah menyelesaikan semua lesson di '
                    f"<strong>{escape_text(completed_level)} - {escape_text(completed_level_title)}</strong>.</p>"
                    f'<p style="margin: 0 0 18px;">{next_line}</p>'
                ),
                cta_label=cta_label,
                cta_url=courses_url,
                footer_note="Kamu menerima email ini karena menyelesaikan sebuah level di Conversease.",
            ),
            text_body=(
                f"Hi {user.name},\n\n"
                f"Selamat! Kamu menyelesaikan level {completed_level} - {completed_level_title}.\n"
                f"{text_next}"
            ),
            idempotency_key=f"level-complete:{user.id}:{completed_level}",
        )
        return LearningEmailResult(sent=result.sent, provider=result.provider, error=result.error)
