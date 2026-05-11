"""Select literature evidence needs by task type."""

from __future__ import annotations

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


def select_literature_needs(task_type: str, registry: ModelRegistry | None = None) -> dict[str, object]:
    registry = registry or load_model_registry()
    data = registry.get_map("model_literature_map", task_type)
    return {
        "needed_topics": list(data.get("needed_topics", [])),
        "seed_references": list(data.get("seed_references", [])),
        "evidence_rule": "同行评议文献支撑论文正式论断；GitHub/HF/OpenML 仅作工程参考。",
    }
