"""Validation strategy selection from task type and data profile."""

from __future__ import annotations

from typing import Any

from workflow1.model_registry.model_registry_loader import ModelRegistry, load_model_registry


def select_validation_strategy(task_type: str, profile: dict[str, Any] | None = None, registry: ModelRegistry | None = None) -> dict[str, Any]:
    registry = registry or load_model_registry()
    data = registry.get_map("task_to_validation_strategy_map", task_type)
    profile = profile or {}
    strategy = dict(data)
    if profile.get("datetime_columns") and "time_aware" not in str(strategy).lower():
        strategy.setdefault("additional_checks", []).append("check temporal leakage and consider chronological split")
    return strategy
