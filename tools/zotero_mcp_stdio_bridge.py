"""Bridge Zotero FastMCP stdio JSON-lines to clients that use framed stdio.

The bundled zotero-mcp executable speaks newline-delimited JSON-RPC on stdout.
Some MCP clients use LSP-style ``Content-Length`` frames for stdio. This
wrapper accepts either client framing mode, forwards JSON messages to
zotero-mcp as newline-delimited JSON, and returns responses in the same mode
the client used.

It does not call any Zotero tool by itself.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import threading
from typing import BinaryIO, Literal


ZOTERO_MCP_EXE = r"C:\Users\Administrator\codex-uv-bin\zotero-mcp.exe"
PROJECT_ENV_FILE = pathlib.Path(".codex") / "zotero_mcp.env"


def _load_project_env(base_env: dict[str, str], cwd: pathlib.Path) -> dict[str, str]:
    """Load project-local MCP env without printing or logging secrets."""
    env = base_env.copy()
    env_file = cwd / PROJECT_ENV_FILE
    if not env_file.exists():
        return env

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            env[key] = value
    return env


def _write_stderr(data: bytes) -> None:
    try:
        sys.stderr.buffer.write(data)
        sys.stderr.buffer.flush()
    except BrokenPipeError:
        pass


def _read_framed(first_header_line: bytes, stream: BinaryIO) -> bytes | None:
    headers = [first_header_line]
    while True:
        line = stream.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        headers.append(line)

    content_length = None
    for header in headers:
        if header.lower().startswith(b"content-length:"):
            content_length = int(header.split(b":", 1)[1].strip())
            break
    if content_length is None:
        return None

    body = stream.read(content_length)
    if len(body) != content_length:
        return None
    return body


def _write_client_message(mode: Literal["framed", "newline"], payload: bytes) -> None:
    if mode == "framed":
        sys.stdout.buffer.write(b"Content-Length: ")
        sys.stdout.buffer.write(str(len(payload)).encode("ascii"))
        sys.stdout.buffer.write(b"\r\n\r\n")
        sys.stdout.buffer.write(payload)
    else:
        sys.stdout.buffer.write(payload.rstrip(b"\r\n") + b"\n")
    sys.stdout.buffer.flush()


def main() -> int:
    cwd = pathlib.Path.cwd()
    child_env = _load_project_env(os.environ, cwd)
    child = subprocess.Popen(
        [ZOTERO_MCP_EXE, "serve", "--transport", "stdio"],
        cwd=str(cwd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=child_env,
    )

    assert child.stdin is not None
    assert child.stdout is not None
    assert child.stderr is not None

    mode_holder: dict[str, Literal["framed", "newline"] | None] = {"mode": None}

    def relay_child_stdout() -> None:
        while True:
            line = child.stdout.readline()
            if not line:
                break
            mode = mode_holder.get("mode") or "newline"
            _write_client_message(mode, line.rstrip(b"\r\n"))

    def relay_child_stderr() -> None:
        while True:
            chunk = child.stderr.readline()
            if not chunk:
                break
            _write_stderr(chunk)

    threading.Thread(target=relay_child_stdout, daemon=True).start()
    threading.Thread(target=relay_child_stderr, daemon=True).start()

    try:
        while True:
            first = sys.stdin.buffer.readline()
            if not first:
                break

            if first.lower().startswith(b"content-length:"):
                mode_holder["mode"] = "framed"
                payload = _read_framed(first, sys.stdin.buffer)
                if payload is None:
                    break
                child.stdin.write(payload.rstrip(b"\r\n") + b"\n")
            else:
                mode_holder["mode"] = "newline"
                child.stdin.write(first.rstrip(b"\r\n") + b"\n")
            child.stdin.flush()
    finally:
        try:
            child.stdin.close()
        except Exception:
            pass
        try:
            child.terminate()
            child.wait(timeout=3)
        except Exception:
            try:
                child.kill()
            except Exception:
                pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
