"""Metric selection from task type."""

from __future__ import annotations

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


def select_metrics(task_type: str, registry: ModelRegistry | None = None) -> dict[str, list[str]]:
    registry = registry or load_model_registry()
    data = registry.get_map("task_to_metric_map", task_type)
    return {
        "required_metrics": list(data.get("required_metrics", [])),
        "optional_metrics": list(data.get("optional_metrics", [])),
        "not_applicable_reason_required_when_missing": True,
    }
