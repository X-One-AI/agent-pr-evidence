from __future__ import annotations

import re

_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*=\s*[^\\s]+"),
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
)


def redact(text: str) -> str:
    redacted = text
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub(lambda match: _replacement(match.group(0)), redacted)
    return redacted


def _replacement(value: str) -> str:
    if "=" in value:
        key = value.split("=", 1)[0]
        return f"{key}=<redacted>"
    return "<redacted-secret>"
