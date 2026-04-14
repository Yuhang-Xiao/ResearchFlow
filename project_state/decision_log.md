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

## 2026-04-14

### Use gated semi-autonomous execution

Rationale: The user explicitly requested that Codex not continue automatically through major research stages.

Impact: Codex may autonomously perform low-risk preparatory work such as schema profiling, metadata inventory, raw validation, non-destructive inspection, draft plans, and lightweight review summaries. Codex must stop and request explicit approval before applying cleaning rules, creating cleaned datasets, running formal analysis, making modeling decisions, tuning or revising models, finalizing visualization designs, interpreting results, or drafting reports.

### Supersede gated execution with goal-driven autonomous execution

Rationale: The user explicitly changed the intended operating mode. When raw data plus a research goal are provided, Codex should run the full downstream research workflow autonomously unless blocked.

Impact: The previous gated semi-autonomous checkpoint policy is superseded. Codex should now proceed from raw data plus research goal through schema profiling, raw validation, cleaning/matching, cleaned dataset creation, EDA, problem framing, method selection, baseline modeling, tuning/comparison, model revision if needed, output generation, and workflow update. Codex should pause only for ambiguous goals, missing required files, risky destructive or irreversible actions, or repository rule conflicts, and should record assumptions explicitly.

### Archive prior test data and generated outputs before the next run

Rationale: The user requested a clean workspace for a fresh automated research run while preserving workflow infrastructure.

Impact: Previous raw datasets were moved to `data/99_archive`, and dataset-specific generated reports and tables were moved to `reports/archive/cleanup_2026-04-14`. Core workflow infrastructure remains in place.

### Reconstruct product categories using raw category plus product-name semantics

Rationale: The user requested a practical hierarchical category system that uses both `产品分类` and `产品名称`, not simple exact-string grouping.

Impact: The workflow created `新一级类`, `新二级类`, `新三级类`, `分类依据`, `分类置信度`, and `是否建议人工复核`, while preserving `原始产品分类` for traceability. The classification uses original category context, product-name semantics, food regulatory/category logic, and catering usage context where distinguishable. Ambiguous cases are flagged for manual review instead of being forced into high-confidence categories.
