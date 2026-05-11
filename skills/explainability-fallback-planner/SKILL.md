---
name: explainability-fallback-planner
description: Plan permutation importance/PDP/ALE/local/subgroup/extreme-case explanations when SHAP is unavailable or insufficient.
---

# explainability-fallback-planner

## Fallback Ladder

1. Model-native importance where meaningful.
2. Permutation importance on validation/test data.
3. PDP/ALE or carefully labeled response curves.
4. Interpretable substitute model.
5. Local explanations for representative and extreme cases.
6. Subgroup and error-mechanism analysis.

All outputs must state predictive association, not causality.
