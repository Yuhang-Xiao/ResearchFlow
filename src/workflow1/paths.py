"""Shared path helpers for repository and framework assets."""

from __future__ import annotations

import os
from pathlib import Path


def workflow_home() -> Path:
    """Return the workflow workspace root used for local assets."""

    configured = os.environ.get("WORKFLOW1_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path.cwd().resolve()


def framework_root() -> Path:
    """Return the framework asset root, with a legacy fallback."""

    configured = os.environ.get("WORKFLOW1_FRAMEWORK_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    root = workflow_home() / "framework"
    if root.exists():
        return root
    return workflow_home()


def framework_path(*parts: str) -> Path:
    """Return a path under the framework asset root."""

    return framework_root().joinpath(*parts)


def model_registry_root() -> Path:
    """Return the model registry directory."""

    return framework_path("model_registry")


def workflow_recipes_root() -> Path:
    """Return the workflow recipes directory."""

    return framework_path("workflow_recipes")


def workflow_improvement_root() -> Path:
    """Return the workflow improvement directory."""

    return framework_path("workflow_improvement")
