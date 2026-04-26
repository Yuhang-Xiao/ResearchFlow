# 一句话自动科研验收报告

## 验收结论

补强后，9 条一句话命令均通过 dry-run，全部返回结构化 route/mode/执行边界。未跑真实数据、未重新清洗、未训练模型、未运行 DQN。

## 已覆盖能力

- raw data 识别：generic/PEANUT 路由中列为计划阶段，仅 metadata/schema 级别。
- 数据清洗与标签构建：cleaning_and_label_engineering 只生成计划，本轮阻断真实清洗。
- 文献读取与 Zotero 查验：literature_method_update 路由到 reference/Zotero audit，Zotero 写入需确认。
- 模型选择：model_selection_prototype_plan 与 supervised_model_comparison 生成 prototype/model plan，不训练。
- 正式 DQN：ormal_dqn_guarded_plan 明确 blocked，需确认参数。
- 可视化与中文报告：generic/PEANUT/paper writer 路由包含图表、报告、一致性检查。
- run package/project_state：所有 route 都带 run package 与 project_state 更新要求。

## 本轮补强

新增 src/workflow1/one_line.py，并将 CLI dry-run --goal 接入结构化路由；新增 workflow_recipes/one_line_research_dry_run.yaml 与 model_registry/one_line_task_family_registry.yaml。

## 剩余缺口

- esearch_loop/ 尚未完成独立实验循环层，已列入 backlog。
- Zotero MCP、外部 AutoML agent、PDF OCR 仍需用户确认后才能安装或启用。
- 正式 DQN 仍需用户确认参数表。
