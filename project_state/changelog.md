# Changelog

## 2026-04-24

- Added `Auto-Repair and Stop Policy` to `AGENTS.md`.
- Updated goal-driven orchestrator skills in `.agents/skills/` and `skills/` so lightweight dependency, path, table, chart, sheet-name, output-format, encoding, and dtype issues are repaired or downgraded before stopping.
- Added mirrored `error-recovery-and-auto-repair` skills under `.agents/skills/` and `skills/`.
- Updated project memory, run protocol, handoff, next step, lessons, changelog, and decision log with the long-term auto-repair rule.

## 2026-04-24

- Upgraded workflow1 into a one-line-launch semi-autonomous research workflow framework without processing real data or running models.
- Added `START_HERE.md` and `prompts/one_line_launchers.md` with reusable short launch commands.
- Added long-term project memory files: `project_state/project_memory.md`, `project_state/lessons_learned.md`, `project_state/run_protocol.md`, and `project_state/conversation_handoff.md`.
- Added repo-scoped skills under `.agents/skills/` and mirrored key skills under `skills/`.
- Added `goal-driven-research-orchestrator`, `skill-scout-and-upgrader`, and `project-memory-updater` skills.
- Added lightweight launcher support for `workflow1 --stage launch`, `continue`, `memory-update`, and `skill-scout`.
- Added `reports/skill_scout_report.md` after a web search for relevant open-source skills/workflows.
- Updated `AGENTS.md` with one-line launch, project memory, reference/literature, skill discovery, and default short-command policies.

## 2026-04-24

- Implemented the minimum runnable data preparation stages without starting real data cleaning, modeling, tuning, or visualization.
- Added `workflow1 --stage intake` to scan `.csv` and `.xlsx` files, inspect workbook sheets, headers, row counts, column counts, and write schema inventory artifacts.
- Added `workflow1 --stage validation` to produce lightweight missingness, duplicate row, key candidate, empty/Unnamed column, date-name candidate, mixed-type, and low-cardinality summaries.
- Added `workflow1 --stage cleaning-plan` to generate a Chinese non-destructive cleaning plan from validation findings.
- Updated CLI support for `--raw-dir`, `--reports-dir`, and environment overrides `WORKFLOW1_RAW_DIR` / `WORKFLOW1_REPORTS_DIR`.
- Updated workflow skills and `AGENTS.md` to reflect the implemented preparation stages and the planning-only nature of `cleaning-plan`.

## 2026-04-24

- Performed the first migrated-repository repair pass without starting dataset analysis, cleaning, modeling, tuning, or visualization.
- Added reproducible Python project metadata in `pyproject.toml` and a simple fallback dependency list in `requirements.txt`.
- Added the lightweight runnable workflow entrypoint `workflow1` / `python -m workflow1` with config loading, logging, stage routing placeholders, and graceful not-implemented handling.
- Added the top-level `references/` layer for future data-cleaning, modeling, visualization, literature, standards, notes, and processed Chinese summaries.
- Added `skills/reference-document-reader/SKILL.md` and lightweight reference-reading stubs under `src/workflow1/references`.
- Updated `AGENTS.md` and `skills/autonomous-research-orchestrator/SKILL.md` so future major workflow stages check relevant reference documents when present.
- Reset project state away from the previous Sichuan category reconstruction task and recorded that no active raw dataset is currently being analyzed.

## 2026-04-24

- Completed a repository readiness audit after migration to the new computer without starting dataset analysis, cleaning, modeling, tuning, or visualization execution.
- Added the Chinese audit report at `reports/readiness_audit_2026-04-24.md`.
- Added the machine-readable readiness checklist at `project_state/readiness_checklist_2026-04-24.yaml`.
- Updated `project_state/next_step.md` to prioritize repairing critical readiness blockers before any fresh automated research run.

## 2026-04-13

- Initialized the repository scaffold for a general-purpose scientific workflow.
- Added Codex project instructions, starter configuration, project state files, reusable skill folders, and lightweight Python module stubs.
- Added a raw data schema inventory for the Excel workbook in `data/01_raw` and updated the recommended next step toward validation rule definition.

## 2026-04-14

- Updated repository instructions to use gated semi-autonomous execution with human approval at major research checkpoints.
- Added a gated autonomous research orchestrator skill.
- Updated project state to reflect that Codex may continue only through low-risk preparatory steps without approval.
- Set `FINAL_SiChuan_2023_ALL_DATA.xlsx` as the active raw dataset for the current task, created a new schema inventory, and created a new raw data validation proposal without executing cleaning, analysis, or modeling.
- Revised the repository to support goal-driven autonomous research execution from raw data plus a research goal through cleaning, EDA, modeling, comparison, output generation, and workflow updates.
- Updated orchestrator and related skills for autonomous continuation unless blocked by ambiguity, missing files, risky destructive or irreversible actions, or repository rule conflicts.
- Added lightweight orchestration helpers under `src/workflow1`.
- Cleaned the workspace for a fresh automated research run by archiving previous raw datasets under `data/99_archive` and prior dataset-specific generated outputs under `reports/archive/cleanup_2026-04-14`.
- Reconstructed and cleaned the product-category system for `FINAL_SiChuan_2023_ALL_DATA.xlsx` using `产品分类` and `产品名称`, generating a cleaned classification dataset, reusable mapping/taxonomy tables, per-category reports, and a master summary.

## 2026-04-24

- 完成 PEANUT2023-20241 花生/AFB1 风险监管首轮自动科研流程，生成 schema、清洗主表、计数面板、浓度清洗表、EDA、图表、可行性报告和交接文件。

## 2026-04-24

- 基于 `data/04_feature/peanut_count_panel.csv` 实现 Beta-Binomial 信念更新原型，生成 belief-MDP 状态特征表、最新状态表、汇总表、配置和技术报告。

## 2026-04-24

- 基于 `data/04_feature/peanut_count_panel.csv` 实现 Beta-Binomial 信念更新原型，生成 belief-MDP 状态特征表、最新状态表、汇总表、配置和技术报告。

## 2026-04-24

- Added upstream verification and concentration-cleaning must-pass rules to `AGENTS.md` and skills.
- Created upstream/concentration auditor skills under `.agents/skills/` and `skills/`.
- Audited and repaired PEANUT concentration cleaning outputs, regenerated cleaned table, concentration table, concentration distribution summary, count panel, Beta-Binomial states, and belief-MDP state features.

## 2026-04-24

- 基于 `data/04_feature/peanut_count_panel.csv` 实现 Beta-Binomial 信念更新原型，生成 belief-MDP 状态特征表、最新状态表、汇总表、配置和技术报告。

## 2026-04-24

- Added upstream verification and concentration-cleaning must-pass rules to `AGENTS.md` and skills.
- Created upstream/concentration auditor skills under `.agents/skills/` and `skills/`.
- Audited and repaired PEANUT concentration cleaning outputs, regenerated cleaned table, concentration table, concentration distribution summary, count panel, Beta-Binomial states, and belief-MDP state features.

## 20260424

- 新增 Run Output Directory Policy 到 `AGENTS.md`。
- 创建 `outputs/20260424_MOE_EDI外部参数匹配与风险度量准备/` 并同步整理本轮 MOE/EDI 关键输出、报告、图表、日志和 README。
- 生成 BMDL 参数配置、消费量参数表、人口参数表、EDI/MOE 风险表、风险摘要和加入 MOE/EDI 的 belief-MDP 状态特征表。
- 重新生成 DQN 前置判断报告；本轮未运行 DQN。

## 20260424

- 新增 Run Output Directory Policy 到 `AGENTS.md`。
- 创建 `outputs/20260424_MOE_EDI外部参数匹配与风险度量准备/` 并同步整理本轮 MOE/EDI 关键输出、报告、图表、日志和 README。
- 生成 BMDL 参数配置、消费量参数表、人口参数表、EDI/MOE 风险表、风险摘要和加入 MOE/EDI 的 belief-MDP 状态特征表。
- 重新生成 DQN 前置判断报告；本轮未运行 DQN。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 20260424

- 完成全工作目录整理与规范化，创建 `outputs/20260424_全工作目录整理与规范化/`。
- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。
- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。
- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。

## 2026-04-24 23:56

- 建立 Run Package First 文件管理机制，主入口改为 `outputs/工作包/`。
- 补建历史任务工作包：PEANUT 数据清洗与风险底座、上游查验与浓度修复、BetaBinomial 信念更新、MOE/EDI 外部参数匹配、全工作目录整理与规范化。
- 生成 `run_index.md`、`run_manifest.csv`、`latest_canonical_outputs.yaml` 和任务包 manifests。
- 创建 `run-package-manager` skill 并更新相关 organizer/orchestrator skills。

## 2026-04-24 23:57

- 建立 Run Package First 文件管理机制，主入口改为 `outputs/工作包/`。
- 补建历史任务工作包：PEANUT 数据清洗与风险底座、上游查验与浓度修复、BetaBinomial 信念更新、MOE/EDI 外部参数匹配、全工作目录整理与规范化。
- 生成 `run_index.md`、`run_manifest.csv`、`latest_canonical_outputs.yaml` 和任务包 manifests。
- 创建 `run-package-manager` skill 并更新相关 organizer/orchestrator skills。

## 2026-04-25 00:20

- 执行全工作流目录重构与去重，主入口固化为 `outputs/工作包/`。
- 清理 reports/data/outputs 中的 latest/archive 辅助残留，标准目录只保留 canonical 和 pipeline 必需文件。
- 更新 AGENTS.md、run-package-manager、whole-workspace-organizer、artifact-organizer、goal-driven orchestrator 和 project-memory-updater。
- 生成 workspace_inventory_before、cleanup plan、移动/删除/待复核日志、run index 和 cleanup report。
## 2026-04-25 11:40

- 创建 `outputs/工作包/20260425_1132_DQN初步运行/`，完成 DQN 前上游核验与 DQN-style 沙盒 prototype。
- 上游核验 10 项通过，0 个阻断；prototype 输出 1710 个状态单元的动作建议、动作汇总和高优先级状态表。
- 当前环境缺少 `torch`，本轮用 `sklearn.MLPRegressor` 的 Fitted Q iteration 作为轻量 DQN-style 替代。
- 新增 DQN 核心方法文献 Mnih et al. (2015) 到 Zotero，item key `NHMM33QB`。

## 2026-04-25 12:08

- 创建 `outputs/工作包/20260425_1157_DQN文档驱动建模准备与参数确认/`，完成正式 DQN 前的文档抽取、Zotero 文献/乱码审计、联网方法背景补充、Python/torch 环境查验和参数缺口清单。
- 从研究计划 DOCX 生成 `project_state/dqn_model_spec_from_document.yaml`、`project_state/dqn_parameter_confirmation_table.csv`、`project_state/environment_notes.md` 和 `references/processed_summaries/dqn_model_spec_summary.md`。
- 发现用户指定的 `D:/anaconda3/envs/myevn1/python.exe` 路径不存在；实际 `D:/anaconda3/envs/myenv1/python.exe` 可在 OpenMP workaround 下导入 `torch 2.11.0+cu130`，CUDA 不可用，`sklearn` 缺失。
- 更新 AGENTS.md 和 DQN 前置审计相关 skills，固化 document-governed DQN、Zotero note 编码查验、环境查验和 readiness 审计规则。

## 2026-04-25 13:00

- 完成 `D:\anaconda3\envs\myenv1\python.exe` 环境修复：卸载 `torch 2.11.0+cu130` / `torchvision 0.26.0+cu130`，安装 `torch 2.11.0+cu126`、`torchvision 0.26.0+cu126`、`torchaudio 2.11.0+cu126`。
- 安装并验证 DQN、数据处理、可视化、Excel 输出和文档读取依赖：`numpy`、`pandas`、`scipy`、`scikit-learn`、`matplotlib`、`seaborn`、`plotly`、`openpyxl`、`xlsxwriter`、`pyyaml`、`tqdm`、`joblib`、`tensorboard`、`gymnasium`、`python-docx`、`pypdf`、`pyarrow`。
- `torch.cuda.is_available()` 已验证为 True，GPU 为 `NVIDIA GeForce RTX 4060 Ti`，10-step torch GPU smoke test 通过。
- 新增任务工作包 `outputs/工作包/20260425_1251_DQN环境修复_PyTorch_CUDA126安装/`，同步 `project_state/myenv1_dqn_environment_config.yaml` 和 `project_state/environment_notes.md`。

## 2026-04-26 16:28:01

- 创建工作包 outputs/工作包/20260426_1616_DQN文献增强建模方案与参数确认/。
- 复验 DQN 环境：D:\anaconda3\envs\myenv1\python.exe、	orch 2.11.0+cu126、CUDA 12.6、RTX 4060 Ti。
- 生成上游产物审计、Zotero 文献审计、联网补充文献清单、DQN 文献增强建模方案、参数确认表、readiness 报告和 YAML 草案。
- 同步 canonical 参数确认表到 project_state/dqn_parameter_confirmation_table.csv，同步方法摘要到 
eferences/processed_summaries/，并写入 Zotero 工作流 deepread/candidate/screened 文件。

## 2026-04-26 17:09:05

- 建立 workflow_improvement/ 长期自我升级机制，包括 source watchlist、capability taxonomy、gap schema、evaluation rubric、safe patch policy、approval queue、improvement ledger。
- 新增 8 个自我升级 skills，并同步到 skills/ 与 .agents/skills/。
- 新增 workflow self-improvement recipes 与 workflow_recipes/command_intents.yaml。
- 新增 src/workflow1/self_improvement/ 轻量模块和 CLI 阶段：workflow-scout、workflow-upgrade-plan、workflow-upgrade-apply --safe-only、list-upgrade-candidates、list-approval-queue、skills-doctor、dry-run --goal。
- 执行首次安全扫描和 dry-run；未运行真实数据、模型训练或 DQN。

## 2026-04-26 17:22:53

- 执行一句话自动科研 dry-run 验收，覆盖 9 条常用短命令。
- 新增 src/workflow1/one_line.py，并将 CLI --stage dry-run --goal 接入结构化 one-line plan。
- 新增 workflow_recipes/one_line_research_dry_run.yaml 和 model_registry/one_line_task_family_registry.yaml。
- 生成验收矩阵、缺口矩阵、安全补强报告和 approval queue。


## 2026-04-26 18:30:50 全流程验收与DQN自动参数训练

- 创建任务工作包 `outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`。
- 完成 one-line dry-run 验收、文献/环境/上游核验、experimental DQN 参数自动合成、myenv1 GPU 训练、baseline 对比、结果审计和 canonical 同步。
- 修复训练报告缺少 tabulate 与 reward 尺度异常问题。

## 2026-04-26 19:11:21

- 新增 research_quality policy 总体系、20 个质量核验 skills、顶级期刊 benchmark registry、多模型比较协议、结果论断保护和论文质量输出 stub。
- 更新 workflow_improvement、model_registry、AGENTS.md 和 project memory。

## 2026-04-26 19:12:22

- 新增 research_quality policy 总体系、20 个质量核验 skills、顶级期刊 benchmark registry、多模型比较协议、结果论断保护和论文质量输出 stub。
- 更新 workflow_improvement、model_registry、AGENTS.md 和 project memory。

## 2026-04-26 20:03:21

- 创建 `outputs/工作包/20260426_2000_指定清理与DQN修正版继续实验`，完成删除候选扫描；未删除文件，未继续 DQN。

## 2026-04-26 20:04:06

- 创建 `outputs/工作包/20260426_2000_指定清理与DQN修正版继续实验`，完成删除候选扫描；未删除文件，未继续 DQN。

## 2026-04-26 20:51:24 推荐缓存删除与DQN修正版训练

- 删除 recommended 缓存/临时项 21 项。
- 完成 PEANUT DQN 修正版 experimental run，新增 PNG 图表、多模型对比、Q-learning baseline、quality gates 和 results_draft.docx。
- 工作包：`outputs/工作包/20260426_2050_推荐缓存删除与DQN修正版训练`。

## 2026-04-26 20:55:03 推荐缓存删除与DQN修正版训练

- 删除 recommended 缓存/临时项 21 项。
- 完成 PEANUT DQN 修正版 experimental run，新增 PNG 图表、多模型对比、Q-learning baseline、quality gates 和 results_draft.docx。
- 工作包：`outputs/工作包/20260426_2054_推荐缓存删除与DQN修正版训练`。

## 2026-04-26 20:57:02 推荐缓存删除与DQN修正版训练

- 删除 recommended 缓存/临时项 21 项。
- 完成 PEANUT DQN 修正版 experimental run，新增 PNG 图表、多模型对比、Q-learning baseline、quality gates 和 results_draft.docx。
- 工作包：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练`。


## 2026-04-26

- 完成 DQN 输出复核、解释体系补强、代码说明、论文级 Results DOCX、文献/Zotero 侧车和长期规则升级。任务包：`outputs/工作包/20260426_2245_DQN输出复核_解释体系与论文输出升级`。


## 2026-04-26

- 完成 DQN 输出复核、解释体系补强、代码说明、论文级 Results DOCX、文献/Zotero 侧车和长期规则升级。任务包：`outputs/工作包/20260426_2245_DQN输出复核_解释体系与论文输出升级`。


## 2026-04-26

- 完成 DQN 输出复核、解释体系补强、代码说明、论文级 Results DOCX、文献/Zotero 侧车和长期规则升级。任务包：`outputs/工作包/20260426_2249_DQN输出复核_解释体系与论文输出升级`。


## 2026-04-26

- 完成 DQN 输出复核、解释体系补强、代码说明、论文级 Results DOCX、文献/Zotero 侧车和长期规则升级。任务包：`outputs/工作包/20260426_2252_DQN输出复核_解释体系与论文输出升级`。


## 2026-04-26

- 完成 DQN 输出复核、解释体系补强、代码说明、论文级 Results DOCX、文献/Zotero 侧车和长期规则升级。任务包：`outputs/工作包/20260426_2254_DQN输出复核_解释体系与论文输出升级`。


## 2026-04-26

- 修正输出解释机制：解释必须就地放在结果目录，关键 artifact 生成同名 `.explanation.md`，DQN 代码增加深度说明。任务包：`outputs/工作包/20260426_2317_输出解释就地化修正与DQN代码深度说明补强`。


## 2026-04-26

- 精简冗余解释文件，清理缓存/失败中间包，创建项目精选存档，生成含表和核心图的学术 Results Word。任务包：`outputs/工作包/20260426_2332_输出解释精简_项目存档与Word学术升级`。


## 2026-04-26

- 精简冗余解释文件，清理缓存/失败中间包，创建项目精选存档，生成含表和核心图的学术 Results Word。任务包：`outputs/工作包/20260426_2334_输出解释精简_项目存档与Word学术升级`。


## 2026-04-26

- 精简冗余解释文件，清理缓存/失败中间包，创建项目精选存档，生成含表和核心图的学术 Results Word。任务包：`outputs/工作包/20260426_2335_输出解释精简_项目存档与Word学术升级`。


## 2026-04-26

- 精简冗余解释文件，清理缓存/失败中间包，创建项目精选存档，生成含表和核心图的学术 Results Word。任务包：`outputs/工作包/20260426_2336_输出解释精简_项目存档与Word学术升级`。
