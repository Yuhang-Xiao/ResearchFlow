"""ResearchTask data object."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

from workflow1.orchestration.research_state import ResearchState


@dataclass
class ResearchTask:
    data_file: str
    research_goal: str
    output_dir: str
    target_variable: str | None = None
    task_type: str | None = None
    constraints: list[str] = field(default_factory=list)
    state: ResearchState = ResearchState.INITIALIZED
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = str(self.state)
        return data

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)
