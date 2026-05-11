---
name: zotero-library-searcher
description: Local workflow1 skill for safe audit, explanation, evidence mapping, or planning. It is Chinese-first, metadata-only by default, and preserves experimental boundaries.
---

# zotero-library-searcher

## Use

Use when the task requires this capability in DQN/modeling/reporting/literature/external-reference workflows.

## Rules

- Do not modify `data/01_raw`.
- Do not run unknown external code.
- Do not install large dependencies or use API keys without approval.
- Do not write Zotero databases without explicit authorization.
- Keep GitHub/Hugging Face as engineering references unless backed by literature or official documentation.
- Mark unverified settings as `experimental assumption`.

## Outputs

Write CSV/Markdown outputs into the active run package and update project_state after durable work.
