# Autonomous Research Orchestrator

## Purpose

Use this skill as the main end-to-end orchestrator when the user provides raw data plus a research objective, scientific goal, modeling purpose, and optional constraints. The orchestrator should move the workflow forward autonomously unless execution is blocked by ambiguity, missing files, high-risk irreversible actions, or repository rule conflicts.

## Inputs

- Raw dataset path or data source.
- Research objective or modeling purpose.
- Optional constraints, preferences, expected outputs, or evaluation criteria.
- Relevant reference documents under `references/`, if present.
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
- Extracted reference guidance summaries, when reference documents are used.
- Updated project state files.

## Default Orchestration Flow

1. Confirm the active raw dataset and research goal.
2. Check whether relevant reference documents exist under `references/`.
3. If relevant references exist, use `skills/reference-document-reader` to extract Chinese guidance for cleaning, label engineering, modeling, simulation, optimization, visualization, or reporting.
4. Record extracted reference guidance under `references/processed_summaries/` when it will guide durable workflow decisions, and cite source file paths in workflow summaries.
5. Run the implemented minimum preparation stages when appropriate:
   - `workflow1 --stage intake`
   - `workflow1 --stage validation`
   - `workflow1 --stage cleaning-plan`
6. Decide identifiers, date fields, targets, metadata fields, candidate features, and exclusions from the data, research goal, reference guidance, and repository rules.
7. Clean, match, preprocess, and create cleaned analysis-ready datasets only when the user goal calls for execution beyond planning.
8. Run EDA guided by the research goal.
9. Frame the ML or statistical problem.
10. Select baseline and candidate advanced methods.
11. Train baseline models or run baseline analyses.
12. Compare, tune, and revise methods if initial performance is poor.
13. Generate reportable technical outputs.
14. Update `project_state` with assumptions, outputs, decisions, and next steps.

## Continue Automatically

Continue without asking for approval when:

- The raw dataset exists and can be read.
- The research goal is specific enough to operationalize.
- The action is reversible or produces derived outputs without modifying raw data.
- Cleaning, modeling, or reporting choices can be justified from the data, research goal, and repository rules.
- Reference documents, if present, are readable enough to extract relevant guidance or can be safely skipped with limitations recorded.
- The preparation stages are limited to intake, validation, and cleaning-plan unless heavier workflow logic has been explicitly implemented or requested.
- Any uncertainty can be handled by recording assumptions and preserving source fields.

## Pause Only When Blocked

Stop and ask the user only when:

- The research goal is too ambiguous to operationalize.
- A required file, sheet, column, or dependency is missing.
- An action would be destructive or irreversible in a risky way.
- The task conflicts with repository rules, privacy constraints, or user constraints.
- Reference documents are required by the user but unreadable, encrypted, scanned without OCR, or ambiguous in a way that blocks the requested workflow.

## Reference Guidance Rules

- Reference documents can influence cleaning, label engineering, modeling, simulation, optimization, visualization, and reporting.
- Do not assume every reference applies automatically.
- User explicit instruction overrides reference documents.
- Actual dataset evidence overrides generic reference suggestions when they conflict.
- If no relevant reference documents exist, proceed based on `AGENTS.md`, the user goal, and dataset evidence.
- Cite reference file paths in workflow summaries whenever extracted guidance affects a durable decision.

When stopping, state the blocker, list the options, and ask for the minimum clarification needed to continue.

## Project State Updates

After each durable stage, update project state as appropriate:

- `project_state/current_focus.md`: active dataset, research goal, current stage, and assumptions.
- `project_state/next_step.md`: the next autonomous step or the blocker requiring user input.
- `project_state/changelog.md`: outputs and workflow changes.
- `project_state/decision_log.md`: cleaning decisions, method choices, modeling assumptions, and their rationale.
