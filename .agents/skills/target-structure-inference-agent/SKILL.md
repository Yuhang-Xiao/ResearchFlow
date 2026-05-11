---
name: target-structure-inference-agent
description: Infer target type, zero inflation, imbalance, time/group/spatial structure, leakage risk, and downstream task families.
---

# target-structure-inference-agent

## Required Checks

- Candidate target variable, unit of analysis, identifier/date/group/region fields.
- Continuous, binary, multiclass/ordinal, count, zero-inflated, long-tail, or extreme-event structure.
- Missingness, imbalance, all-zero risk, outliers, leakage, post-outcome features.
- Time-aware, group-aware, or spatial validation needs.

## Output Contract

- `target_structure_inference.csv`
- `leakage_and_split_risk_audit.csv`
- `recommended_task_families.md`

If the target or unit of analysis cannot be identified, block modeling and ask for user clarification.
