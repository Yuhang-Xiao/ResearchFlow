"""Persist model decisions as JSON."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Any


def write_model_decision(decision: dict[str, Any], path: str | Path) -> dict[str, str]:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(decision, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "ok", "path": str(output)}
