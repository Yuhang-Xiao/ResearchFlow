"""Select repair strategies for model and product failures."""

from __future__ import annotations

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


def select_repair_strategies(task_type: str, failed_gate: str | None = None, registry: ModelRegistry | None = None) -> list[dict[str, object]]:
    registry = registry or load_model_registry()
    data = registry.get_map("model_repair_strategies", task_type)
    strategies = list(data.get("strategies", []))
    if failed_gate:
        strategies = [s for s in strategies if failed_gate in s.get("applies_to_gates", [])] or strategies
    return strategies
