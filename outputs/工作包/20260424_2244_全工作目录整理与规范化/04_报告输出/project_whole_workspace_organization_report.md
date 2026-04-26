# 全工作目录整理与规范化报告

## 1. 整理前目录问题

- 根目录存在散落 `.docx` 文档。
- `reports/` 根目录堆积多个历史 Markdown/JSON 报告。
- `data/04_feature/` 同时存在 canonical CSV 与重复 XLSX 导出。
- `outputs/` 缺少统一 `_index` manifest、latest outputs 和 workspace structure。
- skills 在 `.agents/skills/` 与 `skills/` 间存在兼容副本，需要索引说明。

## 2. 整理范围

本次覆盖 root、`.agents/`、`.codex/`、`skills/`、`src/`、`data/`、`reports/`、`experiments/`、`outputs/`、`references/`、`project_state/`、`prompts/`。未重新跑数据分析、清洗、MOE/EDI 或 DQN。

## 3. 创建或补齐的目录

- 标准 data/reports/outputs/references/experiments latest 与 archive 目录。
- 本轮任务目录 `outputs/20260424_全工作目录整理与规范化/` 及其 data、reports、tables、figures、logs、configs、manifests、archive 子目录。
- `outputs/_index/` 全局索引目录。

## 4. 移动或复制了哪些文件

- 本次幂等整理运行中移动文件数：3
- 复制文件数：50
- 操作日志见 `outputs/20260424_全工作目录整理与规范化/logs/organization_actions.csv`。
- 当前 archive manifest 记录文件数：35，见 `outputs/20260424_全工作目录整理与规范化/tables/archive_manifest.csv`。

## 5. canonical latest 文件

canonical 数据文件保留在原 pipeline 路径，并复制到 `latest/`：

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

报告 latest 副本位于 `reports/latest/`。

## 6. archive 文件

- `data/04_feature/archive/`：重复 XLSX feature 导出。
- `reports/archive/20260424_整理前历史报告/`：历史 root 报告。
- `references/notes/`：根目录散落文档。
- 不确定 root 文件会进入 `outputs/archive/unsorted_root_files/`。

当前 archive 文件清单节选：

- `reports/archive/20260424_整理前历史报告/category_reconstruction_summary_FINAL_SiChuan_2023_ALL_DATA.md`
- `reports/archive/20260424_整理前历史报告/peanut_beta_binomial_error_log.md`
- `reports/archive/20260424_整理前历史报告/peanut_beta_binomial_run_summary.json`
- `reports/archive/20260424_整理前历史报告/peanut_count_panel_report.md`
- `reports/archive/20260424_整理前历史报告/peanut_eda_report.md`
- `reports/archive/20260424_整理前历史报告/peanut_modeling_optimization_feasibility.md`
- `reports/archive/20260424_整理前历史报告/peanut_pre_dqn_readiness_after_repair.md`
- `reports/archive/20260424_整理前历史报告/peanut_upstream_audit_summary.json`
- `reports/archive/20260424_整理前历史报告/peanut_visualization_report.md`
- `reports/archive/20260424_整理前历史报告/peanut_workflow_error.md`
- `reports/archive/20260424_整理前历史报告/readiness_audit_2026-04-24.md`
- `reports/archive/20260424_整理前历史报告/README.md`
- `reports/archive/20260424_整理前历史报告/README_20260424_1777041323.md`
- `reports/archive/20260424_整理前历史报告/schema_inventory_PEANUT2023-20241.md`
- `reports/archive/20260424_整理前历史报告/skill_scout_report.md`
- `reports/archive/cleanup_2026-04-14/raw_data_schema_inventory.md`
- `reports/archive/cleanup_2026-04-14/raw_data_schema_inventory_FINAL_SiChuan_2023_ALL_DATA.en.md`
- `reports/archive/cleanup_2026-04-14/raw_data_schema_inventory_FINAL_SiChuan_2023_ALL_DATA.md`
- `reports/archive/cleanup_2026-04-14/raw_data_validation_proposal_FINAL_SiChuan_2023_ALL_DATA.en.md`
- `reports/archive/cleanup_2026-04-14/raw_data_validation_proposal_FINAL_SiChuan_2023_ALL_DATA.md`
- `reports/archive/cleanup_2026-04-14/raw_data_validation_report_FINAL_SiChuan_2023_ALL_DATA.md`
- `reports/archive/cleanup_2026-04-14/tables/raw_data_validation_summary_FINAL_SiChuan_2023_ALL_DATA.csv`
- `data/04_feature/archive/peanut_belief_mdp_state_features.xlsx`
- `data/04_feature/archive/peanut_count_panel.xlsx`
- `outputs/archive/README.md`
- `outputs/archive/cache_20260424/src/workflow1/__pycache__/cli.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/__pycache__/launch.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/__pycache__/orchestration.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/__pycache__/__init__.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/__pycache__/__main__.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/utils/__pycache__/io.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/utils/__pycache__/logging.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/utils/__pycache__/__init__.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/pipelines/__pycache__/runner.cpython-313.pyc`
- `outputs/archive/cache_20260424/src/workflow1/pipelines/__pycache__/__init__.cpython-313.pyc`

## 7. outputs 归档与索引

已生成：

- `outputs/_index/output_index.md`
- `outputs/_index/output_manifest.csv`
- `outputs/_index/latest_outputs.yaml`
- `outputs/_index/workspace_structure.md`

## 8. 仍然不确定的文件

本轮未删除任何文件。不确定归属的文件按 archive/unsorted 原则处理；当前主要需人工关注的是 `references/notes/` 中从根目录移入的 Word 总结文档是否应进一步归入 project_plan 或 literature。

## 9. 是否影响后续 pipeline

未移动 `data/01_raw` 原始数据。pipeline 依赖的 canonical 数据文件保留在原路径。轻量检查结果：

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
    "stdout": "{'config_path': '.codex\\\\config.toml', 'config_loaded': True, 'stage': 'launch', 'status': 'ok', 'details': {'message': 'One-line launch context prepared. No heavy data processing was started.', 'memory_files': ('project_state/project_memory.md', 'project_state/run_protocol.md', 'project_state/current_focus.md', 'project_state/next_step.md', 'project_state/decision_log.md', 'project_state/lessons_learned.md', 'project_state/conversation_handoff.md'), 'raw_files': ('data\\\\01_raw\\\\Concentration_and_Consumption pEANUT.xlsx', 'data\\\\01_raw\\\\FINAL_SiChuan_2023_ALL_DATA.xlsx', 'data\\\\01_raw\\\\PEANUT2023-20241.xlsx', 'data\\\\01_raw\\\\PEANUTwithProb0627.xlsx', 'data\\\\01_raw\\\\population_long_clean.xlsx', 'data\\\\01_raw\\\\raw_data_inventory.csv'), 'reference_files': ('references\\\\README.md', 'references\\\\data_cleaning\\\\README.md', 'references\\\\literature\\\\README.md', 'references\\\\modeling\\\\README.md', 'references\\\\notes\\\\README.md', 'references\\\\notes\\\\物流与供应链管理前言-研究计划-肖宇航.docx', 'references\\\\notes\\\\食品安全风险监测与优化_Codex科研工作流总结.docx', 'references\\\\processed_summaries\\\\README.md', 'references\\\\processed_summaries\\\\peanut_research_plan_summary.md', 'references\\\\reference_inventory.csv', 'references\\\\standards\\\\README.md', 'references\\\\visualization\\\\README.md'), 'next_step': '# Next Step\\n\\n不要运行 DQN。下一步先补齐或确认最小 belief-MDP / DQN prototype 所需动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数；每次任务结束后执行全工作目录整理检查。', 'notes': ('This launcher only prepares context and recommendations.', 'Use intake/validation/cleaning-plan before actual cleaning.')}}",
    "stderr": "INFO:workflow1:Loaded config: True\nINFO:workflow1:Routing stage: launch"
  }
]
```

## 10. 是否适合继续 MOE/EDI、DQN prototype 和论文输出

适合继续 MOE/EDI 后续整理、belief-MDP 环境设计和 DQN prototype 参数补齐。正式 DQN 仍需动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

## 11. 后续保持整洁的方法

后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
