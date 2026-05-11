"""Evidence dossier data object."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class EvidenceDossier:
    literature_items: list[dict[str, Any]] = field(default_factory=list)
    engineering_references: list[dict[str, Any]] = field(default_factory=list)
    result_artifacts: list[str] = field(default_factory=list)
    figure_artifacts: list[str] = field(default_factory=list)
    code_artifacts: list[str] = field(default_factory=list)
    citation_map: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
