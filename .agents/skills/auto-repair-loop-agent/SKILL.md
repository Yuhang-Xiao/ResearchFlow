---
name: auto-repair-loop-agent
description: Run three-round repair loop and write redo logs.
---

# auto-repair-loop-agent

## Product-Mode Contract

Run at least three rounds: initial execution, quality-gate repair, and final paper/Word repair.

## Repair Without Asking When

Missing model comparison, missing metrics, missing SHAP/fallback explanation, blank figures, missing captions, incomplete paper sections, citation maps, unsupported claims, missing manifest, or missing reproducibility README can be repaired with existing local evidence.

## Stop Only For

Unreadable raw data, missing critical user scientific parameters, API keys, paid access, Zotero writeback, MCP/plugin/dependency installation, or human scientific judgment that changes conclusions.

## Required Logs

- `redo_log.csv`
- `failed_gate_summary.md`
- `repaired_items.csv`
- `remaining_issues.csv`
