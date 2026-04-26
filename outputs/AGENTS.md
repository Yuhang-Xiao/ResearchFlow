

## Research Quality Gate Policy

After every durable scientific task, Codex must run or plan research quality gates covering data generation and derived-data lineage, table/report consistency, chart QA, model validation, multi-model comparison, baseline fairness, reward/convergence/constraint audit, citation verification, top-journal benchmarking, result claim guard, Reviewer 2 style self-audit, reproducibility, and workflow self-improvement review.

## Top-Journal Benchmarking Policy

Before and after generating methods, model settings, figures, tables, result interpretation, or paper sections, Codex must consult `references/top_journal_benchmark/`. If a paper was not read in full, mark it as `metadata-only` or `abstract-only`; never pretend full-text support exists.

## Literature Coverage and Citation Verification Policy

Every paper section must include a citation evidence table. DOI, title, authors, year, journal/conference, and URL must be verified where possible. Citation failures cannot support formal claims.

## Data Generation and Lineage Validation Policy

Every derived output must record input sources, transformation intent, row count, column count, key fields, units, missingness/anomaly/duplicate checks, and repair or issue logs. Each task package should include `data_lineage_manifest.csv` when data outputs are generated.

## Model Comparison and Baseline Fairness Policy

Every model run must include at least one simple baseline. Advanced models must compare against an interpretable control. RL/DQN must compare heuristic, Q-learning, random, historical, and risk-ranking baselines when applicable. All models must use consistent splits, budgets, constraints, and metrics.

## Reward-Convergence-Constraint Audit Policy

RL/DQN outputs must audit reward scaling, convergence, constraint violations, budget/capacity/minimum coverage assumptions, and whether parameters were user-confirmed. Unconfirmed or unconverged results remain prototype/experimental only.

## Chart/Table QA and PNG Output Policy

Every chart must have a source data table, nonblank output check, readable axes/labels, Chinese font handling when needed, and PNG/SVG output status. Every table must be checked against report numbers.

## Paper Section Evidence and DOCX Export Policy

Paper section generation must follow: benchmark -> outline -> evidence map -> Chinese draft -> DOCX/fallback export -> citation table -> citation verification -> result claim guard -> Reviewer 2 audit -> revision checklist.

## Result Claim Guard Policy

Every result claim must map to data, model, figure/table, or literature evidence. Experimental must not become formal; prototype must not become policy recommendation; synthetic parameters must be labeled; unverified literature cannot imply mainstream consensus; only quality-gate-passing results can enter paper Results.

## Reviewer-2 Style Self-Audit Policy

Before a result, figure, table, or paper section is treated as reportable, Codex must produce a critical audit of likely reviewer objections, missing controls, overclaiming, weak citations, and reproducibility gaps.

## Workflow Self-Improvement After Every Task Policy

At the end of each scientific task, Codex must consider whether errors, repeated frictions, chart/model/literature/citation/claim gaps, or new external tools justify updating AGENTS, skills, recipes, model registry, project memory, or approval queue. Codex should proactively search for useful skills/tools, but must not install high-risk plugins, MCP servers, APIs, large dependencies, or write Zotero databases without user confirmation.
