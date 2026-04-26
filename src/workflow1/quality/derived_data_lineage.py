"""Derived data lineage manifest helpers."""
from __future__ import annotations

import csv
from pathlib import Path


def write_lineage_manifest(path: str | Path, records: list[dict]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fields = ["output_path", "source_paths", "transform", "row_count", "column_count", "status", "notes"]
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})
