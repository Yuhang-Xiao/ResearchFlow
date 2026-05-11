---
name: full-paper-product-writer
description: Generate a complete paper product with all required sections, evidence maps, references, appendix, and Word-ready structure.
---

# full-paper-product-writer

## Purpose

Turn validated research outputs into a complete paper product, not a stage report.

## Required Sections

Title, Abstract, Keywords, Introduction, Literature Review, Method, Results, Discussion, Conclusion, References, Appendix.

## Required Inputs

- Data card and lineage manifest.
- Target-structure and multi-task modeling plan.
- Model comparison, complete metrics, robustness, and explainability outputs.
- Figure/table plan, source tables, captions, and QA results.
- Section citation map and reference integrity table.

## Gate Rules

- Missing required sections fail the Full Paper Product Gate.
- Every Results claim must map to table, figure, model output, data lineage, or verified literature.
- Metadata-only literature cannot support formal claims.
- Predictive association must not be written as causal mechanism.
- If a required input is missing and no authorization is needed, create an auto-repair task.

## Outputs

- `full_paper.md`
- `full_paper.docx` or audited fallback
- `section_evidence_map.csv`
- `paper_completeness_checklist.csv`
- `citation_evidence_table.csv`
