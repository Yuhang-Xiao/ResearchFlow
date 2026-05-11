# EDA Generator

## When To Use

Use this skill after schema profiling, validation, and cleaning when exploratory summaries, diagnostic plots, or analysis-ready overview tables are needed. In goal-driven autonomous mode, run EDA guided by the research objective.

## Inputs

- Cleaned or primary dataset.
- Schema notes.
- Research question, if available.
- Optional grouping, time, or target variable.

## Outputs

- Summary tables.
- Missingness and distribution diagnostics.
- Initial figures.
- EDA notes and recommended follow-up checks.

## Recommended Workflow

1. Confirm the data layer is appropriate for EDA.
2. Generate descriptive summaries before complex plots.
3. Inspect missingness, duplicates, ranges, category cardinality, and outliers.
4. Create focused visualizations tied to the research question.
5. Save tables in `reports/tables` and figures in `reports/figures`.
6. Continue to problem framing or method selection when the research objective is clear.
7. Update `project_state/next_step.md` with the next analysis step.
