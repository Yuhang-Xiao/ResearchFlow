"""Unified quality gate result."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class QualityGateResult:
    gate_name: str
    status: str
    severity: str
    failed_items: list[str] = field(default_factory=list)
    evidence_files: list[str] = field(default_factory=list)
    repair_suggestions: list[str] = field(default_factory=list)
    auto_repairable: bool = True
    requires_human_authorization: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
