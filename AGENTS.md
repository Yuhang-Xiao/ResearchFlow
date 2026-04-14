# AGENTS.md

## Project Purpose

This repository is a general-purpose scientific workflow scaffold for Codex. It is designed to support research tasks such as raw data intake, schema inspection, data cleaning and matching, validation, exploratory data analysis, ML problem framing, method selection, baseline modeling, result comparison, visualization, reporting, and iterative workflow updates.

Do not assume a domain, dataset, model type, or final report format until the user or project state makes it clear.

## Default Workflow Order

1. Read `project_state/current_focus.md`, `project_state/next_step.md`, `project_state/roadmap.yaml`, `project_state/decision_log.md`, and this file.
2. Confirm the task scope from the user request and local project state.
3. Route the task to the relevant skill or pipeline area.
4. Inspect file names, schemas, and metadata before reading full datasets.
5. Perform the next useful workflow step under the goal-driven autonomous execution policy.
6. Validate outputs before using them downstream.
7. Save generated outputs under the appropriate `data`, `reports`, or `experiments` folder.
8. Update project state files when decisions, outputs, or next steps change.

Recommended workflow progression:

```text
intake -> schema profiling -> cleaning/matching -> validation -> EDA
-> ML problem framing -> method selection -> baseline modeling
-> evaluation/comparison -> visualization -> reporting -> workflow update
```

## Language Policy

- Adapt automatically to the language used in the raw data.
- If raw data, column names, sheet names, or metadata are mainly in Chinese, use Chinese-first mode when reading and interpreting them.
- Unless the user explicitly specifies otherwise, use Chinese as the default interaction language.
- Write default repository outputs in Chinese, including schema inventories, validation proposals, validation reports, cleaning logs, data dictionaries, variable maps, and technical analysis summaries.
- Keep original source field names unchanged, especially Chinese column names.
- Algorithm names, model names, parameter names, code terms, and evaluation metrics may remain in English when appropriate.
- When needed, provide bilingual terminology, but keep the main document language Chinese by default.
- If the user explicitly specifies a language for a deliverable, follow the user's instruction for that deliverable.
- If no explicit language is specified, default to Chinese while preserving source field names and allowing appropriate technical terms to remain in English.

## Language Priority Rule

Language instructions are resolved in this order:

```text
user explicit instruction > task-specific requirement > default repository language policy
```

## Language Implementation Guidance

- When generating mixed-language outputs, keep terminology consistent across files and responses.
- Do not translate column names blindly if that may break code, joins, mappings, or traceability to source data.
- When needed, provide bilingual field mapping or terminology, but preserve original source field names.

## Goal-Driven Autonomous Research Execution Policy

When the user provides raw data plus a research goal, scientific objective, or modeling purpose, Codex should autonomously continue the downstream research workflow without waiting for approval at every major stage. Codex should use any optional constraints or preferences supplied by the user to shape the workflow and record assumptions explicitly.

Default workflow:

```text
schema profiling -> raw validation -> cleaning/matching -> cleaned dataset creation
-> EDA -> ML/statistical problem framing -> method selection -> baseline model
-> comparison/tuning -> model revision if needed -> output generation -> workflow update
```

Codex should use the raw dataset and the stated research goal together to decide:

- The data cleaning strategy.
- Which variables are likely identifiers, dates, targets, metadata, or candidate features.
- Whether the task is classification, regression, time series, clustering, anomaly detection, optimization, or another research workflow.
- Which baseline and advanced methods are appropriate.

Codex should automatically perform:

- Data cleaning and preprocessing.
- Cleaned dataset creation.
- Technical data summaries.
- Formal EDA.
- Model framing.
- Model selection.
- Baseline modeling.
- Tuning and comparison.
- Model revision if initial performance is poor.
- Reportable technical outputs.

Codex should pause only when:

- The research goal is too ambiguous to operationalize.
- A required file is missing.
- An action is destructive or irreversible in a risky way.
- The task conflicts with repository rules.

Otherwise, Codex should proceed autonomously and explicitly record assumptions, data decisions, method choices, outputs, and workflow updates.

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

- Use the research goal and validated schema to frame the ML or statistical problem automatically when the objective is clear enough.
- Identify the prediction target, unit of analysis, temporal structure, leakage risks, and evaluation metric before training, and record assumptions when the user has not specified them.
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
