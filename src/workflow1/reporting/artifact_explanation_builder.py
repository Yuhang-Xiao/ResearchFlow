"""Safe scaffold for reporting/artifact_explanation_builder.py.

This module is intentionally lightweight. It records metadata, planning
decisions, quality gates, and approval requirements without executing
external code or formal DQN training.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def build_record(item: str, source: str = "workflow1", status: str = "metadata_only", **extra: Any) -> dict[str, Any]:
    """Return a structured audit/planning record."""

    record: dict[str, Any] = {
        "item": item,
        "source": source,
        "status": status,
        "experimental_boundary": "not_formal_unless_verified",
        "approval_required_for_high_risk_actions": True,
    }
    record.update(extra)
    return record


def write_markdown(path: str | Path, title: str, records: list[dict[str, Any]]) -> Path:
    """Write a compact Chinese-first markdown summary."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", "状态：safe metadata-only scaffold。", ""]
    for row in records:
        lines.append(f"- `{row.get('item', 'unknown')}`：{row.get('status', 'metadata_only')}；边界：{row.get('experimental_boundary')}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
