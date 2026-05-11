"""Lightweight data generation validation utilities."""
from __future__ import annotations

import csv
from pathlib import Path


def summarize_table(path: str | Path, key_fields: list[str] | None = None) -> dict:
    p = Path(path)
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []
    return {
        "path": str(p),
        "row_count": len(rows),
        "column_count": len(fields),
        "key_fields": key_fields or [],
        "missing_key_fields": [k for k in (key_fields or []) if k not in fields],
        "status": "pass" if fields else "fail_no_columns",
    }


def validate_generated_output(path: str | Path, source_paths: list[str], key_fields: list[str] | None = None) -> dict:
    summary = summarize_table(path, key_fields)
    summary["source_paths"] = source_paths
    summary["has_lineage"] = bool(source_paths)
    if not summary["has_lineage"]:
        summary["status"] = "fail_missing_lineage"
    return summary
