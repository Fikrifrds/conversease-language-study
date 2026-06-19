from datetime import timedelta
import logging
import re
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from urllib.parse import urlencode

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.rate_limit import login_attempts, rate_limiter
from app.core.security import create_access_token
from app.db.session import get_db
from app.domain.users import User, name_looks_suspicious
from app.repositories.billing import BillingRepository
from app.repositories.auth_tokens import (
    EMAIL_VERIFICATION_TOKEN,
    GOOGLE_LOGIN_TOKEN,
    PASSWORD_RESET_TOKEN,
    AuthTokenRepository,
    InvalidAuthTokenError,
)
from app.repositories.users import UserRepository, normalize_email
from app.services.auth_email import AuthEmailService
from app.services.google_oauth import (
    GoogleOAuthError,
    create_google_oauth_state,
    decode_google_oauth_state,
    exchange_google_code,
    google_authorization_url,
    google_oauth_enabled,
    safe_next_path,
)


router = APIRouter()
logger = logging.getLogger(__name__)


class AuthUserPayload(BaseModel):
    id: str
    name: str
    email: str
    role: str
    email_verified_at: Optional[str] = None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserPayload


class RegisterPayload(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8, max_length=128)


class LoginPayload(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8, max_length=128)


class ForgotPasswordPayload(BaseModel):
    email: str = Field(min_length=5, max_length=320)


class ResetPasswordPayload(BaseModel):
    token: str = Field(min_length=20, max_length=256)
    password: str = Field(min_length=8, max_length=128)


class VerifyEmailPayload(BaseModel):
    token: str = Field(min_length=20, max_length=256)


class GoogleSessionPayload(BaseModel):
    token: str = Field(min_length=20, max_length=256)


def delivery_payload(result) -> dict:
    return {
        "sent": result.sent,
        "provider": result.provider,
        "error": result.error,
        "url": result.url,
    }


def user_payload(user: User) -> AuthUserPayload:
    return AuthUserPayload(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        email_verified_at=user.email_verified_at.isoformat() if user.email_verified_at else None,
    )


def auth_response(user: User) -> AuthResponse:
    return AuthResponse(access_token=create_access_token(user.id), user=user_payload(user))


# Pragmatic email check: a single local part and domain made of standard,
# unambiguous characters. Rejects the SQL/script payloads (quotes, parentheses,
# pipes, spaces, semicolons) seen in registration spam so they never reach the DB.
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?)+$"
)


def validate_email(email: str) -> str:
    normalized = normalize_email(email)
    if len(normalized) > 320 or not EMAIL_PATTERN.fullmatch(normalized):
        raise HTTPException(status_code=422, detail="Valid email is required")
    return normalized


def guard_email_recipient(email: str) -> None:
    """Cap how many transactional emails one address can receive in the window,
    so abusing forgot-password / verification can't email-bomb a victim even
    from many IPs (the per-IP limiter alone doesn't stop that).
    """
    if not settings.rate_limit_enabled:
        return
    remaining = rate_limiter.hit(
        f"email-recipient:{email}",
        limit=settings.email_recipient_rate_limit_requests,
        window_seconds=settings.email_recipient_rate_limit_window_seconds,
    )
    if remaining < 0:
        raise HTTPException(
            status_code=429,
            detail="Too many email requests for this address. Please try again later.",
        )


@router.post("/auth/register", response_model=AuthResponse)
async def register(payload: RegisterPayload, db: Session = Depends(get_db)) -> AuthResponse:
    email = validate_email(payload.email)

    # Bots register with stolen-email combo lists under random names like
    # "mMFlPCiwwJYwWfsti". Reject those up front so they never reach the DB,
    # using the same heuristic the admin user list flags as suspicious.
    if name_looks_suspicious(payload.name, email):
        raise HTTPException(status_code=422, detail="Please enter your real name")

    guard_email_recipient(email)
    repository = UserRepository(db)

    if repository.get_by_email(email):
        raise HTTPException(status_code=409, detail="Email already registered")

    try:
        user = repository.create_user(name=payload.name, email=email, password=payload.password)
        BillingRepository(db).ensure_free_access(user.id)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from exc

    await send_verification_email(user, db)
    return auth_response(user)


@router.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginPayload, db: Session = Depends(get_db)) -> AuthResponse:
    email = validate_email(payload.email)

    if settings.rate_limit_enabled and login_attempts.is_locked(
        email,
        max_attempts=settings.login_max_failed_attempts,
        window_seconds=settings.login_lockout_window_seconds,
    ):
        raise HTTPException(
            status_code=429,
            detail="Too many failed login attempts. Please try again later.",
        )

    user = UserRepository(db).authenticate(email=email, password=payload.password)

    if user is None:
        if settings.rate_limit_enabled:
            login_attempts.register_failure(email, window_seconds=settings.login_lockout_window_seconds)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if settings.rate_limit_enabled:
        login_attempts.reset_key(email)
    return auth_response(user)


@router.get("/auth/google/status")
async def google_status() -> dict:
    return {"data": {"enabled": google_oauth_enabled()}}


@router.get("/auth/google/login")
async def google_login(next: str = Query(default="/dashboard")):
    next_path = safe_next_path(next)

    if not google_oauth_enabled():
        return redirect_to_app("/login", google_error="not_configured", next=next_path)

    state = create_google_oauth_state(next_path)
    return RedirectResponse(google_authorization_url(state), status_code=302)


@router.get("/auth/google/callback")
async def google_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if error:
        logger.warning("Google OAuth provider returned error: %s", error)
        return redirect_to_app("/login", google_error=error)

    if not code or not state:
        return redirect_to_app("/login", google_error="missing_google_callback")

    try:
        decoded_state = decode_google_oauth_state(state)
        google_profile = await exchange_google_code(code)
        user = UserRepository(db).get_or_create_google_user(
            name=google_profile.name,
            email=google_profile.email,
            email_verified=google_profile.email_verified,
        )
        BillingRepository(db).ensure_free_access(user.id)
        login_token = AuthTokenRepository(db).create_token(
            user_id=user.id,
            token_type=GOOGLE_LOGIN_TOKEN,
            expires_delta=timedelta(minutes=5),
        )
    except GoogleOAuthError as exc:
        logger.warning("Google OAuth callback failed: %s", exc)
        return redirect_to_app("/login", google_error="google_login_failed")

    return redirect_to_app(
        "/auth/google/callback",
        token=login_token.token,
        next=decoded_state.next_path,
    )


@router.post("/auth/google/session", response_model=AuthResponse)
async def google_session(payload: GoogleSessionPayload, db: Session = Depends(get_db)) -> AuthResponse:
    try:
        token = AuthTokenRepository(db).consume_token(payload.token, GOOGLE_LOGIN_TOKEN)
        user = UserRepository(db).get_by_id(token.user_id)
    except InvalidAuthTokenError as exc:
        raise HTTPException(status_code=422, detail="Invalid or expired Google login token") from exc

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return auth_response(user)


@router.get("/auth/me", response_model=AuthUserPayload)
async def me(current_user: User = Depends(get_current_user)) -> AuthUserPayload:
    return user_payload(current_user)


@router.post("/auth/request-email-verification")
async def request_email_verification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if current_user.email_verified_at:
        return {"data": {"already_verified": True, "email": current_user.email}}

    guard_email_recipient(current_user.email)
    result = await send_verification_email(current_user, db)
    return {
        "data": {
            "already_verified": False,
            "email": current_user.email,
            "delivery": delivery_payload(result),
        }
    }


@router.post("/auth/verify-email")
async def verify_email(payload: VerifyEmailPayload, db: Session = Depends(get_db)) -> dict:
    try:
        token = AuthTokenRepository(db).consume_token(payload.token, EMAIL_VERIFICATION_TOKEN)
        user = UserRepository(db).mark_email_verified(token.user_id)
    except InvalidAuthTokenError as exc:
        raise HTTPException(status_code=422, detail="Invalid or expired verification token") from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc

    return {"data": {"verified": True, "user": user_payload(user)}}


@router.post("/auth/forgot-password")
async def forgot_password(payload: ForgotPasswordPayload, db: Session = Depends(get_db)) -> dict:
    email = validate_email(payload.email)
    guard_email_recipient(email)
    user = UserRepository(db).get_by_email(email)
    delivery = None

    if user is not None:
        token = AuthTokenRepository(db).create_token(
            user_id=user.id,
            token_type=PASSWORD_RESET_TOKEN,
            expires_delta=timedelta(minutes=settings.password_reset_token_expire_minutes),
        )
        delivery = await AuthEmailService().send_password_reset_email(user, token.token)

    return {
        "data": {
            "requested": True,
            "delivery": delivery_payload(delivery) if delivery and not settings.is_production else None,
        }
    }


@router.post("/auth/reset-password")
async def reset_password(payload: ResetPasswordPayload, db: Session = Depends(get_db)) -> dict:
    try:
        token = AuthTokenRepository(db).consume_token(payload.token, PASSWORD_RESET_TOKEN)
        user = UserRepository(db).update_password(token.user_id, payload.password)
    except InvalidAuthTokenError as exc:
        raise HTTPException(status_code=422, detail="Invalid or expired reset token") from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc

    return {"data": {"reset": True, "user": user_payload(user)}}


async def send_verification_email(user: User, db: Session):
    token = AuthTokenRepository(db).create_token(
        user_id=user.id,
        token_type=EMAIL_VERIFICATION_TOKEN,
        expires_delta=timedelta(hours=settings.email_verification_token_expire_hours),
    )
    return await AuthEmailService().send_verification_email(user, token.token)


def redirect_to_app(path: str, **params: str) -> RedirectResponse:
    query = urlencode({key: value for key, value in params.items() if value})
    separator = "&" if "?" in path else "?"
    target_path = f"{path}{separator}{query}" if query else path
    target_url = f"{settings.public_app_url.rstrip('/')}{target_path}"
    return RedirectResponse(target_url, status_code=302)
