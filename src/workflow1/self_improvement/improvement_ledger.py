from __future__ import annotations
import csv
from pathlib import Path

FIELDS = ["timestamp", "run_package", "action", "risk_level", "status", "approval_required", "notes"]

def append_ledger(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in FIELDS})
