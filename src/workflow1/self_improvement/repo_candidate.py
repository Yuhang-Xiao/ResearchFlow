from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class RepoCandidate:
    name: str
    url: str
    category: str
    recommendation: str
    rationale: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
