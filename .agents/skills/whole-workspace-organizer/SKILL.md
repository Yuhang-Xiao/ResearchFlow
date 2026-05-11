---
name: whole-workspace-organizer
description: Scan, clean, deduplicate, classify, and index the ResearchFlow OS workspace while preserving raw data and canonical workflow files.
---

# Whole Workspace Organizer

## When To Use

Use this skill after durable workflow tasks, before public release checks, or whenever duplicate files, scattered outputs, or unclear workspace structure appear.

## Scan Scope

Inspect the repository root, `.agents/`, `.codex/`, `src/`, `tools/`, `references/`, `data/`, `reports/`, `experiments/`, `outputs/`, `archive/`, `workflow_recipes/`, `model_registry/`, `workflow_improvement/`, and `project_state/`.

## Cleanup Rules

- Preserve `data/01_raw/` and never modify raw data in place.
- Delete only exact duplicate files, cache files, temporary files, empty test residue, or files already backed up and confirmed safe to remove.
- Preserve unique code, configuration, reference documents, run manifests, and public template files.
- Route generated outputs to task run packages or ignored local output directories.
- Keep `.agents/skills/` as the single repo-scoped skill directory.

## Verification

After cleanup, run lightweight checks:

- `python -m workflow1 --stage launch`
- `python -m workflow1 --stage github-release-cleanup-scan`
- duplicate hash scan over tracked files
- private keyword and credential scan before public release

Record durable structural decisions in `project_state/` only when they are public-safe.
