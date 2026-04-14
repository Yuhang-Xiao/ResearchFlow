# Task Router

## When To Use

Use this skill at the start of a research workflow request when the correct next step is unclear or when a task may span multiple workflow areas. If the user provides raw data plus a research objective, route to `skills/autonomous-research-orchestrator` for end-to-end execution.

## Inputs

- User request.
- Current project state files.
- Available data or artifact inventory, if relevant.

## Outputs

- Recommended workflow stage or orchestrator handoff.
- Suggested skill or pipeline area.
- Short list of prerequisites or blockers.
- Proposed next action.

## Recommended Workflow

1. Read `AGENTS.md` and the project state files.
2. Classify the request into one or more stages: intake, schema profiling, cleaning, matching, validation, EDA, framing, method selection, baseline modeling, evaluation, visualization, reporting, or workflow update.
3. If raw data plus a research goal are present, hand off to the autonomous research orchestrator.
4. If the request lacks a usable research goal, identify the blocker and ask for the minimum clarification needed.
5. If the request does not require dataset access, avoid data analysis.
6. Record any durable routing decision in `project_state/decision_log.md`.
