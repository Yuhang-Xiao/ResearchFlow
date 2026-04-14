"""Lightweight helpers for goal-driven autonomous workflow planning."""

from dataclasses import dataclass, field


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
