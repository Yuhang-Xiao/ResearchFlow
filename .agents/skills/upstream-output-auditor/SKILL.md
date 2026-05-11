---
name: upstream-output-auditor
description: Verify upstream workflow outputs before downstream modeling, simulation, optimization, or formal visualization.
---

# Upstream Output Auditor

Use this skill before downstream work depends on cleaned data, feature tables, dictionaries, reports, state features, or derived summaries.

## Checks

- Confirm source tables, cleaned tables, features, and reports are mutually consistent.
- Recompute key row counts, label counts, grouped totals, missingness, and numeric ranges from source artifacts.
- Flag stale outputs, parsing failures, label conflicts, inconsistent units, missing fields, and report-vs-data mismatches.
- Repair auto-repairable issues and regenerate affected downstream artifacts.
- Block downstream modeling when unresolved upstream defects would affect conclusions.
