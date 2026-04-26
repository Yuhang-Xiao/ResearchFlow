"""Lightweight chart QA and data-source consistency checks."""
from __future__ import annotations

from pathlib import Path


def audit_chart_file(chart_path: str | Path, data_path: str | Path | None = None) -> dict:
    chart = Path(chart_path)
    exists = chart.exists()
    size = chart.stat().st_size if exists else 0
    status = "pass" if exists and size > 512 else "fail_blank_or_missing"
    return {
        "chart_path": str(chart),
        "data_path": str(data_path) if data_path else "",
        "chart_exists": exists,
        "chart_size_bytes": size,
        "has_data_source": data_path is not None,
        "status": status if data_path else "fail_missing_data_source",
    }
