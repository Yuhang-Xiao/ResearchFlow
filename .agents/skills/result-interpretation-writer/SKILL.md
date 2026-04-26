---
name: result-interpretation-writer
description: Convert model outputs and evaluation tables into readable result interpretation with metric meanings, limitations, quality gates, and experimental/formal boundaries.
---

# result-interpretation-writer

Use after model comparison, quality gate, chart QA, or paper Results generation.

## Required Coverage

- overall model comparison
- what each metric means
- what higher/lower values imply
- stability and convergence
- reward hacking risk for RL/DQN
- constraint violation risk
- which results can enter paper Results
- which results remain exploratory or experimental
- what requires human confirmation
- domain implication and overclaiming boundaries

## Outputs

- `model_result_interpretation_report.md`
- `model_output_explanations.md`
- `result_interpretation_guide.md`
- claim/evidence map when paper use is requested
