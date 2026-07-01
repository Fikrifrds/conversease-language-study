from datetime import date, datetime, timedelta
from html import escape
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.admin_deps import AdminActor, require_admin_api_key
from app.data.seed import EMAIL_TEMPLATES, SUBSCRIPTION_PLANS, TOPUP_PACKAGES
from app.api.deps import get_current_user
from app.core.config import settings
from app.db.models import PaymentOrderModel
from app.db.session import get_db
from app.domain.email import branded_email_html, build_idempotency_key, render_template
from app.domain.payment import PaymentKind, PaymentStatus
from app.domain.users import User
from app.repositories.billing import (
    BillingRepository,
    InvalidPaymentStateError,
    ManualTransferCodeUnavailableError,
)
from app.repositories.users import UserRepository
from app.services.email_delivery import EmailDeliveryResult, EmailDeliveryService

router = APIRouter()


class CheckoutPayload(BaseModel):
    package_key: str = Field(min_length=2, max_length=64)
    payment_kind: PaymentKind


class TransferConfirmationPayload(BaseModel):
    transfer_date: date
    target_bank: str = Field(min_length=1, max_length=80)
    sender_name: Optional[str] = Field(default=None, max_length=160)
    sender_bank: Optional[str] = Field(default=None, max_length=80)
    notes: Optional[str] = Field(default=None, max_length=500)


class AdminPaymentDecisionPayload(BaseModel):
    approved_by: str = Field(default="admin", min_length=2, max_length=160)
    notes: Optional[str] = Field(default=None, max_length=1000)


class AdminPaymentNotificationPayload(BaseModel):
    requested_by: str = Field(default="admin", min_length=2, max_length=160)


def order_payload(order: PaymentOrderModel) -> dict:
    expires_at = manual_transfer_expires_at(order)
    return {
        "id": order.id,
        "user_id": order.user_id,
        "package_key": order.package_key,
        "payment_kind": order.payment_kind,
        "status": order.status,
        "amount_idr": order.amount_idr,
        "base_amount_idr": order.base_amount_idr,
        "unique_code": order.unique_code,
        "provider": order.provider,
        "provider_reference": order.provider_reference,
        "checkout_url": order.checkout_url,
        "metadata": order.metadata_json,
        "transfer_date": order.transfer_date.date().isoformat() if order.transfer_date else None,
        "expires_at": expires_at.isoformat() if expires_at else None,
        "confirmed_at": order.confirmed_at.isoformat() if order.confirmed_at else None,
        "approved_at": order.approved_at.isoformat() if order.approved_at else None,
        "approved_by": order.approved_by,
        "admin_notes": order.admin_notes,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
    }


def email_payload(result: EmailDeliveryResult) -> dict:
    return {
        "sent": result.sent,
        "provider": result.provider,
        "provider_id": result.provider_id,
        "error": result.error,
    }


def format_idr(amount: int) -> str:
    return f"Rp{amount:,.0f}".replace(",", ".")


def manual_transfer_expires_at(order: PaymentOrderModel) -> Optional[datetime]:
    if order.provider != "manual_transfer" or order.status != "pending":
        return None
    return order.created_at + timedelta(hours=settings.manual_transfer_expire_hours)


def manual_transfer_confirmation_email(current_user: User, order: PaymentOrderModel) -> dict:
    metadata = order.metadata_json or {}
    package_name = metadata.get("package_name", order.package_key)
    admin_url = (
        f"{settings.public_app_url.rstrip('/')}/admin/payments"
        f"?order_id={order.id}&unique_code={order.unique_code or ''}"
    )
    order_url = f"{settings.public_app_url.rstrip('/')}/billing?order_id={order.id}"
    safe_user_name = escape(current_user.name)
    safe_user_email = escape(current_user.email)
    safe_package_name = escape(str(package_name))
    safe_transfer_date = escape(str(metadata.get("transfer_date", "-")))
    safe_sender_name = escape(str(metadata.get("sender_name", "-")))
    safe_sender_bank = escape(str(metadata.get("sender_bank", "-")))
    safe_notes = escape(str(metadata.get("user_notes", "-")))
    detail_rows = [
        ("Order", order.id),
        ("User", f"{safe_user_name} ({safe_user_email})"),
        ("Paket", safe_package_name),
        ("Nominal transfer", format_idr(order.amount_idr)),
        ("Harga dasar", format_idr(order.base_amount_idr or order.amount_idr)),
        ("Kode unik", str(order.unique_code or "-")),
        ("Tanggal transfer", safe_transfer_date),
        ("Nama pengirim", safe_sender_name),
        ("Bank pengirim", safe_sender_bank),
        ("Catatan user", safe_notes),
    ]
    details_html = "".join(
        (
            '<tr>'
            '<td style="padding: 8px 0; color: #78716c; font-size: 13px;">'
            f"{label}</td>"
            '<td style="padding: 8px 0; color: #1c1917; font-size: 13px; font-weight: 700; text-align: right;">'
            f"{value}</td>"
            "</tr>"
        )
        for label, value in detail_rows
    )
    html_body = branded_email_html(
        public_app_url=settings.public_app_url,
        preheader=f"Transfer {format_idr(order.amount_idr)} dengan kode unik {order.unique_code}.",
        title="Konfirmasi transfer perlu dicek",
        body_html=(
            '<p style="margin: 0 0 16px;">Ada konfirmasi pembayaran manual Conversease yang perlu '
            "direview admin.</p>"
            '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" '
            'style="border-collapse: collapse; margin: 4px 0 18px;">'
            f"{details_html}</table>"
            f'<p style="margin: 0 0 12px;">Order user: <a href="{order_url}" '
            'style="color: #c2410c;">lihat billing user</a>.</p>'
        ),
        cta_label="Review Pembayaran",
        cta_url=admin_url,
        footer_note="Pastikan nominal, kode unik, tanggal, dan nama pengirim cocok dengan mutasi bank tujuan.",
    )
    text_body = "\n".join(
        [
            "Konfirmasi pembayaran manual Conversease perlu dicek.",
            f"Order: {order.id}",
            f"User: {current_user.name} ({current_user.email})",
            f"Paket: {package_name}",
            f"Nominal transfer: {format_idr(order.amount_idr)}",
            f"Harga dasar: {format_idr(order.base_amount_idr or order.amount_idr)}",
            f"Kode unik: {order.unique_code or '-'}",
            f"Tanggal transfer: {metadata.get('transfer_date', '-')}",
            f"Nama pengirim: {metadata.get('sender_name', '-')}",
            f"Bank pengirim: {metadata.get('sender_bank', '-')}",
            f"Catatan user: {metadata.get('user_notes', '-')}",
            f"Review admin: {admin_url}",
            f"Order user: {order_url}",
        ]
    )
    return {
        "recipient_email": settings.payment_admin_email,
        "subject": f"Konfirmasi transfer {format_idr(order.amount_idr)} - {order.unique_code}",
        "html_body": html_body,
        "text_body": text_body,
        "reply_to": current_user.email,
        "idempotency_key": f"payment-confirmation:{order.id}",
    }


def payment_template(template_key: str):
    template = next((item for item in EMAIL_TEMPLATES if item.template_key == template_key), None)
    if template is None:
        raise RuntimeError(f"Missing email template: {template_key}")
    return template


def manual_transfer_customer_decision_email(
    user: User,
    order: PaymentOrderModel,
    template_key: str,
    event_id: Optional[str] = None,
) -> dict:
    template = payment_template(template_key)
    package_name = str((order.metadata_json or {}).get("package_name", order.package_key))
    billing_url = f"{settings.public_app_url.rstrip('/')}/billing?order_id={order.id}"
    dashboard_url = f"{settings.public_app_url.rstrip('/')}/dashboard"
    variables = {
        "name": user.name,
        "package_name": package_name,
        "amount": format_idr(order.amount_idr),
        "order_id": order.id,
        "admin_notes": order.admin_notes or "-",
        "billing_url": billing_url,
        "dashboard_url": dashboard_url,
    }
    html_variables = {key: escape(value) for key, value in variables.items()}

    return {
        "recipient_email": user.email,
        "subject": render_template(template.subject, variables),
        "html_body": branded_email_html(
            public_app_url=settings.public_app_url,
            preheader=render_template(template.preheader, variables),
            title=render_template(template.subject, variables),
            body_html=render_template(template.html_body, html_variables),
            cta_label=render_template(template.cta_label, variables),
            cta_url=render_template(template.cta_url, variables),
        ),
        "text_body": render_template(template.text_body, variables),
        "reply_to": settings.email_reply_to or settings.payment_admin_email,
        "idempotency_key": build_idempotency_key(user.id, template.template_key, event_id or order.id),
    }


def manual_transfer_decision_template_key(order: PaymentOrderModel) -> Optional[str]:
    if order.status == PaymentStatus.SUCCESS.value:
        return "payment_manual_approved"
    if order.status == PaymentStatus.FAILED.value:
        return "payment_manual_rejected"
    return None


async def send_and_record_manual_transfer_customer_decision_email(
    db: Session,
    order: PaymentOrderModel,
    template_key: str,
    trigger: str,
) -> EmailDeliveryResult:
    user = UserRepository(db).get_by_id(order.user_id)
    if user is None:
        return EmailDeliveryResult(
            sent=False,
            provider="internal",
            error="Payment order user was not found",
        )

    metadata = order.metadata_json or {}
    previous_delivery = metadata.get("customer_decision_email")
    previous_attempt_count = (
        int(previous_delivery.get("attempt_count", 0))
        if isinstance(previous_delivery, dict)
        else 0
    )
    attempt_count = previous_attempt_count + 1
    event_id = order.id if trigger == "decision" else f"{order.id}:{trigger}:{attempt_count}"
    email = manual_transfer_customer_decision_email(user, order, template_key, event_id=event_id)
    result = await EmailDeliveryService().send_email(**email)
    now = datetime.utcnow()
    order.metadata_json = {
        **metadata,
        "customer_decision_email": {
            "template_key": template_key,
            "recipient_email": user.email,
            "sent": result.sent,
            "provider": result.provider,
            "provider_id": result.provider_id,
            "error": result.error,
            "attempt_count": attempt_count,
            "attempted_at": now.isoformat(),
            "trigger": trigger,
        },
    }
    order.updated_at = now
    db.add(order)
    db.commit()
    return result


@router.get("/plans")
async def list_plans() -> dict:
    return {"data": SUBSCRIPTION_PLANS}


@router.get("/topups")
async def list_topups() -> dict:
    return {"data": TOPUP_PACKAGES}


@router.get("/me/billing/access")
async def get_my_billing_access(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    access = BillingRepository(db).access_summary(current_user.id)
    return {"data": access}


@router.post("/billing/checkout")
async def create_checkout(
    payload: CheckoutPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if payload.package_key == "free":
        raise HTTPException(status_code=422, detail="Free plan does not require checkout")

    try:
        order = BillingRepository(db).create_manual_transfer_order(
            user_id=current_user.id,
            package_key=payload.package_key,
            payment_kind=payload.payment_kind,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Package not found") from exc
    except ManualTransferCodeUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="Manual transfer unique codes are temporarily unavailable",
        ) from exc

    return {"data": order_payload(order)}


@router.get("/billing/checkout/{order_id}")
async def get_checkout_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    try:
        order = BillingRepository(db).get_user_manual_payment_order(
            user_id=current_user.id,
            order_id=order_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc

    return {"data": order_payload(order)}


@router.post("/billing/checkout/{order_id}/confirm-transfer")
async def confirm_manual_transfer(
    order_id: str,
    payload: TransferConfirmationPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    repository = BillingRepository(db)

    try:
        order = repository.confirm_manual_transfer(
            user_id=current_user.id,
            order_id=order_id,
            transfer_date=payload.transfer_date,
            sender_name=payload.sender_name,
            sender_bank=payload.sender_bank,
            target_bank=payload.target_bank,
            notes=payload.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc
    except InvalidPaymentStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    email = manual_transfer_confirmation_email(current_user, order)
    email_result = await EmailDeliveryService().send_email(**email)

    return {"data": {"order": order_payload(order), "email": email_payload(email_result)}}


@router.post("/billing/checkout/{order_id}/sandbox-complete")
async def complete_sandbox_checkout(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if settings.is_production:
        raise HTTPException(status_code=404, detail="Sandbox checkout is disabled")

    try:
        order = BillingRepository(db).complete_sandbox_order(
            user_id=current_user.id,
            order_id=order_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc
    except InvalidPaymentStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return {"data": order_payload(order)}


@router.post("/billing/sandbox-activate")
async def activate_sandbox_package(
    payload: CheckoutPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if settings.is_production:
        raise HTTPException(status_code=404, detail="Sandbox activation is disabled")

    if payload.package_key == "free":
        raise HTTPException(status_code=422, detail="Free plan is already available")

    try:
        order = BillingRepository(db).activate_package_now(
            user_id=current_user.id,
            package_key=payload.package_key,
            payment_kind=payload.payment_kind,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Package not found") from exc

    return {
        "data": {
            "order": order_payload(order),
            "access": BillingRepository(db).access_summary(current_user.id),
        }
    }


@router.get("/admin/payment-orders")
async def list_admin_payment_orders(
    status: Optional[str] = Query(default=None, max_length=32),
    unique_code: Optional[int] = Query(default=None, ge=1, le=999),
    limit: int = Query(default=50, ge=1, le=100),
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    orders = BillingRepository(db).list_payment_orders(
        status=status,
        unique_code=unique_code,
        limit=limit,
    )
    return {"data": [order_payload(order) for order in orders]}


@router.get("/admin/payment-orders/{order_id}")
async def get_admin_payment_order(
    order_id: str,
    _: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        order = BillingRepository(db).get_manual_payment_order(order_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc

    return {"data": order_payload(order)}


@router.post("/admin/payment-orders/{order_id}/approve")
async def approve_admin_payment_order(
    order_id: str,
    payload: AdminPaymentDecisionPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    repository = BillingRepository(db)
    try:
        current_order = repository.get_manual_payment_order(order_id)
        previous_status = current_order.status
        order = repository.approve_manual_order(
            order_id=order_id,
            approved_by=admin_display_name(payload.approved_by, admin),
            notes=payload.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc
    except InvalidPaymentStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if previous_status != PaymentStatus.SUCCESS.value and order.status == PaymentStatus.SUCCESS.value:
        await send_and_record_manual_transfer_customer_decision_email(
            db,
            order,
            "payment_manual_approved",
            trigger="decision",
        )

    return {"data": order_payload(order)}


@router.post("/admin/payment-orders/{order_id}/reject")
async def reject_admin_payment_order(
    order_id: str,
    payload: AdminPaymentDecisionPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    repository = BillingRepository(db)
    try:
        current_order = repository.get_manual_payment_order(order_id)
        previous_status = current_order.status
        order = repository.reject_manual_order(
            order_id=order_id,
            approved_by=admin_display_name(payload.approved_by, admin),
            notes=payload.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc
    except InvalidPaymentStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if previous_status != PaymentStatus.FAILED.value and order.status == PaymentStatus.FAILED.value:
        await send_and_record_manual_transfer_customer_decision_email(
            db,
            order,
            "payment_manual_rejected",
            trigger="decision",
        )

    return {"data": order_payload(order)}


@router.post("/admin/payment-orders/{order_id}/resend-decision-email")
async def resend_admin_payment_decision_email(
    order_id: str,
    payload: AdminPaymentNotificationPayload,
    admin: AdminActor = Depends(require_admin_api_key),
    db: Session = Depends(get_db),
) -> dict:
    try:
        order = BillingRepository(db).get_manual_payment_order(order_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Payment order not found") from exc

    template_key = manual_transfer_decision_template_key(order)
    if template_key is None:
        raise HTTPException(
            status_code=409,
            detail="Payment order must be approved or rejected before sending a decision email",
        )

    requester_name = admin_display_name(payload.requested_by, admin)
    requester = "-".join(requester_name.strip().lower().split()) or "admin"
    result = await send_and_record_manual_transfer_customer_decision_email(
        db,
        order,
        template_key,
        trigger=f"resend:{requester}",
    )

    return {"data": {"order": order_payload(order), "email": email_payload(result)}}


def admin_display_name(value: Optional[str], admin: AdminActor) -> str:
    clean_value = (value or "").strip()
    if clean_value and clean_value.lower() != "admin":
        return clean_value
    return admin.display_name
