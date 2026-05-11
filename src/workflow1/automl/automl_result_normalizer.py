"""Normalize AutoML and local baseline results."""

from __future__ import annotations

from typing import Any


def normalize_automl_result(result: Any) -> dict[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    return dict(result)
