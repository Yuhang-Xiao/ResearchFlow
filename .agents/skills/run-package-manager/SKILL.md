---
name: run-package-manager
description: Create task run packages under outputs/工作包, route all task artifacts into the package, update manifests, and protect canonical workflow files.
---

# Run Package Manager

## 何时触发

每次实质性科研任务、清洗、建模、可视化、报告、目录整理或优化实验开始前必须触发。

## 创建任务工作包

1. 使用任务开始时间创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
2. 创建 `README.md`、`manifest.csv`，以及 `00_输入说明/` 到 `08_代码快照/`。
3. 在 `00_输入说明/inputs.md` 记录输入路径和摘要；不复制大型原始数据。

## 文件分类

- 数据输出进入 `01_数据输出/`。
- 汇总表进入 `02_表格输出/`。
- 图表进入 `03_图表输出/`。
- 报告进入 `04_报告输出/`。
- 模型和实验进入 `05_模型与实验/`。
- 参数配置进入 `06_配置参数/`。
- 日志、错误和修复记录进入 `07_日志与错误/`。
- 本轮新增或修改的关键脚本副本进入 `08_代码快照/`。

## canonical 文件

如果某个结果需要被后续 pipeline 读取，保留任务包副本，同时复制到标准目录作为 canonical 文件。标准目录只保存 canonical 和 pipeline 必需文件。

## 去重和待复核

hash 完全重复的辅助副本、缓存、临时文件和空文件可以删除，但必须写入 `outputs/_index/deleted_duplicates_log.csv`。唯一但无法归类的文件进入 `outputs/_待复核/`，不得删除。

## 任务结束

更新任务包 `manifest.csv`、`outputs/_index/run_manifest.csv`、`outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml`，然后调用 `whole-workspace-organizer` 做全工作目录整理检查。

长期规则：以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。

## Document-Governed DQN Addendum

For any DQN, POMDP, belief-MDP, constrained RL, or safe RL task, the run package must be created before model preparation and must contain outputs from these prerequisite auditors:

1. `document-governed-modeling`
2. `zotero-literature-auditor`
3. `environment-auditor`
4. `dqn-readiness-auditor`

Formal DQN outputs must not be written unless the user has confirmed the parameter confirmation table. Readiness reports, parameter tables, environment audits, literature audits, and model-spec extraction files belong in the task package first, with only confirmed canonical files synchronized to `project_state/` or `references/processed_summaries/`.
