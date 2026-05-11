"""Authorization queue for actions that must not be performed automatically."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class AuthorizationItem:
    action: str
    reason: str
    safe_fallback: str
    status: str = "pending_user_authorization"


def build_authorization_item(action: str, reason: str, safe_fallback: str) -> dict[str, str]:
    return asdict(AuthorizationItem(action=action, reason=reason, safe_fallback=safe_fallback))
