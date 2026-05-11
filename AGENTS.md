# AGENTS.md

## Purpose

workflow1 is a Codex-assisted Research Operating System scaffold for scientific workflows. It supports data intake, schema profiling, validation, cleaning plans, task inference, model/method registry selection, quality gates, explainability planning, reporting, and reproducibility packaging.

This public repository is framework-only. It must not contain real datasets, private research outputs, API keys, Zotero secrets, local corpora, or historical project state.

## Default Operating Rules

1. Read `README.md`, `START_HERE.md`, `project_state/current_focus.md`, `project_state/next_step.md`, and relevant registry/recipe files before major workflow work.
2. Inspect schemas and metadata before reading full datasets.
3. Keep `data/01_raw/` immutable.
4. Write generated outputs into run packages or local output directories that are ignored by Git.
5. Record durable workflow decisions in `project_state/` only after removing private identifiers.
6. Before any public push, run the GitHub release cleanup scan and verify no private data remains.

## Product Mode Contract

When a user says:

```text
启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。
```

workflow1 should infer target structure and task type from the goal and data profile, then route through:

```text
input contract -> task understanding -> data understanding -> research planning
-> literature evidence -> method/model selection -> baseline and comparison
-> metrics -> explainability -> figure/table planning -> quality gates
-> auto repair -> reproducibility packaging
```

Do not ask the user to choose a model first when the research goal and data profile are sufficient.

## Data And Output Safety

- Never modify raw data in place.
- Do not commit real `.csv`, `.xlsx`, `.jsonl`, model weights, pickles, rendered documents, run packages, cache folders, or private notes.
- Keep secrets in environment variables or local ignored files.
- Zotero writeback must use an authorized MCP/API path, never direct SQLite edits.
- External plugins, API keys, large dependencies, paid access, global environment changes, and unknown third-party code require explicit authorization.

## GitHub Release Cleanup

The workflow includes a public-release cleanup stage:

```powershell
python -m workflow1 --stage github-release-cleanup-scan
python -m workflow1 --stage github-release-cleanup --backup-to "D:\桌面\workflow1_private_backup_YYYYMMDD_HHMMSS" --apply --keep-synthetic-example
```

The backup directory must be outside the repository. The cleanup manifest must stay in that external backup directory and must not be committed.

## Language

Use the user's language for interaction. Chinese-first output is appropriate when the data, project context, or user request is Chinese. Preserve source field names and technical terms when traceability matters.
