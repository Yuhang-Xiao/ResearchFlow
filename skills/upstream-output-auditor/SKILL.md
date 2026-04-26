---
name: upstream-output-auditor
description: Verify upstream workflow outputs before downstream modeling, simulation, MOE/EDI, POMDP, belief-MDP, DQN, or formal visualization. Use when Codex must compare raw data, cleaned data, feature tables, dictionaries, reports, Beta-Binomial belief states, and belief-MDP state features for consistency, omissions, parsing failures, label conflicts, numeric anomalies, or stale downstream artifacts.
---

# Upstream Output Auditor

## When To Trigger

Use this skill before any downstream modeling, MOE/EDI, POMDP, belief-MDP, DQN, formal visualization, or report finalization that depends on earlier workflow outputs.

Also use it when the user suspects previous outputs may contain omissions or errors.

## What To Check

- Required upstream files exist or can be regenerated from available inputs.
- Raw data, cleaned data, feature tables, and reports agree on row counts, key counts, label counts, and grouped totals.
- Cleaned main tables preserve traceability to raw rows and original Chinese fields.
- Concentration tables contain all records that should be included and no records that should be excluded.
- Count panels match cleaned data grouped by province, time, and supply-chain stage.
- Label dictionaries and variable dictionaries match actual output columns.
- Beta-Binomial belief states and belief-MDP state features are current relative to the count panel and AFB1 labels.
- Reports do not contain stale numbers that disagree with CSV/XLSX outputs.

## How To Compare Outputs

1. Inspect schema and row counts before full comparisons.
2. Recompute key metrics from source tables: total rows, AFB1 records, concentration-available records, noncompliance counts, exceedance counts, and grouped panel totals.
3. Compare recomputed metrics against saved tables and report summaries.
4. Check join/index keys such as row ID, province, year, month, year-month, and supply-chain stage.
5. Flag stale downstream artifacts when upstream repaired values change fields used by panels or belief states.

## Finding Omissions

Search raw and cleaned text fields for expected terms, variants, units, comparison operators, empty markers, and mixed-value patterns. Compare matched candidates against labels and parsed outputs to find false negatives, false positives, and records needing manual review.

## Repair Or Stop

Auto-repair lightweight issues such as field-name mismatches, regex omissions, unit spelling differences, dtype conversion, missing output folders, stale reports, and derived file regeneration. Stop only when raw data are unreadable, critical fields have no substitute, an API/permission/manual configuration is required, external parameters are missing, or competing repairs would change scientific conclusions.

## Required Records

Write findings to `reports/tables/*audit_findings.csv` or an equivalent table, write repair steps to `reports/*repair_log.md`, update affected reports and derived data, and update `project_state/decision_log.md`, `project_state/lessons_learned.md`, `project_state/next_step.md`, and `project_state/conversation_handoff.md`.
