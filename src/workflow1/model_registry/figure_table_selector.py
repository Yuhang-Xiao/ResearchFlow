"""Figure and table plan selection."""

from __future__ import annotations

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


def select_figure_table_plan(task_type: str, registry: ModelRegistry | None = None) -> dict[str, list[str]]:
    registry = registry or load_model_registry()
    data = registry.get_map("task_to_figure_table_map", task_type)
    return {
        "required_figures": list(data.get("required_figures", [])),
        "required_tables": list(data.get("required_tables", [])),
        "qa_requirements": list(data.get("qa_requirements", ["source_data", "nonblank_output", "caption", "paper_reference"])),
    }
