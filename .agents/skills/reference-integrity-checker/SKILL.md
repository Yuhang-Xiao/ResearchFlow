---
name: reference-integrity-checker
description: Verify DOI/title/authors/year/venue/URL/read status before citations support formal claims.
---

# reference-integrity-checker

## Required Fields

DOI, title, authors, year, journal/conference, URL, read status.

## Gate Rules

- Citation failures cannot support formal claims.
- Metadata-only and abstract-only items must remain labeled.
- Paid/full-text gaps go to authorization plan, not invented evidence.

## Outputs

- `reference_integrity_check.csv`
- `citation_failure_log.md`
