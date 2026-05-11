"""Audit registry completeness."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


@dataclass
class RegistryIssue:
    task_type: str
    check: str
    status: str
    detail: str


REQUIRED_MAPS = [
    "task_to_model_map",
    "task_to_metric_map",
    "task_to_explainability_map",
    "task_to_validation_strategy_map",
    "task_to_figure_table_map",
    "model_literature_map",
    "model_repair_strategies",
]


def audit_model_registry(registry: ModelRegistry | None = None) -> dict[str, Any]:
    registry = registry or load_model_registry()
    taxonomy = registry.registries.get("task_taxonomy", {})
    tasks = taxonomy.get("tasks", taxonomy) if isinstance(taxonomy, dict) else {}
    issues: list[RegistryIssue] = []
    for task_type in sorted(tasks):
        model_map = registry.get_map("task_to_model_map", task_type)
        checks = {
            "baseline": bool(model_map.get("baseline_models")),
            "two_model_families": len(model_map.get("model_families", [])) >= 2,
            "required_metrics": bool(registry.get_map("task_to_metric_map", task_type).get("required_metrics")),
            "validation_strategy": bool(registry.get_map("task_to_validation_strategy_map", task_type)),
            "explainability": bool(registry.get_map("task_to_explainability_map", task_type).get("required_methods")),
            "figures_tables": bool(registry.get_map("task_to_figure_table_map", task_type).get("required_tables")),
            "literature": bool(registry.get_map("model_literature_map", task_type).get("needed_topics")),
            "repair": bool(registry.get_map("model_repair_strategies", task_type).get("strategies")),
        }
        for check, ok in checks.items():
            issues.append(RegistryIssue(task_type, check, "pass" if ok else "fail", "" if ok else "registry field missing"))
    failed = [i for i in issues if i.status == "fail"]
    return {
        "status": "pass" if not failed else "fail",
        "score": round(1 - len(failed) / max(1, len(issues)), 3),
        "issues": [asdict(i) for i in issues],
        "load_warnings": registry.load_warnings,
    }
