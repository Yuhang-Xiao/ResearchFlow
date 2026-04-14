# ML Problem Framer

## When To Use

Use this skill before training a model or selecting algorithms. In goal-driven autonomous mode, use the research objective and validated schema to frame the problem automatically when the objective is clear enough.

## Inputs

- Research question or product objective.
- Candidate target variable.
- Unit of analysis.
- Available feature sources.
- Temporal or grouping constraints.

## Outputs

- Problem type, such as regression, classification, ranking, clustering, forecasting, or causal estimation.
- Target definition and prediction unit, with assumptions when not explicitly specified.
- Candidate evaluation metrics.
- Leakage and split risks.
- Recommended baseline strategy.

## Recommended Workflow

1. Translate the research goal into a measurable task.
2. Define the target and prediction time point from the research goal and data schema when possible.
3. Identify the row-level unit and grouping structure.
4. List features that are allowed at prediction time.
5. Choose simple evaluation metrics aligned to the goal.
6. Recommend baseline models before advanced models.
7. Pause only if the research goal, target, or evaluation unit is too ambiguous to operationalize.
8. Record key decisions and assumptions in `project_state/decision_log.md`.
