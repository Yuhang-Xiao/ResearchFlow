"""Known Research OS actions."""

from __future__ import annotations


ACTION_REGISTRY = [
    {"action": "data_profile", "executor": "research_executor.profile_data", "auto_repairable": True},
    {"action": "infer_target_type", "executor": "task_inference_engine", "auto_repairable": True},
    {"action": "load_model_registry", "executor": "model_registry_loader", "auto_repairable": True},
    {"action": "select_models", "executor": "model_selection_engine", "auto_repairable": True},
    {"action": "select_metrics", "executor": "metric_selection_engine", "auto_repairable": True},
    {"action": "select_validation_strategy", "executor": "validation_strategy_selector", "auto_repairable": True},
    {"action": "search_literature", "executor": "literature_need_selector", "auto_repairable": True},
    {"action": "train_models", "executor": "sklearn_baseline_adapter", "auto_repairable": True},
    {"action": "run_shap_or_fallback", "executor": "explainability_selector", "auto_repairable": True},
    {"action": "generate_figures", "executor": "figure_table_selector", "auto_repairable": True},
    {"action": "write_paper", "executor": "paper_product_writer_or_template", "auto_repairable": True},
    {"action": "audit_gates", "executor": "quality_gate_runner", "auto_repairable": True},
    {"action": "repair_failed_gates", "executor": "auto_repair_loop", "auto_repairable": True},
    {"action": "create_dependency_approval_plan", "executor": "dependency_approval_planner", "auto_repairable": False},
]
