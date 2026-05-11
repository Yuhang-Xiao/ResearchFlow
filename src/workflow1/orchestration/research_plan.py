"""ResearchPlan data object."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class ResearchPlan:
    task_type: str
    target_variable: str | None
    baseline_models: list[str]
    candidate_models: list[str]
    metrics: dict[str, list[str]]
    validation_strategy: dict[str, Any]
    explainability_plan: dict[str, Any]
    figure_table_plan: dict[str, list[str]]
    literature_needs: dict[str, Any]
    repair_strategies: list[dict[str, Any]]
    actions: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
