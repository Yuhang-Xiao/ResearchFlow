# Run Index

任务工作包是以后人工查看结果的主入口：`outputs/工作包/`。

- [PEANUT数据清洗与风险底座](../工作包/20260424_1908_PEANUT数据清洗与风险底座/README.md) | `20260424_1908` | 数据清洗/风险底座
- [BetaBinomial信念更新](../工作包/20260424_2048_BetaBinomial信念更新/README.md) | `20260424_2048` | 信念状态
- [PEANUT上游查验与浓度修复](../工作包/20260424_2049_PEANUT上游查验与浓度修复/README.md) | `20260424_2049` | 上游核验/浓度修复
- [MOE_EDI外部参数匹配](../工作包/20260424_2132_MOE_EDI外部参数匹配/README.md) | `20260424_2132` | MOE/EDI风险度量
- [全工作目录整理与规范化](../工作包/20260424_2244_全工作目录整理与规范化/README.md) | `20260424_2244` | 目录整理/规则固化
- [工作流任务包机制重构](../工作包/20260424_2357_工作流任务包机制重构/README.md) | `20260424_2357` | 目录整理/规则固化
- [全工作流目录重构与去重](../工作包/20260425_0020_全工作流目录重构与去重/README.md) | `20260425_0020` | 目录整理/规则固化
- [DQN初步运行](../工作包/20260425_1132_DQN初步运行/README.md) | `20260425_1132` | DQN prototype/上游核验/文献入库
- [DQN文档驱动建模准备与参数确认](../工作包/20260425_1157_DQN文档驱动建模准备与参数确认/README.md) | `20260425_1157` | DQN readiness/文档抽取/文献环境审计
- [DQN环境修复_PyTorch_CUDA126安装](../工作包/20260425_1251_DQN环境修复_PyTorch_CUDA126安装/README.md) | `20260425_1251` | DQN 环境修复/PyTorch cu126/GPU smoke test

## 20260426_1616_DQN文献增强建模方案与参数确认

- 路径：outputs/工作包/20260426_1616_DQN文献增强建模方案与参数确认/`n- 结论：formal DQN blocked；已生成文献增强方案、参数确认表、readiness、环境审计和 Zotero 审计。


## 20260426_1702_工作流自我升级机制构建

- 路径：outputs/工作包/20260426_1702_工作流自我升级机制构建/
- 结论：已建立 Workflow Self-Improvement System，新增 policies、skills、recipes、Python stubs、CLI dry-run、approval queue 和 improvement ledger。
- 验证：skills-doctor、workflow-scout、workflow-upgrade-plan、dry-run 均通过。

## 20260426_1718_一句话自动科研验收与补强

- 路径：outputs/工作包/20260426_1718_一句话自动科研验收与补强/
- 结论：9 条一句话 dry-run 验收通过；已补强结构化 one-line router、recipe 和 task-family registry。
- 限制：未跑真实数据、未重新清洗、未训练模型、未运行 DQN。


## 20260426_1746_全流程验收与DQN自动参数训练
- 路径：`outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`
- 结论：一句话 dry-run 验收通过；self-synthesized DQN experimental run 使用 myenv1 + torch cu126 + RTX 4060 Ti 训练完成；formal DQN 仍需用户确认参数。

## 20260426_1857_科研质量核验_顶级文献对标_工作流强化
- 路径：`outputs/工作包/20260426_1857_科研质量核验_顶级文献对标_工作流强化`
- 结论：已建立科研质量核验、顶级期刊对标、多模型比较、论文/citation 质量和 workflow self-improvement after-task 机制；dry-run 待执行。

## 20260426_2000_指定清理与DQN修正版继续实验
- 路径：`outputs/工作包/20260426_2000_指定清理与DQN修正版继续实验`
- 结论：按用户最新指令仅完成删除候选扫描；未删除文件，未继续 DQN。等待用户从 `02_表格输出/delete_candidates.csv` 指定删除目标。

## 20260426_2050_推荐缓存删除与DQN修正版训练
- 路径：`outputs/工作包/20260426_2050_推荐缓存删除与DQN修正版训练`
- 结论：删除 recommended 缓存项 21 项；DQN 修正版 experimental run 已完成，输出 PNG、多模型对比、质量审计和 results_draft.docx。
- 限制：仍非 formal DQN，正式训练需用户确认参数。

## 20260426_2054_推荐缓存删除与DQN修正版训练
- 路径：`outputs/工作包/20260426_2054_推荐缓存删除与DQN修正版训练`
- 结论：删除 recommended 缓存项 21 项；DQN 修正版 experimental run 已完成，输出 PNG、多模型对比、质量审计和 results_draft.docx。
- 限制：仍非 formal DQN，正式训练需用户确认参数。

## 20260426_2056_推荐缓存删除与DQN修正版训练
- 路径：`outputs/工作包/20260426_2056_推荐缓存删除与DQN修正版训练`
- 结论：删除 recommended 缓存项 21 项；DQN 修正版 experimental run 已完成，输出 PNG、多模型对比、质量审计和 results_draft.docx。
- 限制：仍非 formal DQN，正式训练需用户确认参数。

## 20260426_2245_DQN输出复核_解释体系与论文输出升级

- 时间：2026-04-26T22:45:10
- 类型：DQN输出复核_解释体系与论文输出升级
- 路径：`outputs/工作包/20260426_2245_DQN输出复核_解释体系与论文输出升级`
- 状态：completed_experimental_audit_and_workflow_upgrade
- 关键输出：deep audit、解释索引、图表修复、DQN 设置说明、结果解读、文献/Zotero 侧车、Results DOCX、dry-run。

## 20260426_2245_DQN输出复核_解释体系与论文输出升级

- 时间：2026-04-26T22:45:37
- 类型：DQN输出复核_解释体系与论文输出升级
- 路径：`outputs/工作包/20260426_2245_DQN输出复核_解释体系与论文输出升级`
- 状态：completed_experimental_audit_and_workflow_upgrade
- 关键输出：deep audit、解释索引、图表修复、DQN 设置说明、结果解读、文献/Zotero 侧车、Results DOCX、dry-run。

## 20260426_2249_DQN输出复核_解释体系与论文输出升级

- 时间：2026-04-26T22:49:43
- 类型：DQN输出复核_解释体系与论文输出升级
- 路径：`outputs/工作包/20260426_2249_DQN输出复核_解释体系与论文输出升级`
- 状态：completed_experimental_audit_and_workflow_upgrade
- 关键输出：deep audit、解释索引、图表修复、DQN 设置说明、结果解读、文献/Zotero 侧车、Results DOCX、dry-run。

## 20260426_2252_DQN输出复核_解释体系与论文输出升级

- 时间：2026-04-26T22:52:15
- 类型：DQN输出复核_解释体系与论文输出升级
- 路径：`outputs/工作包/20260426_2252_DQN输出复核_解释体系与论文输出升级`
- 状态：completed_experimental_audit_and_workflow_upgrade
- 关键输出：deep audit、解释索引、图表修复、DQN 设置说明、结果解读、文献/Zotero 侧车、Results DOCX、dry-run。

## 20260426_2254_DQN输出复核_解释体系与论文输出升级

- 时间：2026-04-26T22:54:52
- 类型：DQN输出复核_解释体系与论文输出升级
- 路径：`outputs/工作包/20260426_2254_DQN输出复核_解释体系与论文输出升级`
- 状态：completed_experimental_audit_and_workflow_upgrade
- 关键输出：deep audit、解释索引、图表修复、DQN 设置说明、结果解读、文献/Zotero 侧车、Results DOCX、dry-run。

## 20260426_2317_输出解释就地化修正与DQN代码深度说明补强

- 时间：2026-04-26T23:17:57
- 类型：输出解释就地化修正与DQN代码深度说明补强
- 路径：`outputs/工作包/20260426_2317_输出解释就地化修正与DQN代码深度说明补强`
- 状态：completed
- 说明：将解释就地化到每个输出目录，并补强 DQN code-to-method/code-to-output 映射。

## 20260426_2332_输出解释精简_项目存档与Word学术升级

- 时间：2026-04-26T23:32:20
- 类型：输出解释精简、项目存档、缓存清理与 Word 学术升级
- 路径：`outputs/工作包/20260426_2332_输出解释精简_项目存档与Word学术升级`
- 存档：`archive/project_snapshots/workflow1_curated_project_snapshot_20260426_2332.zip`
- Word：`outputs/工作包/20260426_2332_输出解释精简_项目存档与Word学术升级/09_论文输出/09_word导出/dqn_results_academic_with_figures.docx`
- 删除项：93

## 20260426_2334_输出解释精简_项目存档与Word学术升级

- 时间：2026-04-26T23:34:45
- 类型：输出解释精简、项目存档、缓存清理与 Word 学术升级
- 路径：`outputs/工作包/20260426_2334_输出解释精简_项目存档与Word学术升级`
- 存档：`archive/project_snapshots/workflow1_curated_project_snapshot_20260426_2334.zip`
- Word：`outputs/工作包/20260426_2334_输出解释精简_项目存档与Word学术升级/09_论文输出/09_word导出/dqn_results_academic_with_figures.docx`
- 删除项：1

## 20260426_2335_输出解释精简_项目存档与Word学术升级

- 时间：2026-04-26T23:35:13
- 类型：输出解释精简、项目存档、缓存清理与 Word 学术升级
- 路径：`outputs/工作包/20260426_2335_输出解释精简_项目存档与Word学术升级`
- 存档：`archive/project_snapshots/workflow1_curated_project_snapshot_20260426_2335.zip`
- Word：`outputs/工作包/20260426_2335_输出解释精简_项目存档与Word学术升级/09_论文输出/09_word导出/dqn_results_academic_with_figures.docx`
- 删除项：1

## 20260426_2336_输出解释精简_项目存档与Word学术升级

- 时间：2026-04-26T23:36:41
- 类型：输出解释精简、项目存档、缓存清理与 Word 学术升级
- 路径：`outputs/工作包/20260426_2336_输出解释精简_项目存档与Word学术升级`
- 存档：`archive/project_snapshots/workflow1_curated_project_snapshot_20260426_2336.zip`
- Word：`outputs/工作包/20260426_2336_输出解释精简_项目存档与Word学术升级/09_论文输出/09_word导出/dqn_results_academic_with_figures.docx`
- 删除项：1
