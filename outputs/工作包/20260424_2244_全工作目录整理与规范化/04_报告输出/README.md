# 全工作目录整理与规范化

## 任务目的

整理整个 workflow1 工作目录，建立长期目录规范、latest/archive 副本、全局索引和整理后报告。本次不重新跑数据分析、清洗、MOE/EDI 或 DQN。

## 关键输出

- `reports/workspace_inventory.md`
- `tables/workspace_inventory.csv`
- `tables/raw_data_inventory.csv`
- `reports/source_code_inventory.md`
- `reports/skills_inventory.md`
- `reports/project_whole_workspace_organization_report.md`
- `manifests/output_manifest.csv`
- `manifests/latest_outputs.yaml`
- `manifests/workspace_structure.md`
- `logs/organization_actions.csv`

## 关键假设

- `data/01_raw` 原始文件不可移动、不可重命名、不可删除。
- pipeline 依赖 canonical 文件保留原路径，同时复制到 `latest/`。
- 不确定文件不删除，进入 archive/unsorted 或 notes。

## 下一步建议

继续补齐 belief-MDP / DQN prototype 所需动作空间、预算、产能、成本和约束参数；每次任务结束后执行全工作目录整理检查。
