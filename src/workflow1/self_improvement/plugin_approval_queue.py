from __future__ import annotations

def default_queue() -> list[dict[str, str]]:
    return [
        {"candidate": "Zotero MCP", "reason": "MCP install and Zotero database access", "status": "waiting_user_confirmation"},
        {"candidate": "AutoML/data-science agents", "reason": "External dependency/code execution risk", "status": "waiting_user_confirmation"},
    ]
