# Task Router

## When To Use

Use this skill at the start of a research workflow request when the correct next step is unclear or when a task may span multiple workflow areas.

## Inputs

- User request.
- Current project state files.
- Available data or artifact inventory, if relevant.

## Outputs

- Recommended workflow stage.
- Suggested skill or pipeline area.
- Short list of prerequisites or blockers.
- Proposed next action.

## Recommended Workflow

1. Read `AGENTS.md` and the project state files.
2. Classify the request into one or more stages: intake, schema profiling, cleaning, matching, validation, EDA, framing, method selection, baseline modeling, evaluation, visualization, reporting, or workflow update.
3. Check whether the request requires dataset access. If not, avoid data analysis.
4. Choose the smallest useful next step.
5. Record any durable routing decision in `project_state/decision_log.md`.
