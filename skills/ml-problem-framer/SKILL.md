# ML Problem Framer

## When To Use

Use this skill before training a model or selecting algorithms, especially when the target, prediction unit, leakage risks, or metric are unclear.

## Inputs

- Research question or product objective.
- Candidate target variable.
- Unit of analysis.
- Available feature sources.
- Temporal or grouping constraints.

## Outputs

- Problem type, such as regression, classification, ranking, clustering, forecasting, or causal estimation.
- Target definition and prediction unit.
- Candidate evaluation metrics.
- Leakage and split risks.
- Recommended baseline strategy.

## Recommended Workflow

1. Translate the research goal into a measurable task.
2. Define the target and prediction time point.
3. Identify the row-level unit and grouping structure.
4. List features that are allowed at prediction time.
5. Choose simple evaluation metrics aligned to the goal.
6. Recommend baseline models before advanced models.
7. Record key decisions in `project_state/decision_log.md`.
