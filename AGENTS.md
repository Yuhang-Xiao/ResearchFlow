# AGENTS.md

## Project Purpose

This repository is a general-purpose scientific workflow scaffold for Codex. It is designed to support research tasks such as raw data intake, schema inspection, data cleaning and matching, validation, exploratory data analysis, ML problem framing, method selection, baseline modeling, result comparison, visualization, reporting, and iterative workflow updates.

Do not assume a domain, dataset, model type, or final report format until the user or project state makes it clear.

## Default Workflow Order

1. Read `project_state/current_focus.md`, `project_state/next_step.md`, `project_state/roadmap.yaml`, `project_state/decision_log.md`, and this file.
2. Confirm the task scope from the user request and local project state.
3. Route the task to the relevant skill or pipeline area.
4. Inspect file names, schemas, and metadata before reading full datasets.
5. Perform the next useful workflow step under the goal-driven autonomous execution policy.
6. Validate outputs before using them downstream.
7. Save generated outputs under the appropriate `data`, `reports`, or `experiments` folder.
8. Update project state files when decisions, outputs, or next steps change.

Recommended workflow progression:

```text
intake -> schema profiling -> cleaning/matching -> validation -> EDA
-> ML problem framing -> method selection -> baseline modeling
-> evaluation/comparison -> visualization -> reporting -> workflow update
```

Currently implemented runnable stages:

- `workflow1 --stage intake`: scans supported raw files and writes schema inventory outputs.
- `workflow1 --stage validation`: runs lightweight raw data validation summaries.
- `workflow1 --stage cleaning-plan`: generates a Chinese cleaning plan from validation findings.

`cleaning-plan` only creates recommendations. It must not modify raw data or create cleaned datasets.

## One-line Launch Policy

When the user uses a short command such as “启动自动科研流程”, “继续上次任务”, or “启动花生风险监管流程”, Codex should not ask the user to repeat a long prompt. Codex should automatically read:

- `START_HERE.md`
- `project_state/project_memory.md`
- `project_state/run_protocol.md`
- `project_state/current_focus.md`
- `project_state/next_step.md`
- `project_state/decision_log.md`
- `project_state/lessons_learned.md`
- `project_state/conversation_handoff.md`
- `references/`
- relevant skills under `.agents/skills/` and `skills/`

Then Codex should plan and execute according to the current raw data, research plan, project memory, implemented stages, and user constraints.

## Project Memory Policy

After each durable task, Codex must update the following when applicable:

- `project_state/project_memory.md`, if long-term rules or project understanding changed.
- `project_state/lessons_learned.md`, if new cleaning, modeling, literature, visualization, or workflow lessons emerged.
- `project_state/conversation_handoff.md`, if the task is complex or the conversation may be resumed later.
- `project_state/next_step.md`.
- `project_state/changelog.md`.
- `project_state/decision_log.md`.

Do not store secrets, private identifiers, or unnecessary raw-data details in project memory.

## Reference and Literature Policy

Before major data processing, model setup, optimization modeling, or report writing, Codex should check:

- `references/`
- `references/processed_summaries/`
- `D:\桌面\codex\zotero`

If literature support is needed, prioritize full PDFs or existing deepread notes over abstracts only. If no suitable local literature exists and the task requires evidence, Codex may search the web for authoritative literature, official standards, or GitHub open-source methods. User explicit instruction overrides references, and actual dataset evidence overrides generic reference suggestions.

## Skill Discovery and Improvement Policy

When existing skills are insufficient, Codex should:

- Prefer searching GitHub for well-maintained open-source skills, agents, workflows, and research automation projects with clear README files, licenses, and adoption signals.
- Evaluate whether the project fits workflow1.
- Absorb methods and structure only; do not blindly copy uncontrolled code.
- If no suitable option exists, create a lightweight local skill.
- Record new or modified skills in `project_state/decision_log.md` and `project_state/changelog.md`.

## Default Short Commands

- “启动自动科研流程”: read memory, references, raw inventory, and route the full workflow.
- “启动花生风险监管流程”: start the peanut/AFB1 food-safety risk monitoring workflow.
- “继续上次任务”: read `project_state/conversation_handoff.md` and `project_state/next_step.md`.
- “只做清洗”: run reference reading, intake, validation, cleaning plan, and cleaning only when requested.
- “只做建模”: use existing cleaned/model input data and run model framing/modeling stages only.
- “只做可视化”: use existing outputs or requested tables to plan and create figures.
- “读取文献并更新方法”: inspect references, Zotero/deepread notes, and update method memory.
- “生成交接文件”: update `project_state/conversation_handoff.md`.

## Language Policy

- Adapt automatically to the language used in the raw data.
- If raw data, column names, sheet names, or metadata are mainly in Chinese, use Chinese-first mode when reading and interpreting them.
- Unless the user explicitly specifies otherwise, use Chinese as the default interaction language.
- Main written responses and reports to the user should be in Chinese by default.
- Write default repository outputs in Chinese, including schema inventories, validation proposals, validation reports, cleaning logs, data dictionaries, variable maps, and technical analysis summaries.
- Keep original source field names unchanged, especially Chinese column names.
- Algorithm names, model names, package names, parameter names, code terms, and evaluation metrics may remain in English when appropriate.
- When needed, provide bilingual terminology, but keep the main document language Chinese by default.
- If the user explicitly specifies a language for a deliverable, follow the user's instruction for that deliverable.
- If no explicit language is specified, default to Chinese while preserving source field names and allowing appropriate technical terms to remain in English.

## Language Priority Rule

Language instructions are resolved in this order:

```text
user explicit instruction > task-specific requirement > default repository language policy
```

## Language Implementation Guidance

- When generating mixed-language outputs, keep terminology consistent across files and responses.
- Do not translate column names blindly if that may break code, joins, mappings, or traceability to source data.
- When needed, provide bilingual field mapping or terminology, but preserve original source field names.

## Reference Document Policy

- The repository may contain user-provided reference documents under `references/`.
- Before major data cleaning, modeling, simulation, optimization, or visualization tasks, Codex should inspect relevant reference documents if they exist.
- Codex should not assume every reference applies automatically.
- Codex should extract actionable guidance and summarize it in Chinese.
- Codex should preserve original technical terms, model names, algorithm names, package names, metrics, and official standard names when appropriate.
- User explicit instruction overrides reference documents.
- Actual dataset evidence overrides generic reference suggestions when there is a conflict.
- If reference documents are too long, unreadable, scanned, encrypted, or ambiguous, Codex should report the limitation and proceed with available information.
- Extracted durable guidance should be saved under `references/processed_summaries/` when it will guide future workflow stages.

## Goal-Driven Autonomous Research Execution Policy

When the user provides raw data plus a research goal, scientific objective, or modeling purpose, Codex should autonomously continue the downstream research workflow without waiting for approval at every major stage. Codex should use any optional constraints or preferences supplied by the user to shape the workflow and record assumptions explicitly.

Default workflow:

```text
schema profiling -> raw validation -> cleaning/matching -> cleaned dataset creation
-> EDA -> ML/statistical problem framing -> method selection -> baseline model
-> comparison/tuning -> model revision if needed -> output generation -> workflow update
```

Codex should use the raw dataset and the stated research goal together to decide:

- The data cleaning strategy.
- Which variables are likely identifiers, dates, targets, metadata, or candidate features.
- Whether the task is classification, regression, time series, clustering, anomaly detection, optimization, or another research workflow.
- Which baseline and advanced methods are appropriate.

Codex should automatically perform:

- Data cleaning and preprocessing.
- Cleaned dataset creation.
- Technical data summaries.
- Formal EDA.
- Model framing.
- Model selection.
- Baseline modeling.
- Tuning and comparison.
- Model revision if initial performance is poor.
- Reportable technical outputs.

Codex should pause only when:

- The research goal is too ambiguous to operationalize.
- A required file is missing.
- An action is destructive or irreversible in a risky way.
- The task conflicts with repository rules.

Otherwise, Codex should proceed autonomously and explicitly record assumptions, data decisions, method choices, outputs, and workflow updates.

## Auto-Repair and Stop Policy

### Default Auto-Repair Problems

In later scientific workflow tasks, Codex should first try to solve the following problems autonomously instead of stopping immediately to ask the user:

- Missing lightweight Python packages when an existing dependency or standard-library substitute is available.
- Missing common lightweight dependencies such as `tabulate`, `matplotlib`, `seaborn`, `openpyxl`, `python-docx`, or `pypdf`.
- Unavailable charting libraries; use pure Python, CSV summaries, SVG, Markdown tables, or another lightweight substitute.
- Markdown table rendering failures; use an internal table-rendering helper.
- Word/PDF Chinese path passing failures; use directory scanning, relative paths, filename matching, or `pathlib`.
- Excel sheet-name mismatches; list sheets and choose the most reasonable sheet from file evidence.
- Missing output directories; create them automatically.
- Chinese filenames, spaces, or special characters causing path errors; switch to safe path handling.
- One output format failing; write an alternative such as CSV instead of XLSX, or SVG instead of PNG.
- Non-critical figure generation failures; skip that figure, continue core outputs, and record the omission.
- Optional dependencies missing; run a degraded workflow when valid and record the downgrade reason.
- Lightweight code errors, encoding errors, path errors, missing-directory errors, and ordinary dtype conversion errors; attempt a repair before continuing.

### Auto-Repair Requirements

When one of the above issues appears, Codex should:

1. Decide whether the issue is auto-repairable.
2. Try 1-3 reasonable fixes before stopping.
3. Never modify or damage raw data.
4. Never skip core scientific outputs silently.
5. If using a substitute or degraded path, record the original error, repair method, effect on results, and whether later manual review is needed.
6. Stop and ask the user only if repair fails or the repair would affect core scientific conclusions.

### Must-Stop Problems

Codex should stop and ask the user only for problems such as:

- Raw data files are missing or unreadable.
- A research plan document is missing and the task strictly depends on it.
- Critical fields are completely unidentifiable and no reasonable substitute exists.
- API keys, account login, paid access, external database permissions, or manual authorization are required.
- Zotero, MCP, or literature-library connection fails and must be manually configured by the user.
- Missing critical external parameters that the user must supply, such as consumption, population, BMDL, budget, cost, or capacity limits.
- An operation could overwrite or damage `data/01_raw`.
- Multiple cleaning choices would lead to materially different scientific conclusions and the user must choose.
- Auto-repair would introduce clearly unreliable results.
- Memory or compute resources are insufficient and cannot be reasonably handled by chunking, degradation, or sampling.

### Error Logging

Every task should maintain or update a task error log such as `reports/*_error_log.md`, update `project_state/lessons_learned.md`, and update `project_state/decision_log.md` when the issue affects later workflow decisions.

Error logs must distinguish:

- Automatically repaired errors.
- Degraded-but-continued errors.
- Unresolved errors requiring user action.

## Upstream Verification Before Downstream Modeling Policy

1. Before entering any downstream modeling, DQN, POMDP, belief-MDP, MOE/EDI, or formal visualization step, Codex must first check whether upstream data products are reliable.
2. Codex must not directly trust previous-stage outputs without quality verification.
3. If the current task depends on any of the following files, verify them first: cleaned main table, concentration clean table, count panel, label dictionary, variable dictionary, Beta-Binomial belief state, and belief-MDP state features.
4. If upstream outputs contain omissions, inconsistent fields, cleaning logic errors, parsing failures, label conflicts, numeric anomalies, or report-vs-data mismatches, Codex must clearly identify the problem, decide whether it is auto-repairable, repair it when possible, regenerate affected derived files, update reports, update the error log, update project state, and not continue into downstream modeling with known errors.
5. Stop and ask the user only when a fix requires external parameters, human scientific judgment, API keys, account permissions, raw-data supplementation, or when multiple repair choices would lead to materially different scientific conclusions.
6. Simple code errors, path errors, missing lightweight dependencies, minor field-name mismatches, incomplete regex parsing, inconsistent unit spellings, chart output failures, and Markdown table failures must be repaired autonomously under the Auto-Repair policy.

Long-term rule: any downstream model task must start with upstream output verification. If upstream omissions or errors are found, Codex should repair them and rebuild affected artifacts before continuing; Codex must not carry known upstream errors into downstream models.

## Concentration Cleaning Must-Pass Checks

Before entering MOE/EDI, POMDP, or DQN, concentration cleaning must pass these checks:

1. AFB1-related record identification must cover common variants including `黄曲霉毒素B₁`, `黄曲霉毒素B1`, `黄曲霉毒素B`, `黄曲霉毒素 B₁`, `黄曲霉毒素B₁μg/kg`, `黄曲霉毒素B₁，µg/kg`, initial/retest descriptions containing `黄曲霉毒素B1`, and reasonable variants containing `黄曲霉`, `AFB`, `B₁`, or `B1`.
2. Codex must not treat all `生物毒素` records as AFB1 by default.
3. `检测数值` should be parsed as fully as possible, preserving the original value, initial-test value, retest value, final adopted value, numeric value, unit, parsing status, and parsing-failure reason.
4. `法规限制` should be parsed as fully as possible, preserving original limit text, numeric limit, limit unit, comparison operator, and whether the unit was inferred from context.
5. For AFB1, concentration units should preferentially be normalized to `μg/kg`.
6. `是否超标` must not rely only on `判定结果`; it should preferentially compare `最终采用浓度值` against `法规限量_数值` after unit normalization, then cross-check against the original judgment result.
7. `超标倍数` must be calculated from concentration and limit values after unit normalization.
8. Records that cannot be parsed but may be important must be written to the issue log and must not be silently discarded.
9. Statistical counts in reports must match actual CSV/XLSX outputs.
10. If the concentration table is repaired, Codex must decide whether concentration distribution summaries, EDA, modeling feasibility, Beta-Binomial outputs, or belief-MDP state features need regeneration.

## Downstream Blocker Rule

If concentration cleaning, AFB1 labels, the count panel, or belief states contain unresolved core problems, Codex must block formal DQN work and explicitly record the blocker and repair plan in `project_state/next_step.md`.

## Data Handling Rules

- Do not analyze datasets unless the user asks for analysis or the current task clearly requires it.
- Treat `data/01_raw` as immutable. Do not edit raw data in place.
- Intake, validation, and cleaning-plan stages may inspect raw metadata and table-level quality signals when explicitly requested, but they must not rewrite raw files.
- Write derived files to the next appropriate layer:
  - `data/02_intermediate` for parsed or lightly transformed data.
  - `data/03_primary` for cleaned analysis-ready tables.
  - `data/04_feature` for engineered features.
  - `data/05_model_input` for final modeling matrices or splits.
- Prefer metadata and schema inspection before loading entire large files.
- Record data assumptions, joins, filters, exclusions, and validation failures.
- Avoid storing secrets, credentials, tokens, or private identifiers in committed files.
- When handling sensitive or human-subject data, minimize exposure, use aggregate outputs where possible, and ask for clarification before exporting risky artifacts.

## Modeling Rules

- Use the research goal and validated schema to frame the ML or statistical problem automatically when the objective is clear enough.
- Identify the prediction target, unit of analysis, temporal structure, leakage risks, and evaluation metric before training, and record assumptions when the user has not specified them.
- Start with transparent baselines before advanced methods.
- Separate model input construction from model training.
- Use reproducible splits when possible and record random seeds.
- Compare models against baselines with the same data splits and metrics.
- Do not overfit the scaffold with heavy training logic until a real task requires it.

## Document-Governed DQN Policy

1. DQN, POMDP, belief-MDP, constrained RL, safe RL, and reinforcement-learning tasks must first read the user research plan, model specification documents, project state, and relevant Zotero/deepread notes.
2. User documents have higher priority than Codex autonomous judgment, default machine-learning practice, previous sandbox prototypes, and external open-source patterns.
3. Codex must not independently set formal DQN state, observation, action, reward, constraints, transition logic, training hyperparameters, network structure, baselines, or evaluation metrics.
4. Any key parameter missing from the user documents must be listed in a parameter confirmation table and wait for user confirmation before formal DQN training.
5. Zotero notes containing `?????`, replacement characters, or obvious mojibake must not be used as formal evidence; Codex must trace the PDF/full text/official source or record the note as unusable.
6. Before formal DQN, Codex must audit Python and torch environments. It must not downgrade to sklearn only because the default Python environment lacks torch.
7. The earlier path `D:\anaconda3\envs\myevn1\python.exe` is incorrect and must not be used for formal DQN.
8. Without confirmed parameters and a confirmed torch-capable interpreter, Codex may only produce readiness reports, literature audits, environment audits, model-spec extraction, and parameter confirmation tables; it must not run formal DQN.

## DQN Environment Policy

1. Formal DQN tasks must prefer `D:\anaconda3\envs\myenv1\python.exe`.
2. All DQN environment installation, validation, smoke-test, and training commands must explicitly call `D:\anaconda3\envs\myenv1\python.exe`.
3. Do not use default `python`, base Conda, or `D:\anaconda3\envs\myevn1\python.exe` for formal DQN work.
4. Current validated NVIDIA runtime capability is CUDA 12.6; PyTorch for formal DQN should use the CUDA 12.6 / `cu126` build.
5. Do not install or use PyTorch `cu130` for formal DQN unless the NVIDIA driver is upgraded and the environment is revalidated.
6. Formal DQN must pass a torch GPU smoke test before training.
7. If GPU is unavailable, explicitly record CPU downgrade and wait for user confirmation before formal DQN training.

## Run Package First Policy

1. 每次实质性科研任务开始前，必须创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
2. 本轮任务产生的所有文件必须优先写入该任务工作包。
3. 标准目录只保存 canonical/latest 和 pipeline 必需文件。
4. 不允许把任务结果直接散落到 `reports/`、`data/04_feature/`、`experiments/` 根目录。
5. 如果某个结果需要被后续流程读取，可以同时复制到标准目录作为 canonical 文件。
6. 每个任务工作包必须包含 README 和 manifest。
7. 每次任务完成后必须更新 `outputs/_index/run_index.md`、`outputs/_index/run_manifest.csv`、`outputs/_index/latest_canonical_outputs.yaml`、`project_state/artifact_index.md` 和 `project_state/workspace_structure.md`。
8. 无法归属但唯一的文件进入 `outputs/_待复核/`。
9. hash 完全重复的文件应删除重复副本并记录。
10. 新对话继续任务时，应先读取最新 `run_index.md` 和 `conversation_handoff.md`。

## Whole Workspace Cleanliness Policy

1. 工作目录必须长期保持整洁。
2. 根目录只保留核心入口文件和一级功能目录。
3. 每次任务结束后必须执行全工作目录整理检查。
4. 所有任务产物必须进入任务工作包。
5. 标准目录只保留 canonical 和 pipeline 必需文件。
6. 历史文件必须进入对应任务工作包或待复核目录。
7. 重复文件必须删除重复副本。
8. 唯一文件必须保护，不得删除。
9. `data/01_raw` 永远不可修改、删除、重命名。
10. 删除动作只允许用于重复、缓存、临时、空文件和已确认无价值文件。

## Workflow Self-Improvement Policy

1. 当用户要求“优化工作流”“升级工作流”“让 Codex 自己找 skill”“搜索 GitHub 改进 workflow”“self-improve workflow”“workflow upgrade”时，Codex 必须调用 `workflow-self-improvement-scout`。
2. Codex 应自动扫描当前 workflow1 的 skills、recipes、model registry、orchestration code、project_state、references、Zotero integration、CLI 和 run package 机制。
3. Codex 应联网搜索 GitHub 和开源社区，寻找可升级当前 workflow 的 skill、agent、MCP、AutoML、科研自动化、Zotero、PDF 阅读、实验追踪、可视化、报告写作和 AutoResearch 机制。
4. Codex 不得盲目安装外部代码，不得运行未知第三方脚本。
5. Codex 应优先把外部项目的思想转化为本地轻量 skill、recipe、registry 或 stub。
6. 低风险本地升级可以自动执行，包括新增本地 SKILL.md、workflow recipe、model registry 条目、轻量 Python stub、README/prompt/project_state 更新、报告和 dry-run。
7. 高风险升级必须进入 approval queue，等待用户确认。
8. 每次升级必须写入 `workflow_improvement/improvement_ledger.csv`，并生成任务工作包。
9. 每次升级后必须执行 dry-run 和 skills-doctor。
10. 每次实质性科研任务结束后，Codex 应评估是否有 workflow 改进经验需要写入 self-improvement backlog。

## External Plugin Approval Policy

以下内容必须等待用户确认：

- 安装 MCP 或外部插件。
- 修改 Zotero 数据库。
- 使用 API key。
- 安装大型依赖。
- 启动长期后台服务。
- 全局修改环境。
- clone 并运行未知外部代码。
- 修改正式模型参数。
- 删除唯一文件。

## Output Rules

- Put figures in `reports/figures`.
- Put tables in `reports/tables`.
- Put Quarto or report drafts in `reports/quarto`.
- Put experiment artifacts under `experiments/baselines`, `experiments/advanced`, or `experiments/comparisons`.
- Keep outputs named with enough context to be traceable.
- Prefer lightweight, text-readable summaries for project state and decision records.
- Make final responses concise and include what changed, where it lives, and the next recommended task.



## Project State Update Rules

Update project state files whenever a task changes the workflow, produces durable outputs, or makes a meaningful decision.

- `project_state/roadmap.yaml`: update phase status, milestones, or task ordering.
- `project_state/current_focus.md`: describe the active objective and constraints.
- `project_state/next_step.md`: keep one clear recommended next action.
- `project_state/changelog.md`: append dated entries for notable changes.
- `project_state/decision_log.md`: append dated decisions with rationale and impact.

Do not rewrite history casually. Append new entries unless the user asks for cleanup.

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

## Artifact Explanation Policy

Every durable task output must be accompanied by an explanation index. Codex must not only generate files; it must explain what each important artifact is, why it was generated, which inputs produced it, how to read it, what paper section it can support, whether it can support a formal conclusion, and what limitations or manual cautions remain.

Required outputs when figures, tables, model outputs, code, reports, DOCX, or literature artifacts are produced:

- `artifact_explanation_index.md`
- `figure_explanations.md`
- `table_explanations.md`
- `model_output_explanations.md`
- `code_explanations.md`
- `result_interpretation_guide.md`
- `artifact_to_evidence_map.csv`

Missing or unreadable artifacts must be recorded as `unable_to_verify`; Codex must not infer their contents.

## Figure/Table Interpretation Policy

Every figure and table must have a reading guide, data source, field or axis explanation, main finding, limitation, and paper-use status. A figure/table can support paper Results only when its source table is available, chart/table QA passes, and the result claim is mapped to evidence.

## Empty Chart Prevention Policy

Codex must detect blank charts, near-blank charts, all-zero charts, no-difference charts, malformed SVGs, and charts with missing source data. Blank axes-only main figures are not acceptable. If values are all zero or visually indistinguishable, Codex must generate an explanatory PNG or a replacement table that states whether zero means no violation, no observed difference, or missing data. Historical empty charts must be logged and must not be used in paper Results.

## PNG-First and Chinese Font Policy

Main figures should be exported as PNG by default. Chinese titles, labels, legends, captions, and explanatory text must render correctly. If the preferred font is unavailable, Codex must choose an available Chinese-capable fallback and record the font status in chart QA.

## Code Explanation Policy

Each key script or generated code artifact must have code explanation covering purpose, input files, output files, dependency libraries, core functions, main workflow, model/statistical logic, how to run, common errors, relation to paper/results, reproducibility status, and whether human confirmation is still needed.

## Model Setting Documentation Policy

Every model, including DQN, Q-learning, heuristic policies, XGBoost, Random Forest, LightGBM, Logistic Regression, time series, Bayesian models, Monte Carlo, and optimization models, must include a model setting document. The document must cover model purpose, input features/state, target/action/reward when relevant, constraints, transition/belief update when relevant, parameters, training process, evaluation metrics, baselines, result interpretation, literature basis, limitations, and experimental/formal status.

Model settings must come from local config, code, data outputs, project state, user documents, or verified literature. Unknown settings must be marked `未核验` or `experimental assumption`.

## Literature-Grounded Modeling Policy

Model state/action/reward/constraint/baseline/evaluation choices should be mapped to literature or local data evidence whenever possible. Unsupported choices must be labeled `experimental assumption`. Literature read status must be explicit: `full-text read`, `local deepread`, `abstract-level`, `metadata-only`, or `not accessible`. Garbled notes cannot support formal claims.

## Zotero Safe Writeback Policy

Codex must not directly modify Zotero SQLite databases unless the user explicitly approves that exact action. The default Zotero workflow is sidecar-first: generate clean UTF-8 Markdown notes, BibTeX, RIS, CSV import plans, duplicate-check notes, and writeback logs. Chinese notes must be checked for mojibake or replacement characters before use.

## Academic Paper Section Output Policy

Paper outputs must be section-based and evidence-based. Introduction, Literature Review, Method, Results, Discussion, Conclusion, Appendix, and integrated drafts must each include a section draft, evidence table, figure/table reference map, citation support table, quality audit, experimental/formal status marker, and DOCX export when requested. Word outputs must include readable headings, tables, figure/table captions, result interpretation, evidence mapping, and explicit claim boundaries.

## Result Interpretation Policy

Model outputs must not be delivered as only CSVs or charts. Codex must explain what each metric means, what higher/lower values imply, how models compare, whether training appears stable, whether reward hacking or non-convergence risk exists, whether constraints were respected, which results can enter paper Results, which remain exploratory, and what human confirmations remain.

## Workflow Self-Improvement for Missing Skills Policy

When a task exposes missing capabilities in explanation, artifact documentation, chart QA, table interpretation, model cards, data cards, experiment reports, citation verification, Zotero notes, reproducibility, reviewer-style audits, DOCX export, model explanation, RL/DQN audits, or baseline fairness, Codex must search for high-quality open-source methods or checklists, avoid running unknown code, adapt safe ideas into local skills/recipes/stubs, and place high-risk installs or plugins into the approval queue.

## Experimental Boundary Policy

Experimental, prototype, synthetic, unconfirmed, or weakly validated results must not be written as formal conclusions or policy recommendations. DQN/RL results remain experimental unless state, action, reward, constraints, transition, baselines, evaluation metrics, environment, literature support, sensitivity analysis, and user-confirmed formal parameters all pass the required gates.

## Output Explanation Co-location Policy

Output explanations must live beside the results they explain. `10_输出解释与索引/` is only a navigation and summary layer; it cannot replace detailed explanations in `02_表格输出/`, `03_图表输出/`, `04_报告输出/`, `05_模型与实验/`, `06_配置参数/`, `08_代码快照/`, or `09_论文输出/`.

Every result directory must include a local README or local explanation file that explains what the directory contains, what each important file is, which inputs generated it, how to read it, the main result, paper-use status, experimental/formal status, limitations, relationships to other outputs, and what the user should inspect first.

## Same-name Explanation Policy

Key artifacts should have same-name sidecar explanations whenever practical. Examples:

- `figure.png` and `figure.png.explanation.md`
- `table.csv` and `table.csv.explanation.md`
- `report.md` and `report.md.explanation.md`
- `paper.docx` and `paper.docx.explanation.md`
- `config.yaml` and `config.yaml.explanation.md`

If there are too many auxiliary files, the directory README must identify which files are core and which are support files, and `missing_local_explanations.csv` must record any important gaps.

## Directory README Explanation Policy

Each output directory in a task package must have a directory-level explanation README. The README must be useful in place: it must not simply say “see total index.” It should provide the minimum context needed to read that directory without reverse-searching through a centralized index.

## Code Deep Explanation Policy

Key model code must receive deep explanation, not just a script inventory. The explanation must cover script/module purpose, inputs, outputs, main functions/classes, workflow, model/statistical logic, how to run, reproducibility conditions, common errors, experimental boundary, formal TODOs, risks, and how users should read the code.

## DQN Code-to-Method Mapping Policy

DQN code must map to Method sections: state construction, action space, reward decomposition, constraints/action mask, transition or belief update assumptions, replay buffer or batch sampling, Q-network, target network, epsilon-greedy, training loop, Q-learning baseline, heuristic baselines, evaluation protocol, chart/report generation, and quality gates. Missing or implicit pieces must be labeled `未核验` or `experimental assumption`.

## Code-to-Output Mapping Policy

Code explanations must identify which code units generate which tables, figures, reports, model artifacts, configs, Word files, project indexes, and canonical synchronized outputs. This mapping should be written as `code_to_outputs_map.csv` or a model-specific equivalent.

## Explanation Index Is Not Enough Policy

A task fails explanation quality if explanations exist only in `10_输出解释与索引/`. Before finishing, Codex must check for local directory README files and same-name explanations for key artifacts. If local explanations are missing, Codex must create them or record the gap in `missing_local_explanations.csv`.
