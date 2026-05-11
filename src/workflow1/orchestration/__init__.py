"""Goal-driven orchestration primitives for workflow1.

This package keeps the old public API from ``workflow1.orchestration`` while
adding product-mode routing, gate planning, repair planning, and packaging
contracts for ``data file + research goal -> research product`` workflows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from workflow1.orchestration.auto_repair_loop import plan_auto_repair_loop
from workflow1.orchestration.auto_research_product_orchestrator import (
    build_product_orchestration_dry_run,
    run_auto_research_product,
)
from workflow1.orchestration.quality_gate_runner import run_quality_gate_plan
from workflow1.orchestration.research_task_router import infer_research_product_tasks


DEFAULT_GOAL_DRIVEN_STAGES: tuple[str, ...] = (
    "schema_profiling",
    "raw_validation",
    "cleaning_matching",
    "cleaned_dataset_creation",
    "eda",
    "problem_framing",
    "method_selection",
    "baseline_model",
    "comparison_tuning",
    "model_revision_if_needed",
    "output_generation",
    "workflow_update",
)

AUTO_RESEARCH_PRODUCT_LAYERS: tuple[str, ...] = (
    "user_input_layer",
    "task_understanding_layer",
    "data_understanding_layer",
    "research_planning_layer",
    "literature_evidence_layer",
    "external_engineering_reference_layer",
    "modeling_execution_layer",
    "model_explainability_layer",
    "figure_table_product_layer",
    "full_paper_writing_layer",
    "word_product_layer",
    "quality_gate_layer",
    "auto_repair_layer",
    "archival_reproducibility_layer",
)

AUTO_RESEARCH_PRODUCT_GATES: tuple[str, ...] = (
    "input_contract_gate",
    "data_profile_gate",
    "target_structure_gate",
    "multi_task_modeling_gate",
    "metric_completeness_gate",
    "model_comparison_gate",
    "explainability_gate",
    "figure_table_product_gate",
    "literature_first_evidence_gate",
    "reference_integrity_gate",
    "full_paper_product_gate",
    "word_render_gate",
    "result_claim_guard_gate",
    "reproducibility_packaging_gate",
    "high_journal_readiness_gate",
)

FULL_PAPER_REQUIRED_SECTIONS: tuple[str, ...] = (
    "Title",
    "Abstract",
    "Keywords",
    "Introduction",
    "Literature Review",
    "Method",
    "Results",
    "Discussion",
    "Conclusion",
    "References",
    "Appendix",
)

BLOCKING_CONDITIONS: tuple[str, ...] = (
    "ambiguous_research_goal",
    "missing_required_file",
    "risky_destructive_or_irreversible_action",
    "repository_rule_conflict",
)


@dataclass(frozen=True)
class ResearchObjective:
    """User-provided research objective and optional constraints."""

    raw_dataset: str
    goal: str
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True)
class OrchestrationPlan:
    """Minimal representation of the autonomous workflow plan."""

    objective: ResearchObjective
    stages: tuple[str, ...] = DEFAULT_GOAL_DRIVEN_STAGES
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)

    @property
    def can_continue(self) -> bool:
        """Return whether the plan can continue autonomously."""

        return not self.blockers


@dataclass(frozen=True)
class AutoResearchProductPlan:
    """Product-mode plan for data + research goal -> paper-grade package."""

    data_file: str
    research_goal: str
    optional_constraints: tuple[str, ...] = ()
    product_mode: str = "auto_research_product"
    layers: tuple[str, ...] = AUTO_RESEARCH_PRODUCT_LAYERS
    quality_gates: tuple[str, ...] = AUTO_RESEARCH_PRODUCT_GATES
    required_paper_sections: tuple[str, ...] = FULL_PAPER_REQUIRED_SECTIONS
    auto_repair_rounds: tuple[str, ...] = (
        "round_1_initial_execution",
        "round_2_quality_gate_repair",
        "round_3_word_and_paper_repair",
    )
    approval_required_actions: tuple[str, ...] = (
        "Zotero database write",
        "paid or institution-only full text",
        "external plugin or MCP installation",
        "API key use",
        "large dependency installation",
        "large external dataset/model download",
        "running unknown third-party code",
    )
    blockers: tuple[str, ...] = ()

    @property
    def can_start(self) -> bool:
        """Return whether a product-mode run can start without clarification."""

        return not self.blockers

    def as_dict(self) -> dict[str, Any]:
        """Serialize the plan for CLI dry-run output."""

        return {
            "data_file": self.data_file,
            "research_goal": self.research_goal,
            "optional_constraints": list(self.optional_constraints),
            "product_mode": self.product_mode,
            "layers": list(self.layers),
            "quality_gates": list(self.quality_gates),
            "required_paper_sections": list(self.required_paper_sections),
            "auto_repair_rounds": list(self.auto_repair_rounds),
            "approval_required_actions": list(self.approval_required_actions),
            "blockers": list(self.blockers),
            "can_start": self.can_start,
        }


def make_goal_driven_plan(
    raw_dataset: str,
    goal: str,
    constraints: tuple[str, ...] | None = None,
) -> OrchestrationPlan:
    """Create a lightweight default plan for raw data plus a research goal."""

    blockers: list[str] = []
    if not raw_dataset.strip():
        blockers.append("missing_required_file")
    if not goal.strip():
        blockers.append("ambiguous_research_goal")

    objective = ResearchObjective(
        raw_dataset=raw_dataset,
        goal=goal,
        constraints=constraints or (),
    )
    return OrchestrationPlan(objective=objective, blockers=tuple(blockers))


def make_auto_research_product_plan(
    data_file: str,
    research_goal: str,
    constraints: tuple[str, ...] | None = None,
) -> AutoResearchProductPlan:
    """Create a product-mode plan from a data file and research goal."""

    blockers: list[str] = []
    if not data_file.strip():
        blockers.append("missing_data_file")
    if not research_goal.strip():
        blockers.append("missing_research_goal")
    inferred_tasks = infer_research_product_tasks(research_goal)
    enriched_constraints = tuple(constraints or ()) + tuple(f"planned_task:{task}" for task in inferred_tasks)
    return AutoResearchProductPlan(
        data_file=data_file,
        research_goal=research_goal,
        optional_constraints=enriched_constraints,
        blockers=tuple(blockers),
    )


__all__ = [
    "AUTO_RESEARCH_PRODUCT_GATES",
    "AUTO_RESEARCH_PRODUCT_LAYERS",
    "AutoResearchProductPlan",
    "BLOCKING_CONDITIONS",
    "DEFAULT_GOAL_DRIVEN_STAGES",
    "FULL_PAPER_REQUIRED_SECTIONS",
    "OrchestrationPlan",
    "ResearchObjective",
    "build_product_orchestration_dry_run",
    "infer_research_product_tasks",
    "make_auto_research_product_plan",
    "make_goal_driven_plan",
    "plan_auto_repair_loop",
    "run_quality_gate_plan",
    "run_auto_research_product",
]
