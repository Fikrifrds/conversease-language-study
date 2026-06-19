from dataclasses import dataclass
from datetime import datetime
import re
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

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


def _camelcase_humps(value: str) -> int:
    return sum(1 for prev, curr in zip(value, value[1:]) if prev.islower() and curr.isupper())


def name_looks_suspicious(name: str, email: str) -> bool:
    """Flag bot-generated display names (random strings, gibberish, name==email
    local part). Shared by registration (to block) and the admin user list (to
    surface), so prevention and detection never drift apart.
    """
    name = (name or "").strip()
    email_local_part = (email or "").split("@", 1)[0].strip().lower()

    # A name with no alphanumeric characters at all is empty or symbol-only.
    if not any(char.isalnum() for char in name):
        return True

    # The gibberish rules below (vowels, uppercase ratio, camelCase humps) are
    # specific to the Latin alphabet. Names in other scripts (Arabic, Chinese,
    # Cyrillic, ...) are legitimate for a language-learning app, so don't judge
    # them with Latin-only signals.
    if any(char.isalpha() and not char.isascii() for char in name):
        return False

    collapsed = re.sub(r"[^A-Za-z0-9]", "", name)
    letters = [char for char in collapsed if char.isalpha()]
    digits = sum(1 for char in collapsed if char.isdigit())
    uppercase = sum(1 for char in collapsed if char.isupper())
    vowel_count = sum(1 for char in letters if char.lower() in {"a", "e", "i", "o", "u"})

    if digits >= 3:
        return True
    if len(collapsed) >= 12 and " " not in name and collapsed.lower() == email_local_part:
        return True
    if len(collapsed) >= 12 and " " not in name and uppercase >= max(6, len(collapsed) // 2):
        return True
    if len(letters) >= 8 and vowel_count <= 1:
        return True
    # Random camelCase names (e.g. "gnGtDYnbGqUCvugrLa") have many lowercase->
    # uppercase humps. Real names cap out at one ("McDonald", "JoAnne").
    if " " not in name and _camelcase_humps(collapsed) >= 3:
        return True
    return False
