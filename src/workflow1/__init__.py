"""General-purpose scientific workflow package."""

from workflow1.orchestration import OrchestrationPlan, ResearchObjective, make_goal_driven_plan

__all__ = [
    "__version__",
    "OrchestrationPlan",
    "ResearchObjective",
    "make_goal_driven_plan",
]

__version__ = "0.1.0"
