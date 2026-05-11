"""Research OS state machine."""

from __future__ import annotations

from enum import StrEnum


class ResearchState(StrEnum):
    INITIALIZED = "initialized"
    DATA_PROFILED = "data_profiled"
    TARGET_INFERRED = "target_inferred"
    LITERATURE_STARTED = "literature_started"
    EXPERIMENT_PLANNED = "experiment_planned"
    MODELS_TRAINED = "models_trained"
    GATES_FAILED = "gates_failed"
    REPAIR_RUNNING = "repair_running"
    PAPER_DRAFTED = "paper_drafted"
    WORD_RENDERED = "word_rendered"
    READY_FOR_HUMAN_REVIEW = "ready_for_human_review"
    BLOCKED_BY_AUTHORIZATION = "blocked_by_authorization"
