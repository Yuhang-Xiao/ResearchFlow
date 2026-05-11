---
name: model-registry-auditor
description: Audit workflow1 Model & Method Registry completeness, task-to-model mappings, metric coverage, explainability coverage, validation strategies, literature evidence needs, and repair strategies.
---

# Model Registry Auditor

Use this skill when the user asks to audit, update, or rely on the workflow1 model registry.

## Required Inputs

- `model_registry/task_taxonomy.yaml`
- `model_registry/task_to_model_map.yaml`
- `model_registry/task_to_metric_map.yaml`
- `model_registry/task_to_explainability_map.yaml`
- `model_registry/task_to_validation_strategy_map.yaml`
- `model_registry/task_to_figure_table_map.yaml`
- `model_registry/model_literature_map.yaml`
- `model_registry/model_repair_strategies.yaml`

## Checks

1. Each task type has at least one baseline.
2. Each task type has at least two candidate model families.
3. Required metrics, validation strategy, explainability methods, figure/table plan, literature needs, failure patterns, and repair strategies are present.
4. GitHub/Hugging Face/OpenML references are marked as engineering references, not academic evidence.
5. Optional dependencies are routed through authorization planning when missing.

## Implementation

Prefer `workflow1.model_registry.model_registry_auditor.audit_model_registry()` and write results into the active run package.
