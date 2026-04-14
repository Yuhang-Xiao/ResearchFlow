"""Minimal pipeline entry points.

These stubs exist so future workflow stages have a shared place to start
without introducing dataset-specific logic during scaffolding.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PipelineResult:
    """Lightweight result returned by starter pipeline functions."""

    name: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)


def run_placeholder_pipeline(name: str) -> PipelineResult:
    """Return a placeholder result for an unimplemented pipeline."""

    return PipelineResult(
        name=name,
        status="not_implemented",
        details={"message": "Implement this pipeline when a concrete task requires it."},
    )
