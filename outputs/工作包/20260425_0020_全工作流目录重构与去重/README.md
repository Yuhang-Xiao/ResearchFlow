# 全工作流目录重构与去重

## 本轮任务目的

执行全工作流目录重构、归类、去重和长期规则固化；不重新跑数据、不重新清洗、不重新计算 MOE/EDI、不运行 DQN。

## 输入文件

- `AGENTS.md`
- `outputs/_index/`
- `outputs/工作包/`
- `project_state/`
- `skills/`
- 全工作目录文件清单

## 生成文件

- `02_表格输出/workspace_inventory_before.csv`
- `04_报告输出/workspace_cleanup_plan.md`
- `02_表格输出/deleted_duplicates_log.csv`
- `02_表格输出/moved_files_log.csv`
- `02_表格输出/unclassified_unique_files_log.csv`
- `04_报告输出/workflow_workspace_cleanup_report.md`
- `07_日志与错误/workflow_validation_log.json`

## 关键结果

- 主查看入口固化为 `outputs/工作包/`。
- 标准目录只保留 canonical 和 pipeline 必需文件。
- `data/01_raw` 原始数据未修改、未删除、未移动。
- import 与 launch 验证已执行。

## 错误和修复

轻量整理中遇到的缓存和辅助副本按规则删除或迁移，详见日志。

## 是否影响后续流程

不影响。canonical 文件保留在标准目录，任务结果进入工作包。

## 下一步建议

继续 MOE/EDI 或 DQN prototype 前，先创建新的任务工作包，并补齐动作空间、预算、产能、成本和约束参数。
