# workflow1 Model & Method Registry

This directory is the long-term knowledge base for automatic model, metric, validation, explainability, figure/table, literature, and repair selection.

Core files:

- `task_taxonomy.yaml`: task definitions and auto-detection rules.
- `task_to_model_map.yaml`: baseline and model family mapping.
- `task_to_metric_map.yaml`: required and optional metrics.
- `task_to_validation_strategy_map.yaml`: split and leakage policies.
- `task_to_explainability_map.yaml`: SHAP/fallback explanation policy.
- `task_to_figure_table_map.yaml`: paper-grade figure/table requirements.
- `model_failure_patterns.yaml`: common failure patterns.
- `model_repair_strategies.yaml`: gate-to-repair mapping.
- `model_literature_map.yaml`: academic evidence needs.
- `model_external_reference_map.yaml`: engineering references only.

The orchestrator reads these files through `workflow1.model_registry`; model choice must not be hard-coded in the top-level workflow.
