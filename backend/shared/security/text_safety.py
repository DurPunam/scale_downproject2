from __future__ import annotations

import re
from typing import Tuple

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s\-\(\)]{7,}\d")
CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,16}\b")


def redact_pii(text: str) -> Tuple[str, bool]:
    redacted = text
    redacted, email_hits = EMAIL_RE.subn("[REDACTED_EMAIL]", redacted)
    redacted, phone_hits = PHONE_RE.subn("[REDACTED_PHONE]", redacted)
    redacted, card_hits = CARD_RE.subn("[REDACTED_CARD]", redacted)
    changed = any([email_hits, phone_hits, card_hits])
    return redacted, changed


def detect_prompt_injection(text: str) -> bool:
    patterns = [
        "ignore previous instructions",
        "system prompt",
        "developer message",
        "exfiltrate",
        "override safety",
    ]
    lowered = text.lower()
    return any(p in lowered for p in patterns)
