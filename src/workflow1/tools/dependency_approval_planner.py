"""Create dependency approval plans instead of installing packages."""

from __future__ import annotations


def build_dependency_approval_plan(missing_tools: list[str]) -> list[dict[str, object]]:
    return [
        {
            "tool": tool,
            "status": "missing",
            "approval_required": True,
            "safe_fallback": "use local sklearn/model_registry fallback and record degraded explainability or AutoML coverage",
        }
        for tool in missing_tools
    ]
