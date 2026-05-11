"""Safety guard for external references and actions."""

from __future__ import annotations


BLOCKED_EXTERNAL_ACTIONS = {
    "install_dependency",
    "clone_and_run_unknown_code",
    "write_zotero_sqlite",
    "use_api_key",
    "download_large_model_or_dataset",
}


def check_external_action(action: str) -> dict[str, object]:
    blocked = action in BLOCKED_EXTERNAL_ACTIONS
    return {
        "action": action,
        "allowed": not blocked,
        "requires_human_authorization": blocked,
        "policy": "External code and services are read-only references unless explicitly authorized.",
    }
