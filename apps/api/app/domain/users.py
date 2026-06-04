from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str
    email_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    role: str = "student"
