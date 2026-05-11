---
name: concentration-cleaning-auditor
description: Audit and repair contaminant concentration cleaning before exposure assessment, belief-state modeling, optimization, or risk reporting.
---

# Concentration Cleaning Auditor

## When To Trigger

Use this skill before any downstream task that relies on concentration values, contaminant labels, exceedance flags, exposure assessment, or risk states.

## Checks

- Identify the target analyte using explicit analyte names, abbreviations, units, and source-field context.
- Do not classify an entire broad category as the target analyte by default.
- Preserve original detection text, initial value, retest value, final adopted value, numeric value, unit, parsing status, and parsing-failure reason.
- Parse regulatory limits into original text, numeric value, unit, comparison operator, and unit-inference status.
- Normalize concentration and limit units when possible before computing exceedance flags and exceedance multiples.
- Cross-check parsed exceedance against original judgment text and flag conflicts.
- Write unresolved or scientifically important parsing failures to an issue log.
- Regenerate downstream summaries, state features, reports, and figures when repaired concentration fields change.

## Output Requirements

Write an audit report, issue log, repaired-field summary, and downstream impact note into the active run package.
