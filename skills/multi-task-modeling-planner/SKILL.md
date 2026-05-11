---
name: multi-task-modeling-planner
description: Plan regression/classification/risk/extreme-event/time/group modeling tasks from target structure rather than forcing one model task.
---

# multi-task-modeling-planner

## Rules

- Continuous targets require regression.
- Binary/event targets require binary classification.
- Risk levels require multiclass or ordinal classification.
- Zero-inflated long-tail counts require regression plus event occurrence, risk level, and extreme-event tasks when scientifically relevant.
- Time, group, and spatial structure require matching validation strategies.

## Outputs

- `multi_task_modeling_plan.md`
- `metric_contract_by_task.csv`
- `model_family_candidates.csv`
