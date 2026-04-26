# 初始工作流自我升级报告

## 当前缺口

workflow1 原已有项目记忆、run package、领域技能、DQN readiness 和组织技能，但缺少一个长期可复用的自我升级中枢：缺口扫描 schema、候选项目评分、approval queue、improvement ledger、CLI dry-run、skills doctor 和安全补丁边界。

## 本轮低风险升级

- 新增 `workflow_improvement/` 策略与 ledger。
- 新增 8 个自我升级相关 skills，并同步到 `skills/` 与 `.agents/skills/`。
- 新增 5 个 workflow self-improvement recipes 和 command intents。
- 新增 `src/workflow1/self_improvement/` 轻量 stub。
- 新增 `model_registry/` 占位注册表。
- 更新 `START_HERE.md` 与 `prompts/one_line_launchers.md`。

## 高风险项

Zotero MCP、外部 AutoML/data-science agent、MCP server、API key、依赖安装、第三方脚本执行均进入确认边界，不自动应用。
