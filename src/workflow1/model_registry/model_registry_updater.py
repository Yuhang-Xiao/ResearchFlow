"""Append safe model registry update proposals to a ledger."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import csv


@dataclass
class RegistryUpdateProposal:
    task_type: str
    trigger: str
    proposed_update: str
    source: str
    requires_authorization: bool = False


def append_registry_update_proposal(
    proposal: RegistryUpdateProposal,
    ledger_path: str | Path = "workflow_improvement/model_registry_update_ledger.csv",
) -> dict[str, object]:
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    row = asdict(proposal)
    row["timestamp"] = datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp", *asdict(proposal).keys()])
        if not exists:
            writer.writeheader()
        writer.writerow(row)
    return {"status": "ok", "ledger": str(path), "proposal": row}
