# AGENTS.md

## Project Purpose

This repository is a general-purpose scientific workflow scaffold for Codex. It is designed to support research tasks such as raw data intake, schema inspection, data cleaning and matching, validation, exploratory data analysis, ML problem framing, method selection, baseline modeling, result comparison, visualization, reporting, and iterative workflow updates.

Do not assume a domain, dataset, model type, or final report format until the user or project state makes it clear.

## Default Workflow Order

1. Read `project_state/current_focus.md`, `project_state/next_step.md`, `project_state/roadmap.yaml`, `project_state/decision_log.md`, and this file.
2. Confirm the task scope from the user request and local project state.
3. Route the task to the relevant skill or pipeline area.
4. Inspect file names, schemas, and metadata before reading full datasets.
5. Perform the smallest useful workflow step.
6. Validate outputs before using them downstream.
7. Save generated outputs under the appropriate `data`, `reports`, or `experiments` folder.
8. Update project state files when decisions, outputs, or next steps change.

Recommended workflow progression:

```text
intake -> schema profiling -> cleaning/matching -> validation -> EDA
-> ML problem framing -> method selection -> baseline modeling
-> evaluation/comparison -> visualization -> reporting -> workflow update
```

## Data Handling Rules

- Do not analyze datasets unless the user asks for analysis or the current task clearly requires it.
- Treat `data/01_raw` as immutable. Do not edit raw data in place.
- Write derived files to the next appropriate layer:
  - `data/02_intermediate` for parsed or lightly transformed data.
  - `data/03_primary` for cleaned analysis-ready tables.
  - `data/04_feature` for engineered features.
  - `data/05_model_input` for final modeling matrices or splits.
- Prefer metadata and schema inspection before loading entire large files.
- Record data assumptions, joins, filters, exclusions, and validation failures.
- Avoid storing secrets, credentials, tokens, or private identifiers in committed files.
- When handling sensitive or human-subject data, minimize exposure, use aggregate outputs where possible, and ask for clarification before exporting risky artifacts.

## Modeling Rules

- Frame the scientific or operational question before choosing a model.
- Identify the prediction target, unit of analysis, temporal structure, leakage risks, and evaluation metric before training.
- Start with transparent baselines before advanced methods.
- Separate model input construction from model training.
- Use reproducible splits when possible and record random seeds.
- Compare models against baselines with the same data splits and metrics.
- Do not overfit the scaffold with heavy training logic until a real task requires it.

## Output Rules

- Put figures in `reports/figures`.
- Put tables in `reports/tables`.
- Put Quarto or report drafts in `reports/quarto`.
- Put experiment artifacts under `experiments/baselines`, `experiments/advanced`, or `experiments/comparisons`.
- Keep outputs named with enough context to be traceable.
- Prefer lightweight, text-readable summaries for project state and decision records.
- Make final responses concise and include what changed, where it lives, and the next recommended task.

## Project State Update Rules

Update project state files whenever a task changes the workflow, produces durable outputs, or makes a meaningful decision.

- `project_state/roadmap.yaml`: update phase status, milestones, or task ordering.
- `project_state/current_focus.md`: describe the active objective and constraints.
- `project_state/next_step.md`: keep one clear recommended next action.
- `project_state/changelog.md`: append dated entries for notable changes.
- `project_state/decision_log.md`: append dated decisions with rationale and impact.

Do not rewrite history casually. Append new entries unless the user asks for cleanup.
