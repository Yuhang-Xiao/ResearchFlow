---
name: model-setting-documenter
description: Document model settings for DQN, Q-learning, heuristics, supervised models, Bayesian models, time series, Monte Carlo, and optimization models with literature and evidence mapping.
---

# model-setting-documenter

Use before or after any model run when the user needs detailed model settings, method writing, or formal readiness checks.

## Required Coverage

- model purpose
- input features / state / target / action
- reward, constraints, transition, belief update when relevant
- parameters and hyperparameters
- training process
- evaluation metrics
- baselines
- result interpretation
- literature basis
- limitations
- experimental/formal status

## Evidence Rules

- Settings must come from local config, code, data outputs, project state, or verified literature.
- Unknown settings must be marked `未核验` or `experimental assumption`.
- Formal DQN/RL requires user-confirmed parameter tables.

## Outputs

- `model_setting_detail_report.md`
- `model_output_explanations.md`
- `model_component_literature_map.csv`
- `model_limitations_and_formal_status.md`
