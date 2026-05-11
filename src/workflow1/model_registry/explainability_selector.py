"""Explainability selection from task type and tool availability."""

from __future__ import annotations

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


def select_explainability(task_type: str, shap_available: bool = False, registry: ModelRegistry | None = None) -> dict[str, object]:
    registry = registry or load_model_registry()
    data = registry.get_map("task_to_explainability_map", task_type)
    methods = list(data.get("required_methods", []))
    if shap_available and "SHAP" not in methods:
        methods.insert(0, "SHAP")
    return {
        "required_methods": methods,
        "fallback_methods": list(data.get("fallback_methods", ["permutation_importance"])),
        "shap_available": shap_available,
        "policy": "SHAP 可用则优先运行；不可用必须记录原因并运行解释性替代方案。",
    }
