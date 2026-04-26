# DQN 输出 Deep Audit 报告

- 最新复核包：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练`
- 历史对照包：`outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`
- 审计 artifact 数：108
- 问题数：6

## 问题类型分布

- 表格近似为空: 1
- 全 0 图表语义不足: 1
- 长期解释文件缺失: 4

## 关键发现

- 最新 `2056` 修正版 DQN 包的 PNG 主图总体可读，但 `constraint_summary` 属于全 0 语义图，需要解释性修复。
- 历史 `1746` DQN 自动参数训练包中存在近似空表格和解释不足输出，不能直接进入论文 Results；本轮未在实际文件系统中确认到 0 字节主图。
- 最新包缺少面向用户的系统性图、表、模型输出、代码解释与 artifact-to-evidence map。
- DQN 设置说明仍需把 state/action/reward/transition/constraint/baseline/training/quality gate 逐项写明，并保持 experimental 边界。

## 问题清单摘要

- [high] 表格近似为空：`outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练/02_表格输出/dqn_state_feature_missing_summary.csv`；修复：补充字段、来源、行列数和无法生成原因；必要时重新生成。
- [medium] 全 0 图表语义不足：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练/03_图表输出/dqn_revised_constraint_summary.png`；修复：生成解释性 PNG：说明全 0 表示当前约束设定下没有违约，不是缺失数据。
- [medium] 长期解释文件缺失：`最新 DQN 包缺少 figure_explanations.md`；修复：在本轮任务包生成解释索引，并固化为 workflow 规则。
- [medium] 长期解释文件缺失：`最新 DQN 包缺少 table_explanations.md`；修复：在本轮任务包生成解释索引，并固化为 workflow 规则。
- [medium] 长期解释文件缺失：`最新 DQN 包缺少 model_output_explanations.md`；修复：在本轮任务包生成解释索引，并固化为 workflow 规则。
- [medium] 长期解释文件缺失：`最新 DQN 包缺少 code_explanations.md`；修复：在本轮任务包生成解释索引，并固化为 workflow 规则。

