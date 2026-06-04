from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.admin_deps import require_admin_api_key
from app.data.seed import EMAIL_TEMPLATES
from app.core.config import settings
from app.domain.email import (
    branded_email_html,
    build_idempotency_key,
    render_template,
    unresolved_template_variables,
)
from app.services.email_delivery import EmailDeliveryService

router = APIRouter()


class TestEmailPayload(BaseModel):
    template_key: str = Field(min_length=2, max_length=120)
    variables: dict[str, str] = Field(default_factory=dict)
    user_id: str = Field(default="demo-user", min_length=2, max_length=120)
    event_id: str = Field(default="test", min_length=2, max_length=120)


class SendTestEmailPayload(TestEmailPayload):
    recipient_email: Optional[str] = Field(default=None, max_length=320)


@router.get("/admin/email-templates")
async def list_email_templates(_: bool = Depends(require_admin_api_key)) -> dict:
    return {
        "data": [
            {
                "template_key": template.template_key,
                "category": template.category,
                "subject": template.subject,
                "preheader": template.preheader,
                "language_code": template.language_code,
                "version": template.version,
                "is_active": template.is_active,
            }
            for template in EMAIL_TEMPLATES
        ]
    }


def get_email_template_or_404(template_key: str):
    template = next((item for item in EMAIL_TEMPLATES if item.template_key == template_key), None)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


def rendered_email_payload(payload: TestEmailPayload) -> dict:
    template = get_email_template_or_404(payload.template_key)
    variables = {**default_test_email_variables(), **payload.variables}
    subject = render_template(template.subject, variables)
    content_html = render_template(template.html_body, variables)
    text_body = render_template(template.text_body, variables)
    cta_url = render_template(template.cta_url, variables)
    html_body = branded_email_html(
        public_app_url=settings.public_app_url,
        preheader=render_template(template.preheader, variables),
        title=subject,
        body_html=content_html,
        cta_label=render_template(template.cta_label, variables),
        cta_url=cta_url,
    )
    unresolved = sorted(
        set(
            unresolved_template_variables(subject)
            + unresolved_template_variables(html_body)
            + unresolved_template_variables(text_body)
            + unresolved_template_variables(cta_url)
        )
    )
    return {
        "template_key": template.template_key,
        "subject": subject,
        "html_body": html_body,
        "text_body": text_body,
        "cta_url": cta_url,
        "unresolved_variables": unresolved,
        "idempotency_key": build_idempotency_key(
            payload.user_id,
            template.template_key,
            payload.event_id,
        ),
    }


def default_test_email_variables() -> dict[str, str]:
    return {
        "name": "QA Admin",
        "cta_url": f"{settings.public_app_url.rstrip('/')}/dashboard",
        "verify_url": f"{settings.public_app_url.rstrip('/')}/verify-email?token=test-token",
        "dashboard_url": f"{settings.public_app_url.rstrip('/')}/dashboard",
        "billing_url": f"{settings.public_app_url.rstrip('/')}/billing",
        "remaining_minutes": "25",
        "package_name": "Pro 1 Month",
        "amount": "Rp49.492",
        "order_id": "order-test123",
        "admin_notes": "Nominal transfer sudah cocok.",
    }


@router.post("/admin/test-email/render")
async def render_test_email(payload: TestEmailPayload, _: bool = Depends(require_admin_api_key)) -> dict:
    return {"data": rendered_email_payload(payload)}


@router.post("/admin/test-email/send")
async def send_test_email(payload: SendTestEmailPayload, _: bool = Depends(require_admin_api_key)) -> dict:
    rendered = rendered_email_payload(payload)
    if rendered["unresolved_variables"]:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Email template has unresolved variables",
                "unresolved_variables": rendered["unresolved_variables"],
            },
        )

    recipient_email = payload.recipient_email or settings.payment_admin_email
    if not recipient_email:
        raise HTTPException(status_code=422, detail="recipient_email or PAYMENT_ADMIN_EMAIL is required")

    result = await EmailDeliveryService().send_email(
        recipient_email=recipient_email,
        subject=rendered["subject"],
        html_body=rendered["html_body"],
        text_body=rendered["text_body"],
        idempotency_key=f"admin-test-email:{rendered['idempotency_key']}",
    )
    return {
        "data": {
            "recipient_email": recipient_email,
            "template": rendered,
            "delivery": {
                "sent": result.sent,
                "provider": result.provider,
                "provider_id": result.provider_id,
                "error": result.error,
            },
        }
    }


@router.post("/webhooks/resend")
async def resend_webhook(payload: dict) -> dict:
    return {"received": True, "provider": "resend", "event_type": payload.get("type")}
