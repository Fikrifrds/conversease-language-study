from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Optional
from urllib.parse import urlencode

import httpx
from jose import JWTError, jwt

from app.core.config import settings
from app.repositories.users import normalize_email


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_ISSUERS = {"https://accounts.google.com", "accounts.google.com"}
GOOGLE_STATE_TYPE = "google_oauth_state"


class GoogleOAuthError(Exception):
    pass


@dataclass(frozen=True)
class GoogleOAuthState:
    next_path: str


@dataclass(frozen=True)
class GoogleProfile:
    email: str
    name: str
    email_verified: bool
    subject: str


def google_oauth_enabled() -> bool:
    return bool(settings.google_oauth_client_id and settings.google_oauth_client_secret)


def google_redirect_uri() -> str:
    if settings.google_oauth_redirect_uri:
        return settings.google_oauth_redirect_uri
    return f"{settings.api_base_url.rstrip('/')}/api/auth/google/callback"


def safe_next_path(value: Optional[str]) -> str:
    if value and value.startswith("/") and not value.startswith("//"):
        return value
    return "/dashboard"


def create_google_oauth_state(next_path: Optional[str]) -> str:
    payload = {
        "type": GOOGLE_STATE_TYPE,
        "next": safe_next_path(next_path),
        "nonce": token_urlsafe(12),
        "exp": datetime.utcnow() + timedelta(minutes=10),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_google_oauth_state(state: str) -> GoogleOAuthState:
    try:
        payload = jwt.decode(state, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise GoogleOAuthError("invalid_oauth_state") from exc

    if payload.get("type") != GOOGLE_STATE_TYPE:
        raise GoogleOAuthError("invalid_oauth_state")

    return GoogleOAuthState(next_path=safe_next_path(payload.get("next")))


def google_authorization_url(state: str) -> str:
    query = urlencode(
        {
            "client_id": settings.google_oauth_client_id,
            "redirect_uri": google_redirect_uri(),
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "online",
            "prompt": "select_account",
        }
    )
    return f"{GOOGLE_AUTH_URL}?{query}"


async def exchange_google_code(code: str) -> GoogleProfile:
    if not google_oauth_enabled():
        raise GoogleOAuthError("google_oauth_not_configured")

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.google_oauth_client_id,
                    "client_secret": settings.google_oauth_client_secret,
                    "redirect_uri": google_redirect_uri(),
                    "grant_type": "authorization_code",
                },
            )
            token_response.raise_for_status()
            token_payload = token_response.json()
        except httpx.HTTPError as exc:
            raise GoogleOAuthError("google_token_exchange_failed") from exc

    access_token = token_payload.get("access_token")
    id_token = token_payload.get("id_token")
    if isinstance(id_token, str) and id_token:
        try:
            return await verify_google_id_token(id_token)
        except GoogleOAuthError:
            if isinstance(access_token, str) and access_token:
                return await fetch_google_userinfo(access_token)
            raise

    if isinstance(access_token, str) and access_token:
        return await fetch_google_userinfo(access_token)

    raise GoogleOAuthError("missing_google_profile_token")


async def verify_google_id_token(id_token: str) -> GoogleProfile:
    try:
        header = jwt.get_unverified_header(id_token)
    except JWTError as exc:
        raise GoogleOAuthError("invalid_google_id_token") from exc

    kid = header.get("kid")
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            jwks_response = await client.get(GOOGLE_JWKS_URL)
            jwks_response.raise_for_status()
            jwks = jwks_response.json()
        except httpx.HTTPError as exc:
            raise GoogleOAuthError("google_jwks_fetch_failed") from exc

    key = next((item for item in jwks.get("keys", []) if item.get("kid") == kid), None)
    if key is None:
        raise GoogleOAuthError("google_jwk_not_found")

    try:
        payload = jwt.decode(
            id_token,
            key,
            algorithms=["RS256"],
            audience=settings.google_oauth_client_id,
        )
    except JWTError as exc:
        raise GoogleOAuthError("invalid_google_id_token") from exc

    if payload.get("iss") not in GOOGLE_ISSUERS:
        raise GoogleOAuthError("invalid_google_issuer")

    return google_profile_from_claims(payload)


async def fetch_google_userinfo(access_token: str) -> GoogleProfile:
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            userinfo_response.raise_for_status()
            payload = userinfo_response.json()
        except httpx.HTTPError as exc:
            raise GoogleOAuthError("google_userinfo_fetch_failed") from exc

    return google_profile_from_claims(payload)


def google_profile_from_claims(payload: dict) -> GoogleProfile:
    email = payload.get("email")
    subject = payload.get("sub")
    if not isinstance(email, str) or not isinstance(subject, str):
        raise GoogleOAuthError("missing_google_profile")

    email_verified_claim = payload.get("email_verified")
    email_verified = email_verified_claim is True or str(email_verified_claim).lower() == "true"

    return GoogleProfile(
        email=normalize_email(email),
        name=str(payload.get("name") or email.split("@")[0]),
        email_verified=email_verified,
        subject=subject,
    )
