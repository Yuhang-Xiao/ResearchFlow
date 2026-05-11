---
name: literature-evidence-chain-builder
description: Build literature-first evidence chain for background, methods, metrics, explainability, discussion, references, and Zotero sidecars.
---

# literature-evidence-chain-builder

## Required Evidence Families

Research background, domain literature, method literature, metric literature, explainability literature, reporting guidelines, result discussion literature.

## Rules

- Start literature evidence before modeling, not after results.
- Mark every item as `full-text`, `abstract-only`, `metadata-only`, or `not accessible`.
- GitHub/Hugging Face/official docs are engineering references and cannot replace peer-reviewed literature.
- Zotero outputs are sidecar-only unless the user authorizes real writeback.

## Outputs

- `literature_candidate_pool.csv`
- `literature_selected_core.csv`
- `section_citation_map.csv`
- `model_component_literature_map.csv`
- `references.bib`
- `references.ris`
