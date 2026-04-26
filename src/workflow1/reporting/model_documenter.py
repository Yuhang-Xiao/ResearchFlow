"""Model documentation protocol helpers."""

from __future__ import annotations


REQUIRED_MODEL_DOCUMENTATION_FIELDS = [
    "model_purpose",
    "input_features_or_state",
    "target_or_action_or_reward",
    "constraints_and_transition_when_relevant",
    "parameters_and_hyperparameters",
    "training_process",
    "evaluation_metrics",
    "baselines",
    "result_interpretation",
    "literature_basis",
    "limitations",
    "experimental_or_formal_status",
]


def missing_model_documentation_fields(record: dict[str, object]) -> list[str]:
    """Return required model documentation fields missing from a record."""

    return [field for field in REQUIRED_MODEL_DOCUMENTATION_FIELDS if not record.get(field)]
