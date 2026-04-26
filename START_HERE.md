# START HERE

本项目是 Codex 辅助的食品安全风险监测与自动科研工作流仓库。它用于把原始抽检数据、研究计划、参考文献、标准文件、历史项目记忆和可复用 skills 串联起来，逐步完成数据 intake、validation、cleaning plan、清洗、标签工程、风险面板构建、EDA、模型设定、基线建模、仿真/优化可行性判断、可视化、报告和项目记忆更新。

当前版本已经搭建“一句话启动”框架和最小数据准备阶段，但不会在没有明确启动和足够数据上下文时自动处理真实数据。

## 一句话启动方式

以后可以直接对 Codex 说：

- “启动花生风险监管自动科研流程，使用当前 raw 数据和研究计划文档。”
- “启动自动科研流程，目标是：基于花生抽检数据构建 AFB1 风险监测数据集，并判断是否具备 MOE/EDI、Beta-Binomial、POMDP 和 DQN 建模条件。”
- “继续上次任务，请先读 project_state/conversation_handoff.md。”
- “仅执行数据清洗与标签工程，不做模型。”
- “执行完整流程，但不要训练 DQN，只判断 POMDP/DQN 可行性。”

Codex 收到这些短命令后，应自动读取项目规则、项目记忆、run protocol、references、历史决策和相关 skills，而不是要求用户重复长 prompt。

## 默认短命令与触发流程

| 短命令 | 默认行为 |
|---|---|
| 启动自动科研流程 | 读取记忆、参考资料和 raw inventory，规划并执行当前可用流程 |
| 启动花生风险监管流程 | 面向花生/AFB1 风险监测主线启动 workflow |
| 继续上次任务 | 先读 `project_state/conversation_handoff.md` 和 `project_state/next_step.md` |
| 只做清洗 | 执行 reference reading、intake、validation、cleaning plan，并在确认后进入清洗 |
| 只做建模 | 使用已有清洗表和建模计划，先做 model framing 和 baseline modeling |
| 只做可视化 | 使用已有分析结果或用户指定表格生成图表计划和图表 |
| 读取文献并更新方法 | 读取 `references/` 和 Zotero/deepread 笔记，更新方法摘要 |
| 生成交接文件 | 更新 `project_state/conversation_handoff.md` |

## 运行前需要放置的文件

- 原始数据：放入 `data/01_raw/`，支持 `.csv` 和 `.xlsx`。
- 研究计划、清洗计划、建模计划、标准、文献：放入 `references/` 对应目录。
- Zotero 文献或 deepread 笔记：如存在，可放在或连接到 `D:\桌面\codex\zotero`。

## 输出位置

- schema inventory：`reports/` 和 `reports/tables/`
- validation report：`reports/` 和 `reports/tables/`
- cleaning plan：`reports/`
- 参考资料摘要：`references/processed_summaries/`
- 图表：`reports/figures/`
- 表格：`reports/tables/`
- 实验：`experiments/baselines/`、`experiments/advanced/`、`experiments/comparisons/`
- 项目记忆和下一步：`project_state/`

## 当前可运行的轻量命令

```powershell
workflow1 --stage launch
workflow1 --stage continue
workflow1 --stage intake
workflow1 --stage validation
workflow1 --stage cleaning-plan
workflow1 --stage memory-update
workflow1 --stage skill-scout
```

`launch`、`continue`、`memory-update` 和 `skill-scout` 当前是轻量启动器，不会直接跑重任务。


## Workflow Self-Improvement

说“优化当前工作流”即可触发自我升级机制：扫描能力缺口、搜索 GitHub/开源社区、应用低风险本地升级，并把高风险插件/MCP/API/依赖写入确认队列。
