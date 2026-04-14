# Decision Log

## 2026-04-13

### Use `AGENTS.md` for Codex instructions

Rationale: The user explicitly requested `AGENTS.md`, and this file provides a standard root-level place for repository guidance.

Impact: Codex should read `AGENTS.md` before performing future workflow tasks.

### Preserve raw data as immutable

Rationale: Scientific workflows need reproducibility and auditability.

Impact: Future transformations should write to `data/02_intermediate` or later layers instead of modifying `data/01_raw`.

### Keep the scaffold lightweight

Rationale: No dataset or research task has been selected yet.

Impact: Starter code and skills define interfaces and workflow expectations without implementing heavy analysis logic.
