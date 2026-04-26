# Workflow Updater

## When To Use

Use this skill after a workflow step creates durable outputs, decisions, assumptions, or lessons that should guide future work. In goal-driven autonomous mode, update project state after each completed stage so the workflow can continue coherently.

## Inputs

- Completed task summary.
- Output file paths.
- Decisions and assumptions, including autonomous cleaning/modeling choices.
- Known blockers or next steps.

## Outputs

- Updated project state files.
- Optional updates to `AGENTS.md` when workflow rules change.
- Changelog entry.
- Decision log entry, if applicable.
- References to generated intake, validation, or cleaning-plan artifacts when those stages run.

## Recommended Workflow

1. Identify which project state files need updates.
2. Append dated changelog entries for durable changes.
3. Append decision log entries for important choices and autonomous assumptions.
4. Keep `current_focus.md` aligned to the active objective.
5. Keep `next_step.md` focused on one recommended next action.
6. Update `roadmap.yaml` only when phase status or task ordering changes.
7. When `intake`, `validation`, or `cleaning-plan` outputs are generated, record paths and confirm whether the stage was non-destructive.
