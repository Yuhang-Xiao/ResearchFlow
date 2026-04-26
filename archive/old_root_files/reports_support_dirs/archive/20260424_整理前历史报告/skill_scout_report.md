# Skill Scout Report

生成日期：2026-04-24  
范围：Codex skills、research automation agents、data science workflow skills、academic research skills、PDF/Zotero workflow、machine learning workflow agents、reinforcement learning experiment workflow。  
原则：本报告只吸收结构和方法，不复制外部代码，不在本次任务中启动真实数据处理或模型训练。

## 结论摘要

当前 workflow1 最适合采用“本地 repo-scoped skills + 项目记忆 + references + 轻量 CLI”的方式继续演进。外部项目提供了有用设计参考，但多数不是食品安全抽检数据的直接方案，不应整体引入。

## 已检索并可借鉴的项目

| 项目 | 方向 | 可借鉴点 | 本项目处理 |
|---|---|---|---|
| OpenAI Codex skills examples / docs | Codex skill 结构 | `SKILL.md` 使用 `name` 和 `description` metadata，按触发条件组织说明 | 已用于新建 `.agents/skills/*/SKILL.md` |
| ComposioHQ/awesome-codex-skills | Codex skill 清单 | curated skills、frontmatter description、按任务触发 | 借鉴目录和描述方式，不复制技能内容 |
| kujenga/zotero-mcp | Zotero MCP | 搜索 Zotero item、读取 metadata、读取 full text 的工具划分 | 作为未来 Zotero 联动参考；本次不安装 MCP |
| cookjohn/zotero-mcp | Zotero 插件 + MCP | 支持本地 Zotero、全文分析、多维检索的设计 | 作为 future literature workflow 参考；本次不接入 |
| Awesome-Auto-Research-Tools | 自动科研工具清单 | 将研究流程拆成 literature、experiment、writing、review 等阶段 | 借鉴为 run protocol 和 skill scout 思路 |
| DeepAuto-AI/automl-agent | AutoML agent | 多 agent 全流程 AutoML、任务拆分、评估与迭代 | 只借鉴分阶段思想；不引入重依赖 |
| clearml-agent / awesome-ml-experiment-management | ML experiment workflow | 实验 tracking、参数、metrics、artifact 管理 | 未来建模阶段可借鉴 experiments 结构 |
| ServiceNow/PipelineRL-SWE | RL experiment workflow | RL pipeline 分解、actor/verifier/trainer 等模块化思路 | 仅作为 DQN/POMDP 可行性阶段参考，不训练 |

## 推荐吸收的结构

1. 将 repo-scoped skills 放在 `.agents/skills/`，并保留 legacy `skills/` 兼容层。
2. 每个新增 skill 使用 `name` 和 `description` frontmatter。
3. 自动科研流程必须先读项目记忆、run protocol、references，再决定是否进入数据或模型阶段。
4. 文献/Zotero 流程未来应优先搜索 metadata，再读取 full text 或 deepread 笔记。
5. ML/RL 工作流应在训练前强制记录 target、unit of analysis、split、metric、leakage risk、state/action/reward feasibility。
6. 长时间研究流程需要 `project_state/lessons_learned.md` 和 `conversation_handoff.md` 防止重复劳动。

## 暂不引入的内容

- 不引入完整 AutoML/RL 框架。
- 不接入 Zotero MCP server 或 API key。
- 不复制外部 repo 代码。
- 不启动任何文献全文读取、真实数据清洗、模型训练或可视化。

## 后续建议

- 若用户要求 Zotero 联动，可先检查 `D:\桌面\codex\zotero` 的本地结构，再决定是否使用 MCP 或普通文件读取。
- 若进入建模阶段，先实现轻量 experiment registry，再考虑 MLflow/ClearML 等工具。
- 若进入 DQN/POMDP 阶段，先建立 feasibility checklist，确认状态、动作、奖励、时间顺序和策略轨迹，不直接训练。

## 参考链接

- OpenAI Codex skills docs/examples: https://github.com/openai/codex
- Composio awesome Codex skills: https://github.com/ComposioHQ/awesome-codex-skills
- kujenga Zotero MCP: https://github.com/kujenga/zotero-mcp
- cookjohn Zotero MCP: https://github.com/cookjohn/zotero-mcp
- Awesome Auto Research Tools: https://github.com/handsome-rich/Awesome-Auto-Research-Tools
- AutoML-Agent: https://github.com/DeepAuto-AI/automl-agent
- ClearML Agent: https://github.com/clearml/clearml-agent
- PipelineRL-SWE: https://github.com/ServiceNow/PipelineRL-SWE

