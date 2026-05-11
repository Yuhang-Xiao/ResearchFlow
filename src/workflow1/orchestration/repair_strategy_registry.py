"""Repair strategy registry."""

from __future__ import annotations


REPAIR_STRATEGY_REGISTRY = [
    {"failed_gate": "MetricCompletenessGate", "action": "rerun_task_appropriate_metrics", "priority": 10},
    {"failed_gate": "ExplainabilityGate", "action": "run_shap_or_fallback", "priority": 10},
    {"failed_gate": "ModelComparisonGate", "action": "train_baseline_and_compare_models", "priority": 10},
    {"failed_gate": "PaperCompletenessGate", "action": "write_missing_paper_sections", "priority": 20},
    {"failed_gate": "WordRenderGate", "action": "repair_docx_layout", "priority": 30},
    {"failed_gate": "LiteratureEvidenceGate", "action": "expand_literature_search", "priority": 20},
    {"failed_gate": "ModelRegistryGate", "action": "update_model_registry_entry", "priority": 15},
]
