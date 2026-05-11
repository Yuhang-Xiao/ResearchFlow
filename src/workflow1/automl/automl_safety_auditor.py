"""Audit local AutoML tool availability without installing anything."""

from __future__ import annotations

import importlib.util


TOOLS = ["sklearn", "flaml", "autogluon", "pycaret", "tpot", "h2o", "xgboost", "lightgbm", "catboost", "shap", "openml", "mlflow"]


def audit_automl_tools() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for tool in TOOLS:
        package = "sklearn" if tool == "sklearn" else tool
        available = importlib.util.find_spec(package) is not None
        rows.append(
            {
                "tool": tool,
                "available": available,
                "auto_install_allowed": False,
                "action": "use_if_needed" if available else "create_dependency_approval_plan_and_fallback",
            }
        )
    return rows
