---
name: zotero-literature-auditor
description: Audit Zotero library notes and PDFs before using literature for DQN, POMDP, belief-MDP, risk monitoring, MOE/EDI, or food safety modeling.
---

# Zotero Literature Auditor

## Checks

- Search Zotero project directories for relevant keywords and candidate notes.
- Detect `?????`, replacement characters, or mojibake in notes.
- Do not use garbled notes as formal evidence.
- If a note is garbled, trace the corresponding PDF or official source page.
- Record whether each paper has a PDF, whether full text was read, whether the note is garbled, and how the paper supports the model.

## Outputs

Write a literature inventory CSV, a literature audit report, and an encoding/PDF issue log.
