# Decision Log

## 2026-04-24

### Adopt auto-repair before stopping for lightweight workflow issues

Rationale: The PEANUT workflow showed that missing lightweight optional dependencies, Chinese path handling problems, table rendering failures, and chart output failures can often be repaired safely without user intervention when they do not threaten raw data or scientific conclusions.

Impact: 后续任务中，Codex 应自主修复轻量依赖缺失、路径错误、中文文件名问题、普通图表/表格输出问题和非关键代码错误；只有在 API/权限/手动配置、原始数据无法读取、关键字段缺失、核心外部参数缺失、可能破坏原始数据或会影响科研结论的问题上才停止询问用户。每次自动修复或降级执行都应记录到 `reports/*_error_log.md` 或任务报告；若影响后续流程，还应更新 `lessons_learned.md` 和 `decision_log.md`。

## 2026-04-24

### Adopt one-line launch as the primary operating mode

Rationale: The user wants future tasks to start from concise commands instead of long prompts, while preserving project rules, memory, references, and accumulated workflow decisions.

Impact: Codex should treat commands such as “启动自动科研流程”, “启动花生风险监管流程”, and “继续上次任务” as triggers to read `START_HERE.md`, project memory, run protocol, conversation handoff, references, raw inventory, and relevant skills before planning or execution.

### Add repo-scoped skills while preserving legacy skills

Rationale: Current Codex-style repo-scoped skills are expected under `.agents/skills/`, but the repository already contained useful skills under `skills/`.

Impact: New orchestration, skill scouting, and memory update skills are stored under `.agents/skills/` and mirrored under `skills/`. `AGENTS.md` instructs Codex to read both locations for compatibility.

### Use external skill/workflow projects as design references only

Rationale: Web search found useful projects for Codex skills, Zotero MCP, AutoML, research automation, and RL workflows, but directly copying external code would be unnecessary and risky.

Impact: `reports/skill_scout_report.md` records candidate projects and design ideas. Future skill upgrades should borrow structure and checklists, not uncontrolled code.

## 2026-04-24

### Implement only non-destructive preparation runners in the second repair pass

Rationale: The repository needs a minimal runnable path before full automated research execution, but the user explicitly requested no real cleaning, modeling, tuning, visualization, or raw data modification in this step.

Impact: `intake`, `validation`, and `cleaning-plan` are now runnable. They write reports under `reports/` and `reports/tables/`. `cleaning-plan` produces recommendations only and must not be treated as execution of cleaning rules.

## 2026-04-24

### Add a reference-document layer before future full workflow runs

Rationale: The migrated workflow needs a reusable place for Word/PDF outlines, methodological notes, model plans, data-cleaning plans, standards, literature, and informal notes that can guide later data cleaning, modeling, simulation, optimization, visualization, and reporting.

Impact: Future major workflow tasks should inspect relevant files under `references/` when they exist, extract actionable guidance in Chinese, preserve technical terms where appropriate, and record durable extracted guidance under `references/processed_summaries/`. User explicit instruction and actual dataset evidence override generic reference suggestions.

### Add minimal Python packaging and a lightweight workflow entrypoint

Rationale: The readiness audit found that `src/workflow1` was not importable from the repository root without installation or `PYTHONPATH`, and that the repository lacked a clear runnable entrypoint.

Impact: The repository now has `pyproject.toml`, `requirements.txt`, and a lightweight `workflow1` / `python -m workflow1` runner for config loading, logging, stage routing placeholders, and graceful not-implemented handling. Heavy cleaning, modeling, tuning, and visualization logic remains intentionally unimplemented until a real task requires it.

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

## 2026-04-24

### 限定本轮数据源并构建花生/AFB1 数据基础

Rationale: 用户明确要求本轮只使用 `PEANUT2023-20241.xlsx` 和指定研究计划，不使用 `PEANUTwithProb0627.xlsx`。

Impact: 所有派生数据与报告均基于指定原始数据；原始数据未修改。后续建模应从本轮计数面板和浓度清洗表继续。

### AFB1 浓度最终值采用复检优先规则

Rationale: 用户要求对“初检结果/复检结果”分别提取，并构建最终采用浓度值。

Impact: 当复检浓度可解析时使用复检值，否则使用初检或单一检测值；无法解析记录进入 issue log。

## 2026-04-24

### Use Beta(1,1) prior and 0.95 forgetting factor for the first PEANUT belief-update prototype

Rationale: 当前用户要求实现 Beta-Binomial 信念更新原型，但尚未提供外部先验强度或遗忘因子。Beta(1,1) 是弱信息先验，0.95 遗忘因子可保留历史信息同时允许月度风险变化。

Impact: 输出状态特征表可直接作为 belief-MDP 原型输入；后续如获得专家先验或校准参数，可重跑并替换 `prior_alpha`、`prior_beta` 和 `forgetting_factor`。

## 2026-04-24

### Use Beta(1,1) prior and 0.95 forgetting factor for the first PEANUT belief-update prototype

Rationale: 当前用户要求实现 Beta-Binomial 信念更新原型，但尚未提供外部先验强度或遗忘因子。Beta(1,1) 是弱信息先验，0.95 遗忘因子可保留历史信息同时允许月度风险变化。

Impact: 输出状态特征表可直接作为 belief-MDP 原型输入；后续如获得专家先验或校准参数，可重跑并替换 `prior_alpha`、`prior_beta` 和 `forgetting_factor`。

## 2026-04-24

### Require upstream verification before downstream models

Rationale: 下游 DQN/POMDP/MOE-EDI 依赖浓度、标签、计数面板和 belief state；若上游存在解析或口径错误，会直接污染模型状态和结论。

Impact: 任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。本次已修复计数面板 `浓度可用记录数` 口径，并同步重建 belief state 与 belief-MDP state features。

## 2026-04-24

### Use Beta(1,1) prior and 0.95 forgetting factor for the first PEANUT belief-update prototype

Rationale: 当前用户要求实现 Beta-Binomial 信念更新原型，但尚未提供外部先验强度或遗忘因子。Beta(1,1) 是弱信息先验，0.95 遗忘因子可保留历史信息同时允许月度风险变化。

Impact: 输出状态特征表可直接作为 belief-MDP 原型输入；后续如获得专家先验或校准参数，可重跑并替换 `prior_alpha`、`prior_beta` 和 `forgetting_factor`。

## 2026-04-24

### Require upstream verification before downstream models

Rationale: 下游 DQN/POMDP/MOE-EDI 依赖浓度、标签、计数面板和 belief state；若上游存在解析或口径错误，会直接污染模型状态和结论。

Impact: 任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。本次已修复计数面板 `浓度可用记录数` 口径，并同步重建 belief state 与 belief-MDP state features。

## 20260424

### Adopt task-specific output directories for substantive research tasks

Rationale: 用户要求每轮实质性科研任务都有独立、可追踪、中文命名的输出目录，便于查找关键结果、报告、图表、日志和 README。

Impact: 后续任务必须创建 `outputs/YYYYMMDD_中文任务名/`，标准目录继续保留，但关键产物需同步复制到任务目录。

### Use MOE/EDI prototype parameters before DQN

Rationale: 当前 DQN 仍缺动作、预算、成本和约束参数，但已有消费量、人口、体重和 BMDL 情景值可以先构建风险度量基础。

Impact: `peanut_belief_mdp_state_features_with_moe_edi.csv` 可作为后续最小 belief-MDP 环境设计输入；正式 DQN 仍需等待外部约束参数补齐。

## 20260424

### Adopt task-specific output directories for substantive research tasks

Rationale: 用户要求每轮实质性科研任务都有独立、可追踪、中文命名的输出目录，便于查找关键结果、报告、图表、日志和 README。

Impact: 后续任务必须创建 `outputs/YYYYMMDD_中文任务名/`，标准目录继续保留，但关键产物需同步复制到任务目录。

### Use MOE/EDI prototype parameters before DQN

Rationale: 当前 DQN 仍缺动作、预算、成本和约束参数，但已有消费量、人口、体重和 BMDL 情景值可以先构建风险度量基础。

Impact: `peanut_belief_mdp_state_features_with_moe_edi.csv` 可作为后续最小 belief-MDP 环境设计输入；正式 DQN 仍需等待外部约束参数补齐。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 20260424

### Adopt whole-workspace organization after substantive tasks

Rationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。

Impact: 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 2026-04-24 23:56

### Adopt Run Package First as primary file management rule

Rationale: 单靠 latest/archive 不能让用户一眼看出每一步任务做了什么、产物在哪里、哪些输入输出属于同一轮任务。

Impact: 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。

## 2026-04-24 23:57

### Adopt Run Package First as primary file management rule

Rationale: 单靠 latest/archive 不能让用户一眼看出每一步任务做了什么、产物在哪里、哪些输入输出属于同一轮任务。

Impact: 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。

## 2026-04-25 00:20

### Use Run Package as the only primary output mechanism

Rationale: latest/archive 只能辅助查找最新或历史文件，不能表达每轮任务的输入、输出、日志和报告关系。

Impact: 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。
## 2026-04-25 11:40

### Run DQN only as sandbox prototype until decision parameters are supplied

Rationale: 当前上游 belief-MDP+MOE/EDI 特征已足够测试技术管线，但正式 DQN 需要真实动作空间、预算、单位成本、产能、处置/召回损失、信息价值权重和约束惩罚参数；历史数据也缺少真实干预动作与动作后状态转移。

Impact: 本轮 DQN 输出仅作为 prototype 和参数缺口定位，不作为正式监管策略或科学结论。后续正式建模应优先采用 constrained/safe RL 或 CMDP 表述，并在训练前补齐 action mask、reward 和约束参数表。

### Add Mnih et al. 2015 as core DQN method reference

Rationale: DQN 建模需要原始方法文献支撑，项目本地 Zotero 已有 safe RL 和风险监测文献，但缺少 DQN 核心源头文献。

Impact: 已通过 Zotero Web API 创建条目和 note，item key `NHMM33QB`；后续 DQN 方法章节可引用该文献作为 Q-learning + neural function approximation 的方法基础。

## 2026-04-25 12:08

### Block formal DQN until document-governed parameters and interpreter are confirmed

Rationale: 用户要求正式 DQN 必须严格按照研究计划和 Zotero note/PDF，不得沿用 `20260425_1132_DQN初步运行` sandbox prototype，也不得由 Codex 自行定稿 state、action、reward、约束和训练超参数。本轮完整读取研究计划后确认若干方向已明确，但动作空间、预算、成本、产能、损失权重和训练超参数仍未给出正式值。

Impact: 当前只允许 readiness、参数确认表和模型规范抽取产物；正式 DQN 训练仍被阻断。后续必须先由用户确认 `project_state/dqn_parameter_confirmation_table.csv` 和正式 Python 解释器。

### Treat garbled Zotero notes as unusable for formal modeling evidence

Rationale: Zotero deepread `20260425_Human-level control through deep reinforcement learning.md` 含大量 `?????`，疑似导出或 PowerShell/Markdown 编码污染。直接使用乱码 note 会破坏方法依据追溯。

Impact: 该 note 不作为正式 DQN 依据；DQN 原始方法仅作为外部正式页面背景引用，不能覆盖研究计划文档。

## 2026-04-25 13:00

### Standardize formal DQN environment on myenv1 + PyTorch cu126

Rationale: 用户明确指出 `myevn1` 是错误路径，正式 DQN 环境应使用 `D:\anaconda3\envs\myenv1\python.exe`。原 PyTorch 为 `cu130`，与当前 CUDA 12.6 运行时能力不匹配，导致 CUDA 不可用。

Impact: 正式 DQN 环境统一为 `D:\anaconda3\envs\myenv1\python.exe` + `torch 2.11.0+cu126`。不得使用默认 Python、base 环境、错误路径 `myevn1` 或 PyTorch `cu130` 作为正式 DQN 环境。正式训练前仍需参数确认表获用户批准。

## 2026-04-26 16:28:01

### Keep formal PEANUT DQN blocked after literature-enhanced model planning

Rationale: 本轮已完成用户研究计划、Zotero/PDF、联网高质量文献、当前 PEANUT 数据结构、MOE/EDI 风险特征和 belief-MDP 状态表的综合审计。环境 D:\anaconda3\envs\myenv1\python.exe + 	orch 2.11.0+cu126 可用；但动作空间、预算、单位成本、产能、最低覆盖、处置/召回损失、信息价值、reward 权重、transition/仿真假设和 DQN 训练超参数仍未由用户确认。

Impact: project_state/dqn_parameter_confirmation_table.csv 成为下一步正式 DQN 的参数确认入口。确认前只能继续 readiness、方案修订、文献补充或参数敏感性设计，不得运行 formal DQN。

## 2026-04-26 17:09:05

### Adopt Workflow Self-Improvement System

Rationale: 用户要求 workflow1 长期具备自我寻找、评估并安全吸收外部 skills/agents/workflows 的能力，而不是只做一次性 skill 列表。

Impact: 以后当用户说“优化工作流”“升级工作流”“让 Codex 自己寻找 skill”“搜索 GitHub 改进 workflow”时，Codex 必须触发 workflow-self-improvement-scout。低风险本地升级可自动执行；MCP/API/Zotero 写入/依赖安装/第三方脚本等进入 approval queue 等待确认。

## 2026-04-26 17:22:53

### Strengthen one-line dry-run routing before real autonomous research

Rationale: 补强前 dry-run --goal 只能粗略区分 workflow self-improvement 与 generic preview，无法审计清洗、标签、文献、Zotero、模型选择、报告、正式 DQN 阻断等关键路径。

Impact: 新增 workflow1.one_line.route_goal 作为一句话科研 dry-run 路由器；真实数据处理、清洗、训练和 DQN 仍需遵守用户授权和 formal 参数确认规则。


## 2026-04-26 18:30:50

### Allow self-synthesized experimental DQN without converting it to formal DQN

Rationale: 用户本轮明确授权自动合成参数并运行 DQN 实验版，用于 workflow 闭环和 prototype 分析。

Impact: 本轮结果标记为 `自动合成参数 DQN 实验版 / self-synthesized DQN experimental run`；formal DQN 仍需用户逐项确认参数。reward 中人口加权风险 proxy 采用 P95 归一化以避免 Q/loss 数量级异常。

## 2026-04-26 19:11:21 Research Quality System Upgrade

Decision: 将科研质量核验设为后续所有科研任务的默认硬闸门。

Rationale: 最近 DQN experimental run 已证明流程能跑通，但 formal 科研输出还需要多模型比较、baseline fairness、数据/图表/表格/引用核验和顶刊对标。

Impact: 高风险外部工具进入 approval queue；低风险能力转化为本地 policy、skill、recipe、registry 和 stub。

## 2026-04-26 19:12:22 Research Quality System Upgrade

Decision: 将科研质量核验设为后续所有科研任务的默认硬闸门。

Rationale: 最近 DQN experimental run 已证明流程能跑通，但 formal 科研输出还需要多模型比较、baseline fairness、数据/图表/表格/引用核验和顶刊对标。

Impact: 高风险外部工具进入 approval queue；低风险能力转化为本地 policy、skill、recipe、registry 和 stub。

## 2026-04-26 20:03:21 删除候选扫描先行

Decision: 遵循用户最新指令，本轮只扫描候选，不执行删除，也不继续 DQN。

Rationale: 删除目标尚未由用户明确指定；DQN 修正版实验必须等待清理和索引更新完成。

## 2026-04-26 20:04:06 删除候选扫描先行

Decision: 遵循用户最新指令，本轮只扫描候选，不执行删除，也不继续 DQN。

Rationale: 删除目标尚未由用户明确指定；DQN 修正版实验必须等待清理和索引更新完成。

## 2026-04-26 20:51:24 DQN 修正版仍保持 experimental

Decision: 本轮允许继续 DQN 修正版训练，但所有输出标记为 experimental，不转为 formal policy conclusion。

Rationale: 用户已授权 experimental run，但 formal DQN 所需预算、成本、capacity、reward、transition 与训练超参数仍未逐项确认。

Impact: 结果可用于方法闭环、参数敏感性设计和论文式 experimental draft；formal DQN 仍需用户确认参数后重跑。

## 2026-04-26 20:55:03 DQN 修正版仍保持 experimental

Decision: 本轮允许继续 DQN 修正版训练，但所有输出标记为 experimental，不转为 formal policy conclusion。

Rationale: 用户已授权 experimental run，但 formal DQN 所需预算、成本、capacity、reward、transition 与训练超参数仍未逐项确认。

Impact: 结果可用于方法闭环、参数敏感性设计和论文式 experimental draft；formal DQN 仍需用户确认参数后重跑。

## 2026-04-26 20:57:02 DQN 修正版仍保持 experimental

Decision: 本轮允许继续 DQN 修正版训练，但所有输出标记为 experimental，不转为 formal policy conclusion。

Rationale: 用户已授权 experimental run，但 formal DQN 所需预算、成本、capacity、reward、transition 与训练超参数仍未逐项确认。

Impact: 结果可用于方法闭环、参数敏感性设计和论文式 experimental draft；formal DQN 仍需用户确认参数后重跑。


## 2026-04-26 Decision

决定将 output explanation、empty chart prevention、model setting documentation、code explanation、literature-grounded modeling 和 Zotero safe sidecar 写入长期 workflow。DQN 结果保持 experimental，不升级为 formal policy conclusion。


## 2026-04-26 Decision

决定将 output explanation、empty chart prevention、model setting documentation、code explanation、literature-grounded modeling 和 Zotero safe sidecar 写入长期 workflow。DQN 结果保持 experimental，不升级为 formal policy conclusion。


## 2026-04-26 Decision

决定将 output explanation、empty chart prevention、model setting documentation、code explanation、literature-grounded modeling 和 Zotero safe sidecar 写入长期 workflow。DQN 结果保持 experimental，不升级为 formal policy conclusion。


## 2026-04-26 Decision

决定将 output explanation、empty chart prevention、model setting documentation、code explanation、literature-grounded modeling 和 Zotero safe sidecar 写入长期 workflow。DQN 结果保持 experimental，不升级为 formal policy conclusion。


## 2026-04-26 Decision

决定将 output explanation、empty chart prevention、model setting documentation、code explanation、literature-grounded modeling 和 Zotero safe sidecar 写入长期 workflow。DQN 结果保持 experimental，不升级为 formal policy conclusion。


## Decision: Explanation Co-location

总索引不能替代本地解释。未来每个结果目录必须有 README/local explanation，关键 artifact 必须尽量生成同名 `.explanation.md`。DQN 代码必须映射到 Method 和 Results。


## Decision: Explanation Minimalism

不再为每个辅助文件机械生成同名 explanation。保留目录 README、核心 DQN 说明、代码映射、关键报告和 Word 说明即可，避免阅读混淆。


## Decision: Explanation Minimalism

不再为每个辅助文件机械生成同名 explanation。保留目录 README、核心 DQN 说明、代码映射、关键报告和 Word 说明即可，避免阅读混淆。


## Decision: Explanation Minimalism

不再为每个辅助文件机械生成同名 explanation。保留目录 README、核心 DQN 说明、代码映射、关键报告和 Word 说明即可，避免阅读混淆。


## Decision: Explanation Minimalism

不再为每个辅助文件机械生成同名 explanation。保留目录 README、核心 DQN 说明、代码映射、关键报告和 Word 说明即可，避免阅读混淆。
