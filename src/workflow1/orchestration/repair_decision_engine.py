"""Convert failed gates into repair decisions."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from workflow1.orchestration.action_queue import ResearchAction, actions_from_failed_gate


@dataclass
class RepairDecision:
    status: str
    repair_actions: list[dict[str, Any]]
    requires_human_authorization: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def decide_repairs(gate_results: list[dict[str, Any]]) -> RepairDecision:
    actions: list[ResearchAction] = []
    requires_auth = False
    for result in gate_results:
        if result.get("status") != "pass":
            requires_auth = requires_auth or bool(result.get("requires_human_authorization"))
            if not result.get("requires_human_authorization"):
                actions.extend(actions_from_failed_gate(str(result.get("gate_name"))))
    return RepairDecision(
        status="blocked_by_authorization" if requires_auth else ("repair_running" if actions else "ready_for_human_review"),
        repair_actions=[a.to_dict() for a in actions],
        requires_human_authorization=requires_auth,
        reason="failed gates converted to repair actions" if actions else "no auto-repairable failed gates",
    )
