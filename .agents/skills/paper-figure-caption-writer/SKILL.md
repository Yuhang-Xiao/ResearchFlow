---
name: paper-figure-caption-writer
description: Write paper-ready figure captions with data source, method, result, and limitation.
---

# paper-figure-caption-writer

## Purpose

Write paper-ready figure captions with data source, method, result, and limitation.

## Product-Mode Rules

- Treat `data_file + research_goal` as a product contract.
- Route all outputs into the active run package.
- Do not modify `data/01_raw`.
- Do not install dependencies, run unknown external code, use API keys, or write Zotero databases without approval.
- If a required gate fails and no authorization is needed, create a repair task instead of asking the user.
- Mark evidence status as `full-text`, `abstract-only`, `metadata-only`, or `not accessible`.
- Preserve predictive association vs causal mechanism boundaries.
