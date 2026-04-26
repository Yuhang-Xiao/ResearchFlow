---
name: goal-driven-research-orchestrator
description: Route one-line research launch commands into the workflow1 scientific workflow, using project memory, references, raw inventory, and relevant skills before executing stages.
---

# Goal-driven Research Orchestrator

## When To Trigger

Use this skill when:

- The user says “启动自动科研流程”.
- The user says “启动花生风险监管流程”.
- The user provides raw data plus a research goal.
- The user says “继续上次任务”.
- The user gives a one-line goal that implies data cleaning, modeling, visualization, reporting, simulation, optimization, or project continuation.

## First Files To Read

After trigger, read:

1. `START_HERE.md`
2. `project_state/project_memory.md`
3. `project_state/run_protocol.md`
4. `project_state/current_focus.md`
5. `project_state/next_step.md`
6. `project_state/decision_log.md`
7. `project_state/lessons_learned.md`
8. `project_state/conversation_handoff.md`
9. `references/processed_summaries/`
10. raw data inventory from `data/01_raw`
11. relevant files under `references/`
12. relevant skills under `.agents/skills/` and `skills/`

## Default Flow

1. Reference reading.
2. Intake.
3. Validation.
4. Cleaning plan and cleaning.
5. Label engineering.
6. Concentration extraction.
7. Risk panel construction.
8. EDA.
9. Model framing.
10. Baseline modeling.
11. Tuning and comparison.
12. Simulation / optimization feasibility.
13. Visualization.
14. Summary report.
15. Project memory update.
16. Conversation handoff.

Only execute stages that are appropriate, implemented, and requested by the user goal. Do not treat planning as actual cleaning.

## Before Downstream Modeling

Before MOE/EDI, POMDP, belief-MDP, DQN, formal visualization, or any downstream model task, first use `upstream-output-auditor` and, when concentration or contaminant labels matter, `concentration-cleaning-auditor`.

Do not assume previous outputs are correct. Verify cleaned data, concentration tables, count panels, dictionaries, Beta-Binomial states, belief-MDP features, and reports. If omissions, parsing failures, label conflicts, stale counts, or report/data mismatches are found, repair and regenerate affected artifacts before continuing. Block formal DQN when unresolved upstream concentration, AFB1 label, count panel, or belief-state problems remain.

For DQN, POMDP, belief-MDP, constrained RL, or safe RL tasks, first invoke and follow `document-governed-modeling`, `zotero-literature-auditor`, `environment-auditor`, and `dqn-readiness-auditor`. Do not set formal state, action, reward, constraints, transition, or training hyperparameters until the user confirms missing parameters. Previous sandbox DQN outputs are not formal specifications.

## Stop Conditions

Before stopping, apply the Auto-Repair and Stop Policy below. Pause and ask the user only when:

- Required raw data is missing.
- The research goal is completely non-operational.
- Core fields cannot be identified at all.
- A required dependency is missing and cannot be substituted or downgraded.
- The action would modify or destroy raw data.
- The workflow requires an explicit ethics, compliance, privacy, or sensitive-data decision.

## Auto-Repair and Stop Policy

### Default Auto-Repair Problems

During full workflow execution, do not stop immediately for lightweight dependency, path, chart, table-rendering, sheet-name, output-directory, encoding, or ordinary dtype conversion problems. First attempt a reasonable repair or downgrade:

- Replace missing `tabulate` with an internal Markdown table generator.
- Replace missing `matplotlib` or `seaborn` with SVG, CSV summaries, Markdown tables, or another lightweight output.
- For missing `openpyxl`, `python-docx`, or `pypdf`, use an available parser, workbook/sheet inspection, zip/XML extraction, text fallback, or clearly recorded degraded reading when valid.
- For Chinese paths, spaces, or special characters, use `pathlib`, relative paths, directory scanning, and filename matching.
- For unexpected Excel sheet names, list sheets and choose the most reasonable sheet based on headers and row counts.
- Create missing output directories automatically.
- If XLSX, PNG, or another single output format fails, write a substitute such as CSV or SVG.
- If a non-critical figure fails, continue the core tables/reports and record the skipped figure.
- For lightweight code errors, encoding errors, path errors, missing-directory errors, and ordinary dtype conversion errors, try 1-3 fixes before stopping.

### Repair Requirements

When repairing, protect `data/01_raw`, do not skip core scientific results silently, and record the original error, the repair or downgrade used, whether results were affected, and whether later manual review is needed.

### Must-Stop Problems

Stop only when raw data are missing or unreadable; a required research plan is missing and indispensable; critical fields are completely unidentifiable; API keys, login, paid access, external database permission, Zotero/MCP/manual configuration are required; critical external parameters such as consumption, population, BMDL, budget, cost, or capacity are missing; an action may overwrite raw data; competing cleaning choices would materially change conclusions; auto-repair would produce unreliable results; or memory/compute limits cannot be handled by chunking, degradation, or sampling.

### Error Logging

Every auto-repair or downgrade must be written to the task report or `reports/*_error_log.md`. At task end, update `project_state/lessons_learned.md`, and update `project_state/decision_log.md` when the repair changes later workflow decisions.

## Output Rules

- Use Chinese-first reports and final summaries.
- Preserve technical terms in English when appropriate.
- Do not blindly translate original Chinese field names.
- Never write derived data to `data/01_raw`.
- Save outputs under the appropriate `data`, `reports`, `experiments`, or `references/processed_summaries` folder.
- Update `project_state` after durable work.

## End-of-Task Organization

After every substantive task, call `whole-workspace-organizer` or perform a whole workspace organization check. 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。


## Run Package Requirement

Before every substantive task, call `run-package-manager` to create the task work package. After the task, call `whole-workspace-organizer` or run a whole workspace organization check. 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。

## Run Package And Cleanup Requirement

任务开始前调用 `run-package-manager` 创建任务工作包；任务结束后调用 `whole-workspace-organizer` 做全目录整理检查。以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。
