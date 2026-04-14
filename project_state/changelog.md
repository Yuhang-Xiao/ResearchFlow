# Changelog

## 2026-04-13

- Initialized the repository scaffold for a general-purpose scientific workflow.
- Added Codex project instructions, starter configuration, project state files, reusable skill folders, and lightweight Python module stubs.
- Added a raw data schema inventory for the Excel workbook in `data/01_raw` and updated the recommended next step toward validation rule definition.

## 2026-04-14

- Updated repository instructions to use gated semi-autonomous execution with human approval at major research checkpoints.
- Added a gated autonomous research orchestrator skill.
- Updated project state to reflect that Codex may continue only through low-risk preparatory steps without approval.
- Set `FINAL_SiChuan_2023_ALL_DATA.xlsx` as the active raw dataset for the current task, created a new schema inventory, and created a new raw data validation proposal without executing cleaning, analysis, or modeling.
- Revised the repository to support goal-driven autonomous research execution from raw data plus a research goal through cleaning, EDA, modeling, comparison, output generation, and workflow updates.
- Updated orchestrator and related skills for autonomous continuation unless blocked by ambiguity, missing files, risky destructive or irreversible actions, or repository rule conflicts.
- Added lightweight orchestration helpers under `src/workflow1`.
- Cleaned the workspace for a fresh automated research run by archiving previous raw datasets under `data/99_archive` and prior dataset-specific generated outputs under `reports/archive/cleanup_2026-04-14`.
- Reconstructed and cleaned the product-category system for `FINAL_SiChuan_2023_ALL_DATA.xlsx` using `产品分类` and `产品名称`, generating a cleaned classification dataset, reusable mapping/taxonomy tables, per-category reports, and a master summary.
