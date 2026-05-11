"""Action queue for Research OS execution and repair."""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class ResearchAction:
    name: str
    status: str = "pending"
    priority: int = 50
    payload: dict[str, Any] = field(default_factory=dict)
    requires_authorization: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActionQueue:
    def __init__(self, actions: list[ResearchAction] | None = None) -> None:
        self.actions = actions or []

    def add(self, action: ResearchAction) -> None:
        self.actions.append(action)

    def extend(self, actions: list[ResearchAction]) -> None:
        self.actions.extend(actions)

    def pending(self) -> list[ResearchAction]:
        return sorted([a for a in self.actions if a.status == "pending"], key=lambda a: a.priority)

    def to_rows(self) -> list[dict[str, Any]]:
        return [a.to_dict() for a in self.actions]


def build_default_action_queue() -> ActionQueue:
    names = [
        "data_profile",
        "infer_target_type",
        "load_model_registry",
        "select_models",
        "select_metrics",
        "select_validation_strategy",
        "search_literature",
        "train_models",
        "run_shap_or_fallback",
        "generate_figures",
        "write_paper",
        "audit_gates",
        "repair_failed_gates",
        "package_final_product",
    ]
    return ActionQueue([ResearchAction(name=n, priority=i * 10) for i, n in enumerate(names)])


def actions_from_failed_gate(gate_name: str) -> list[ResearchAction]:
    mapping = {
        "ExplainabilityGate": ["run_shap_or_fallback"],
        "MetricCompletenessGate": ["rerun_task_appropriate_metrics"],
        "PaperCompletenessGate": ["write_missing_paper_sections"],
        "ModelComparisonGate": ["train_baseline_and_compare_models"],
        "FigureTableGate": ["generate_figures_and_captions"],
        "LiteratureEvidenceGate": ["expand_literature_search"],
        "ReferenceIntegrityGate": ["repair_reference_sidecar"],
        "WordRenderGate": ["repair_docx_layout"],
        "ReproducibilityGate": ["write_reproducibility_readme_and_manifest"],
        "ModelRegistryGate": ["update_model_registry_entry"],
    }
    return [ResearchAction(name=name, priority=20, payload={"source_gate": gate_name}) for name in mapping.get(gate_name, ["manual_review"])]
