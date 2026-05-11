---
name: word-docx-render-auditor
description: Audit DOCX render, pages, figures, tables, citations, placeholders, Chinese text, and fallback export status.
---

# word-docx-render-auditor

## Checks

- DOCX exists or fallback export is documented.
- Section order and required headings are present.
- Figures/tables/captions/references render in the expected locations.
- Chinese text is readable, no mojibake, no unresolved placeholders.
- Page render or conversion fallback is recorded.

## Outputs

- `docx_render_qa.md`
- `docx_placeholder_scan.csv`
- `word_repair_items.csv`
