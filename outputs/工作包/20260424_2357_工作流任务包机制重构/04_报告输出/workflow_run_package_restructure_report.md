# 工作流任务包机制重构报告

## 1. 为什么原来的 latest/archive 不够

`latest/` 方便机器和人快速找到当前最新文件，`archive/` 适合保存历史或不确定文件，但它们不能自然表达“一轮任务用了哪些输入、产生了哪些输出、报告和日志在哪里”。用户查看时需要按时间和任务内容理解整个科研过程，因此需要 Run Package 作为主入口。

## 2. 新的任务工作包机制

以后每次实质性任务开始前创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。任务产物优先进入该工作包，并按输入说明、数据、表格、图表、报告、模型、配置、日志、代码快照分类保存。标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 3. 以后每次任务会生成什么目录

```text
outputs/工作包/YYYYMMDD_HHMM_中文任务名/
├─ README.md
├─ 00_输入说明/
├─ 01_数据输出/
├─ 02_表格输出/
├─ 03_图表输出/
├─ 04_报告输出/
├─ 05_模型与实验/
├─ 06_配置参数/
├─ 07_日志与错误/
├─ 08_代码快照/
└─ manifest.csv
```

## 4. 这次如何重组已有文件

已补建 5 个历史任务工作包，并创建本次机制重构工作包：

- `outputs/工作包/20260424_1908_PEANUT数据清洗与风险底座`
- `outputs/工作包/20260424_2049_PEANUT上游查验与浓度修复`
- `outputs/工作包/20260424_2048_BetaBinomial信念更新`
- `outputs/工作包/20260424_2132_MOE_EDI外部参数匹配`
- `outputs/工作包/20260424_2244_全工作目录整理与规范化`
- `outputs/工作包/20260424_2357_工作流任务包机制重构`

## 5. 哪些文件被移动

旧的顶层 `outputs/20260424_*` 目录已复制进入对应工作包后，移动到 `archive/legacy_outputs_after_run_package_restructure/`，避免 outputs 根目录继续混杂。根目录未知唯一文件若出现，会进入 `outputs/_待复核/`。

详细记录见 `02_表格输出/reorganized_files_log.csv`。

## 6. 哪些重复文件被删除

本轮仅允许删除临时缓存、锁文件、空临时文件等安全对象。删除记录见 `outputs/_index/deleted_duplicates_log.csv` 和本工作包 `02_表格输出/deleted_duplicates_log.csv`。

## 7. 哪些唯一文件进入 `_待复核`

本轮未发现需要移动到 `_待复核` 的根目录唯一文件。若后续发现无法归属但唯一的文件，将进入 `outputs/_待复核/YYYYMMDD_未归类唯一文件/`。

## 8. canonical 文件保留在标准目录

以下 canonical 文件仍保留在标准目录，保护后续 pipeline：

- `data/03_primary/peanut_cleaned_analysis_ready.csv`
- `data/03_primary/peanut_cleaned_analysis_ready.xlsx`
- `data/04_feature/peanut_concentration_clean_table.csv`
- `data/04_feature/peanut_concentration_distribution_summary.csv`
- `data/04_feature/peanut_count_panel.csv`
- `data/04_feature/peanut_beta_binomial_belief_states.csv`
- `data/04_feature/peanut_belief_mdp_state_features.csv`
- `data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`
- `data/04_feature/peanut_bmdl_parameter_config.json`
- `data/04_feature/peanut_bmdl_parameter_table.csv`
- `data/04_feature/peanut_consumption_parameter_table.csv`
- `data/04_feature/peanut_population_parameter_table.csv`
- `data/04_feature/peanut_edi_moe_risk_table.csv`
- `data/04_feature/peanut_edi_moe_risk_summary.csv`
- `reports/latest/peanut_pre_dqn_readiness_after_moe_edi.md`
- `project_state/conversation_handoff.md`

## 9. 后续如何查看每一步结果

打开 `outputs/工作包/`，按 `YYYYMMDD_HHMM_中文任务名` 查看每一步；打开 `outputs/_index/run_index.md` 可查看任务包总索引；每个任务包内的 `README.md` 和 `manifest.csv` 说明该轮输入、输出和关键文件。

## 10. 是否适合继续 MOE/EDI、DQN prototype 和论文输出

适合继续。MOE/EDI 和 belief-MDP/DQN prototype 后续任务都应先创建新的任务工作包。当前仍不应直接运行 DQN，需先补齐动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数。
