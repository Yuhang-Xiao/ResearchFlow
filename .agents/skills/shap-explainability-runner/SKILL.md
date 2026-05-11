---
name: shap-explainability-runner
description: Run SHAP when installed and model-compatible; otherwise produce a documented fallback plan.
---

# shap-explainability-runner

## Gate Rules

- Check whether `shap` is installed and whether the selected model is compatible.
- If SHAP is available, run global and local explanations and write figures/tables.
- If SHAP is unavailable, record the reason and route to permutation importance, PDP/ALE, interpretable control, local explanation, and subgroup error analysis.
- Never write SHAP or feature importance as causal proof.

## Outputs

- `shap_availability_audit.csv`
- `shap_or_fallback_decision.csv`
- `explainability_outputs/`
