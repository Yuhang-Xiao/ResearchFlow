"""Readiness checks for Zotero MCP/API writeback.

This module does not print or persist secrets. It only reports whether relevant
configuration and runtime prerequisites are present.
"""

from __future__ import annotations

from pathlib import Path
import json
import os
import re
import socket
import subprocess
from typing import Any
from urllib import request, error


DEFAULT_MCP_EXE = Path(r"C:\Users\Administrator\codex-uv-bin\zotero-mcp.exe")


def _port_open(host: str = "127.0.0.1", port: int = 23119, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _zotero_process_running() -> bool:
    try:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Process | Where-Object { $_.ProcessName -like '*zotero*' } | Select-Object -First 1 -ExpandProperty ProcessName"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return bool(completed.stdout.strip())
    except Exception:
        return False


def _config_env_value(config_text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}\s*=\s*['\"]([^'\"]+)['\"]", config_text, flags=re.MULTILINE)
    return match.group(1) if match else None


def _collection_readback_status(config_text: str, port_open: bool) -> dict[str, Any]:
    if not port_open:
        return {"status": "skipped", "reason": "Zotero local API port is not open."}
    library_id = os.environ.get("ZOTERO_LIBRARY_ID") or _config_env_value(config_text, "ZOTERO_LIBRARY_ID")
    library_type = os.environ.get("ZOTERO_LIBRARY_TYPE") or _config_env_value(config_text, "ZOTERO_LIBRARY_TYPE") or "user"
    if not library_id:
        return {"status": "skipped", "reason": "No Zotero library id configured in environment or project config."}
    path_part = f"users/{library_id}" if library_type == "user" else f"groups/{library_id}"
    url = f"http://localhost:23119/api/{path_part}/collections?start=0&limit=1&format=json&locale=en-US"
    headers = {}
    api_key = os.environ.get("ZOTERO_API_KEY")
    if api_key:
        headers["Zotero-API-Key"] = api_key
    try:
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=5) as response:
            body = response.read(4096).decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body.strip() else []
            collection_count = len(parsed) if isinstance(parsed, list) else None
        except json.JSONDecodeError:
            collection_count = None
        return {"status": "ok", "reason": "Collection endpoint responded.", "collection_count_sample": collection_count}
    except error.HTTPError as exc:
        return {"status": "failed", "reason": f"HTTP {exc.code} from collection readback endpoint."}
    except Exception as exc:
        return {"status": "failed", "reason": str(exc)}


def check_zotero_mcp_readiness(config_path: str | Path = ".codex/config.toml") -> dict[str, Any]:
    """Return a secret-safe Zotero MCP readiness summary."""

    config = Path(config_path)
    text = config.read_text(encoding="utf-8", errors="ignore") if config.exists() else ""
    port_open = _port_open()
    readback = _collection_readback_status(text, port_open)
    writeback_blocked_reason = ""
    if readback.get("status") != "ok":
        writeback_blocked_reason = f"Zotero writeback blocked until collection readback passes: {readback.get('reason')}"
    return {
        "workflow_config_exists": config.exists(),
        "workflow_config_has_zotero_mcp": "[mcp_servers.zotero]" in text,
        "mcp_executable_exists": DEFAULT_MCP_EXE.exists(),
        "zotero_desktop_process_running": _zotero_process_running(),
        "zotero_local_api_port_open": port_open,
        "zotero_api_key_env_present": bool(os.environ.get("ZOTERO_API_KEY")),
        "zotero_library_id_env_present": bool(os.environ.get("ZOTERO_LIBRARY_ID") or _config_env_value(text, "ZOTERO_LIBRARY_ID")),
        "zotero_collection_readback": readback,
        "safe_to_attempt_mcp_write_after_restart": config.exists() and "[mcp_servers.zotero]" in text and DEFAULT_MCP_EXE.exists() and readback.get("status") == "ok",
        "writeback_blocked_reason": writeback_blocked_reason,
        "secret_policy": "API keys are not read, printed, or stored by this check.",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(check_zotero_mcp_readiness(), ensure_ascii=False, indent=2))
