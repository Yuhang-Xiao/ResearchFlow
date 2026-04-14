# Autonomous Research Orchestrator

## Purpose

Use this skill as the main end-to-end orchestrator when the user provides raw data plus a research objective, scientific goal, modeling purpose, and optional constraints. The orchestrator should move the workflow forward autonomously unless execution is blocked by ambiguity, missing files, high-risk irreversible actions, or repository rule conflicts.

## Inputs

- Raw dataset path or data source.
- Research objective or modeling purpose.
- Optional constraints, preferences, expected outputs, or evaluation criteria.
- Current project state files and relevant prior workflow outputs.

## Outputs

- Schema inventory and raw validation outputs.
- Cleaned or matched datasets in the appropriate `data` layer.
- EDA tables, figures, and technical summaries.
- ML/statistical problem framing notes.
- Method selection notes and assumptions.
- Baseline and advanced experiment artifacts when appropriate.
- Comparison, tuning, and revision summaries.
- Reportable technical outputs.
- Updated project state files.

## Default Orchestration Flow

1. Confirm the active raw dataset and research goal.
2. Run schema profiling and raw validation.
3. Decide identifiers, date fields, targets, metadata fields, candidate features, and exclusions from the data plus the research goal.
4. Clean, match, preprocess, and create cleaned analysis-ready datasets.
5. Run EDA guided by the research goal.
6. Frame the ML or statistical problem.
7. Select baseline and candidate advanced methods.
8. Train baseline models or run baseline analyses.
9. Compare, tune, and revise methods if initial performance is poor.
10. Generate reportable technical outputs.
11. Update `project_state` with assumptions, outputs, decisions, and next steps.

## Continue Automatically

Continue without asking for approval when:

- The raw dataset exists and can be read.
- The research goal is specific enough to operationalize.
- The action is reversible or produces derived outputs without modifying raw data.
- Cleaning, modeling, or reporting choices can be justified from the data, research goal, and repository rules.
- Any uncertainty can be handled by recording assumptions and preserving source fields.

## Pause Only When Blocked

Stop and ask the user only when:

- The research goal is too ambiguous to operationalize.
- A required file, sheet, column, or dependency is missing.
- An action would be destructive or irreversible in a risky way.
- The task conflicts with repository rules, privacy constraints, or user constraints.

When stopping, state the blocker, list the options, and ask for the minimum clarification needed to continue.

## Project State Updates

After each durable stage, update project state as appropriate:

- `project_state/current_focus.md`: active dataset, research goal, current stage, and assumptions.
- `project_state/next_step.md`: the next autonomous step or the blocker requiring user input.
- `project_state/changelog.md`: outputs and workflow changes.
- `project_state/decision_log.md`: cleaning decisions, method choices, modeling assumptions, and their rationale.
