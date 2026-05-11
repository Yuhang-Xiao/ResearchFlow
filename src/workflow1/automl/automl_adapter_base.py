"""Base classes for safe AutoML adapters."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class AutoMLRunResult:
    adapter_name: str
    status: str
    task_type: str
    metrics: dict[str, Any]
    model_summary: str
    warnings: list[str]
    artifacts: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AutoMLAdapter:
    adapter_name = "base"
    optional_dependency = ""

    def is_available(self) -> bool:
        return False

    def fit_predict(self, *args: Any, **kwargs: Any) -> AutoMLRunResult:  # pragma: no cover - abstract.
        raise NotImplementedError
