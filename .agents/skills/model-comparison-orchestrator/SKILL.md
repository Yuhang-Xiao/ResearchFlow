---
name: model-comparison-orchestrator
description: Require baselines, interpretable controls, advanced candidates, consistent splits, and complete metrics before model claims.
---

# model-comparison-orchestrator

## Required Comparisons

- Simple baseline, such as mean/median/majority/historical/risk-ranking as appropriate.
- Interpretable control, such as Linear/Logistic/Poisson/DecisionTree/GAM-like substitute.
- Advanced candidate only after the baseline contract is set.
- Same split, budget, constraints, preprocessing, and metrics across compared models.

## Outputs

- `model_comparison_metrics.csv`
- `model_comparison_audit.md`
- `baseline_fairness_findings.csv`
