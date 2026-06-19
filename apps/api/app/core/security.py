from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Precomputed hash with the same scheme/cost as real ones. Verifying against it
# for a non-existent account makes login take the same time as for a real one,
# so response timing can't reveal which emails are registered.
_dummy_password_hash = password_context.hash("conversease-timing-equalizer")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def waste_password_verification() -> None:
    """Run a hash verification and discard the result, to equalize login timing
    when the account does not exist."""
    password_context.verify("conversease-timing-equalizer", _dummy_password_hash)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expires_at = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("invalid_token") from exc

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise ValueError("invalid_token_subject")
    return subject
