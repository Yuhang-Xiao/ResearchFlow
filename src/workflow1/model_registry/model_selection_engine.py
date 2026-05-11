"""Select candidate model families from the workflow1 registry."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


@dataclass
class ModelDecision:
    task_type: str
    baseline_models: list[str]
    candidate_model_families: list[str]
    excluded_models: list[str]
    selection_reasons: list[str]
    dependency_warnings: list[str]
    requires_human_authorization: bool
    method_prompt: str
    results_prompt: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def select_models(task_type: str, registry: ModelRegistry | None = None, available_tools: dict[str, bool] | None = None) -> ModelDecision:
    registry = registry or load_model_registry()
    available_tools = available_tools or {}
    mapping = registry.get_map("task_to_model_map", task_type)
    task = registry.get_task(task_type)
    baselines = list(mapping.get("baseline_models") or task.get("recommended_baseline") or ["dummy_baseline"])
    candidates = list(mapping.get("model_families") or task.get("recommended_model_families") or ["linear_model", "tree_ensemble"])
    excluded = list(mapping.get("not_applicable_models") or task.get("not_applicable_models") or [])
    warnings: list[str] = []
    for family in candidates:
        required = registry.registries.get("model_families", {}).get("families", {}).get(family, {}).get("optional_dependencies", [])
        missing = [dep for dep in required if available_tools and not available_tools.get(dep, False)]
        if missing:
            warnings.append(f"{family} requires optional dependencies not currently available: {', '.join(missing)}")
    return ModelDecision(
        task_type=task_type,
        baseline_models=baselines,
        candidate_model_families=candidates,
        excluded_models=excluded,
        selection_reasons=[
            f"任务类型 {task_type} 的模型候选来自 model_registry/task_to_model_map.yaml",
            "默认先跑透明 baseline，再比较可解释控制模型与增强模型/AutoML 候选",
        ],
        dependency_warnings=warnings,
        requires_human_authorization=False,
        method_prompt=str(mapping.get("method_writing_notes") or task.get("method_writing_notes") or ""),
        results_prompt=str(mapping.get("results_writing_notes") or task.get("results_writing_notes") or ""),
    )
