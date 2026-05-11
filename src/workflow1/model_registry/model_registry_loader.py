"""Load workflow1 model and method registry YAML files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - dependency is declared but keep degraded mode.
    yaml = None


REGISTRY_FILES = {
    "task_taxonomy": "task_taxonomy.yaml",
    "model_families": "model_families.yaml",
    "task_to_model_map": "task_to_model_map.yaml",
    "task_to_metric_map": "task_to_metric_map.yaml",
    "task_to_explainability_map": "task_to_explainability_map.yaml",
    "task_to_validation_strategy_map": "task_to_validation_strategy_map.yaml",
    "task_to_figure_table_map": "task_to_figure_table_map.yaml",
    "model_failure_patterns": "model_failure_patterns.yaml",
    "model_repair_strategies": "model_repair_strategies.yaml",
    "model_literature_map": "model_literature_map.yaml",
    "model_external_reference_map": "model_external_reference_map.yaml",
}

METHOD_FILES = {
    "data_profiling_methods": "data_profiling_methods.yaml",
    "preprocessing_methods": "preprocessing_methods.yaml",
    "feature_engineering_methods": "feature_engineering_methods.yaml",
    "validation_methods": "validation_methods.yaml",
    "imbalance_methods": "imbalance_methods.yaml",
    "explainability_methods": "explainability_methods.yaml",
    "robustness_methods": "robustness_methods.yaml",
    "paper_reporting_methods": "paper_reporting_methods.yaml",
}


@dataclass
class ModelRegistry:
    """In-memory registry bundle used by the Research OS."""

    root: Path
    registries: dict[str, Any] = field(default_factory=dict)
    methods: dict[str, Any] = field(default_factory=dict)
    load_warnings: list[str] = field(default_factory=list)

    def get_task(self, task_type: str) -> dict[str, Any]:
        taxonomy = self.registries.get("task_taxonomy", {})
        tasks = taxonomy.get("tasks", taxonomy) if isinstance(taxonomy, dict) else {}
        return dict(tasks.get(task_type, {})) if isinstance(tasks, dict) else {}

    def get_map(self, map_name: str, task_type: str) -> dict[str, Any]:
        data = self.registries.get(map_name, {})
        tasks = data.get("tasks", data) if isinstance(data, dict) else {}
        value = tasks.get(task_type, {}) if isinstance(tasks, dict) else {}
        return dict(value or {})


def _load_yaml(path: Path) -> tuple[Any, str | None]:
    if not path.exists():
        return {}, f"missing registry file: {path}"
    if yaml is None:
        return {}, "PyYAML is unavailable; registry YAML could not be loaded"
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}, None


def load_model_registry(root: str | Path = "model_registry") -> ModelRegistry:
    """Load all model and method registry files without executing external code."""

    registry_root = Path(root)
    bundle = ModelRegistry(root=registry_root)
    for key, name in REGISTRY_FILES.items():
        value, warning = _load_yaml(registry_root / name)
        bundle.registries[key] = value
        if warning:
            bundle.load_warnings.append(warning)
    for key, name in METHOD_FILES.items():
        value, warning = _load_yaml(registry_root / name)
        bundle.methods[key] = value
        if warning:
            bundle.load_warnings.append(warning)
    return bundle
