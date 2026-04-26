# 全工作流目录重构与去重报告

## 1. 整理前存在的问题

- `latest/archive` 仍承担了过多主入口职责，用户无法一眼按任务查看结果。
- `reports/` 仍有任务级报告和辅助目录残留。
- `data/03_primary/latest`、`data/04_feature/latest` 属于辅助副本，与 canonical 重复。
- `outputs/archive` 与顶层旧输出目录形成平行体系。
- 根目录存在 `scripts/`，不在目标一级结构内。

## 2. 最终目录结构

主入口为 `outputs/工作包/`。标准目录职责为：`data/01_raw` 保存原始数据，`data/03_primary` 保存 canonical 清洗主表，`data/04_feature` 保存 pipeline 必需特征，`reports/项目级索引与摘要` 保存少量项目级摘要，`archive/` 保存旧体系和迁移残留。

## 3. 创建了哪些任务工作包

- `outputs/工作包/20260424_1908_PEANUT数据清洗与风险底座`
- `outputs/工作包/20260424_2048_BetaBinomial信念更新`
- `outputs/工作包/20260424_2049_PEANUT上游查验与浓度修复`
- `outputs/工作包/20260424_2132_MOE_EDI外部参数匹配`
- `outputs/工作包/20260424_2244_全工作目录整理与规范化`
- `outputs/工作包/20260424_2357_工作流任务包机制重构`
- `outputs/工作包/20260425_0020_全工作流目录重构与去重`

## 4. 哪些文件被移动

移动/复制记录见 `02_表格输出/moved_files_log.csv`。本轮记录数：20。

## 5. 哪些重复文件被删除

删除记录见 `02_表格输出/deleted_duplicates_log.csv` 和 `outputs/_index/deleted_duplicates_log.csv`。本轮删除记录数：45。删除范围限于 hash 相同辅助副本、缓存、临时或空文件。

## 6. 哪些唯一文件进入 `outputs/_待复核/`

待复核记录见 `02_表格输出/unclassified_unique_files_log.csv`。本轮待复核文件数：0。

## 7. canonical 文件仍保留在标准目录

- `data/03_primary/peanut_cleaned_analysis_ready.csv`
- `data/03_primary/peanut_cleaned_analysis_ready.xlsx`
- `data/04_feature/peanut_count_panel.csv`
- `data/04_feature/peanut_concentration_clean_table.csv`
- `data/04_feature/peanut_concentration_distribution_summary.csv`
- `data/04_feature/peanut_beta_binomial_belief_states.csv`
- `data/04_feature/peanut_belief_mdp_state_features.csv`
- `data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`
- `data/04_feature/peanut_bmdl_parameter_config.json`
- `data/04_feature/peanut_bmdl_parameter_table.csv`
- `data/04_feature/peanut_consumption_parameter_table.csv`
- `data/04_feature/peanut_population_parameter_table.csv`
- `data/04_feature/peanut_edi_moe_risk_table.csv`
- `data/04_feature/peanut_edi_moe_risk_summary.csv`
- `reports/项目级索引与摘要/peanut_pre_dqn_readiness_after_moe_edi.md`
- `project_state/conversation_handoff.md`

## 8. 是否影响后续 pipeline

未移动、未删除 `data/01_raw` 原始数据。pipeline 必需 canonical 文件仍保留在标准目录。旧辅助副本删除或迁移不影响后续运行。

## 9. import 和 launch 是否通过

```json
[
  {
    "command": "D:\\anaconda3\\python.exe -c import workflow1; print(workflow1.__version__)",
    "returncode": 0,
    "stdout": "0.1.0",
    "stderr": ""
  },
  {
    "command": "D:\\anaconda3\\python.exe -m workflow1 --stage launch",
    "returncode": 0,
    "stdout": "{'config_path': '.codex\\\\config.toml', 'config_loaded': True, 'stage': 'launch', 'status': 'ok', 'details': {'message': 'One-line launch context prepared. No heavy data processing was started.', 'memory_files': ('project_state/project_memory.md', 'project_state/run_protocol.md', 'project_state/current_focus.md', 'project_state/next_step.md', 'project_state/decision_log.md', 'project_state/lessons_learned.md', 'project_state/conversation_handoff.md'), 'raw_files': ('data\\\\01_raw\\\\Concentration_and_Consumption pEANUT.xlsx', 'data\\\\01_raw\\\\FINAL_SiChuan_2023_ALL_DATA.xlsx', 'data\\\\01_raw\\\\PEANUT2023-20241.xlsx', 'data\\\\01_raw\\\\PEANUTwithProb0627.xlsx', 'data\\\\01_raw\\\\population_long_clean.xlsx', 'data\\\\01_raw\\\\raw_data_inventory.csv'), 'reference_files': ('references\\\\README.md', 'references\\\\data_cleaning\\\\README.md', 'references\\\\literature\\\\README.md', 'references\\\\modeling\\\\README.md', 'references\\\\notes\\\\README.md', 'references\\\\notes\\\\物流与供应链管理前言-研究计划-肖宇航.docx', 'references\\\\notes\\\\食品安全风险监测与优化_Codex科研工作流总结.docx', 'references\\\\processed_summaries\\\\README.md', 'references\\\\processed_summaries\\\\peanut_research_plan_summary.md', 'references\\\\reference_inventory.csv', 'references\\\\standards\\\\README.md', 'references\\\\visualization\\\\README.md'), 'next_step': '# Next Step\\n\\n不要运行 DQN。下一步如继续 MOE/EDI 或 DQN prototype 参数准备，必须先创建新的任务工作包，然后补齐动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数。', 'notes': ('This launcher only prepares context and recommendations.', 'Use intake/validation/cleaning-plan before actual cleaning.')}}",
    "stderr": "INFO:workflow1:Loaded config: True\nINFO:workflow1:Routing stage: launch"
  }
]
```

## 10. 后续如何通过 `outputs/工作包/` 查看每一步结果

打开 `outputs/工作包/`，按 `YYYYMMDD_HHMM_中文任务名` 查看每一步任务；每个任务包内有 `README.md` 和 `manifest.csv`。全局索引见 `outputs/_index/run_index.md`。


## 最终核验补充

- 最终核验后，`data/03_primary/FINAL_SiChuan_2023_ALL_DATA__category_cleaned.csv` 不属于当前 PEANUT canonical 主表，且是唯一数据文件，已移入 `outputs/_待复核/20260425_未归类唯一文件/` 并记入 `unclassified_unique_files_log.csv`。
- 标准目录 `data/03_primary/` 现仅保留 PEANUT canonical 清洗主表和 README。
- 最终待复核文件数：1。
