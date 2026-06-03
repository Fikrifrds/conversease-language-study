from __future__ import annotations

import hmac
from typing import Optional

from fastapi import Header, HTTPException

from app.core.config import settings


def require_admin_api_key(x_admin_api_key: Optional[str] = Header(default=None)) -> bool:
    if not settings.payment_admin_api_key:
        raise HTTPException(status_code=503, detail="Admin API key is not configured")

    if not x_admin_api_key or not hmac.compare_digest(
        x_admin_api_key,
        settings.payment_admin_api_key,
    ):
        raise HTTPException(status_code=401, detail="Invalid admin key")

    return True
