---
name: paper-completeness-auditor
description: Audit whether a paper product contains all required sections, evidence tables, citations, figures, metrics, appendix, and reproducibility statements.
---

# paper-completeness-auditor

## Required Checks

- Required sections: Title, Abstract, Keywords, Introduction, Literature Review, Method, Results, Discussion, Conclusion, References, Appendix.
- Required scientific content: research question, data description, literature review, methods, multi-model experiment, complete metrics, explainability, figures/tables, limitations, future work, citations, reproducibility, appendix.
- Required evidence: each section has a citation/evidence map; each result claim maps to an artifact.

## Failure Handling

Set status to `fail` when any required section or evidence table is missing. Route the missing item to `auto-repair-loop-agent` unless the fix needs user authorization.

## Outputs

- `paper_completeness_checklist.csv`
- `paper_completeness_audit.md`
- `missing_paper_items_for_repair.csv`
