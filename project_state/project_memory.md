# Project Memory

## Auto-Repair Long-Term Rule

后续任务中，Codex 应自主修复轻量依赖缺失、路径错误、中文文件名问题、普通图表/表格输出问题和非关键代码错误；只有在 API/权限/手动配置、原始数据无法读取、关键字段缺失、核心外部参数缺失、可能破坏原始数据或会影响科研结论的问题上才停止询问用户。

具体执行要求：遇到 `tabulate`、`matplotlib`、`seaborn`、`openpyxl`、`python-docx`、`pypdf` 等轻量依赖缺失时，优先使用已有依赖、标准库、CSV、SVG、Markdown 或纯 Python 替代方案；遇到中文路径、空格、特殊字符、sheet 名称不一致、输出目录缺失、普通 dtype 转换或编码问题时，先尝试 1-3 种自动修复。所有自动修复、降级执行和未解决错误都应记录到任务 error log，并在必要时更新 `lessons_learned.md` 和 `decision_log.md`。

## 长期研究方向

本项目长期服务于食品安全风险监测、抽检数据治理、污染物风险评估、监管策略模拟和可解释机器学习研究。当前重点方向是以花生及其制品中的 AFB1 等风险因子为主线，构建可复用的数据清洗、标签工程、风险面板、建模、仿真、优化、可视化和报告流程。

## 用户偏好

- 默认中文交流和中文报告。
- 原始中文字段名必须保留，不要盲目翻译。
- Algorithm、model、package、parameter、metric、official standard name 可保留 English。
- 希望以后用一句话启动，不再重复长 prompt。
- 希望 Codex 自动读取项目记忆、references、skills、历史决策和交接文件。
- 不要在没有明确任务边界时处理真实数据。
- 所有原始数据必须保持不可变，不能修改 `data/01_raw`。

## 当前食品安全风险监测研究主线

面向食品安全抽检数据，逐步构建：

- 原始数据 schema inventory；
- raw validation；
- 清洗计划与清洗日志；
- 产品类别、污染物、浓度、限量、合格/不合格、风险标签；
- AFB1 等危害因子的暴露与风险评估数据结构；
- MOE/EDI、Beta-Binomial、POMDP、DQN 或其他优化/仿真模型的可行性判断；
- 监督学习 baseline；
- 监管风险监测可视化和技术报告。

## 花生/AFB1 项目的长期目标

- 基于花生抽检数据构建 AFB1 风险监测数据集。
- 判断是否具备 MOE/EDI、Beta-Binomial、POMDP、DQN 等方法的数据条件。
- 建立浓度提取、单位统一、限量匹配、风险标签构建和监管决策变量整理流程。
- 在数据条件允许时进行 baseline modeling、风险分层、可视化和报告。

## 推荐数据结构

- `data/01_raw`: 原始数据，只读。
- `data/02_intermediate`: 解析、标准化、轻转换数据。
- `data/03_primary`: 清洗后的分析就绪表。
- `data/04_feature`: 特征工程与风险标签。
- `data/05_model_input`: 建模矩阵、split、target、features。
- `reports/tables`: schema、validation、EDA、模型比较表。
- `reports/figures`: 图表输出。
- `experiments`: baseline、advanced、comparison artifacts。

## 推荐输出格式

- 中文 Markdown 技术报告。
- UTF-8-SIG CSV 表格，便于 Excel 打开。
- 必要时输出 JSON/YAML 机器可读摘要。
- 图表应带中文标题/标签，技术缩写可保留英文。
- 每个阶段都记录输入、输出、假设、限制和下一步。

## 重要注意事项

- 参考资料不是自动生效的规则，必须与用户指令和实际数据证据核对。
- 用户明确指令优先于 reference 文档。
- 实际数据证据优先于泛化文献建议。
- 扫描版 PDF 默认没有 OCR。
- POMDP/DQN 等高级模型必须先判断状态、动作、奖励、转移或轨迹数据是否具备。
- 在没有明确 target、unit of analysis 和 leakage 检查前，不应训练模型。

## Upstream Verification Long-Term Rule

任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。

## Upstream Verification Long-Term Rule

任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。

## 20260424 PEANUT MOE/EDI memory

- 每个实质性任务必须创建 `outputs/YYYYMMDD_中文任务名/` 独立输出目录，并将关键结果、报告、图表、日志和 README 同步整理到该目录。
- PEANUT 当前已有 MOE/EDI 风险度量基础：消费量、人口、60 kg 体重、BMDL 情景和风险 proxy 已接入 belief-MDP 状态特征。
- 当前不要进入正式 DQN；仍需动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

## 20260424 PEANUT MOE/EDI memory

- 每个实质性任务必须创建 `outputs/YYYYMMDD_中文任务名/` 独立输出目录，并将关键结果、报告、图表、日志和 README 同步整理到该目录。
- PEANUT 当前已有 MOE/EDI 风险度量基础：消费量、人口、60 kg 体重、BMDL 情景和风险 proxy 已接入 belief-MDP 状态特征。
- 当前不要进入正式 DQN；仍需动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 20260424 Whole workspace organization memory

- 后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。
- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。

## 2026-04-24 23:56 Run Package Memory

- 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。
- 新对话继续任务时，先读 `outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml` 和 `project_state/conversation_handoff.md`。

## 2026-04-24 23:57 Run Package Memory

- 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。
- 新对话继续任务时，先读 `outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml` 和 `project_state/conversation_handoff.md`。

## 2026-04-25 00:20 Run Package Cleanup Memory

- 以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。
- 后续继续任务时先读 `outputs/_index/run_index.md` 和 `project_state/conversation_handoff.md`。

## 2026-04-25 DQN 文档治理记忆

- 正式 DQN、POMDP、belief-MDP、constrained RL 和 safe RL 任务必须先读取用户研究计划、模型设定文档、Zotero note/PDF，并执行 document-governed-modeling、zotero-literature-auditor、environment-auditor、dqn-readiness-auditor。
- `20260425_1132_DQN初步运行` 只作为 sandbox prototype，不能作为正式 DQN state/action/reward/constraint/training 设定依据。
- Zotero note 若出现大量 `?????`，不能直接作为正式依据，必须追溯 PDF 或正式出版页面。
- 正式 DQN 前必须逐解释器查验 `torch`；默认 Python 无 `torch` 时不得直接降级为 sklearn。用户指定 `D:/anaconda3/envs/myevn1/python.exe` 当前未发现，候选 `D:/anaconda3/envs/myenv1/python.exe` 需用户确认。
- 在用户确认参数表前，只能输出 readiness、参数确认表和模型规范抽取，不允许运行正式 DQN。

## 2026-04-25 DQN 环境修复记忆

- 正式 DQN 环境已固定为 `D:\anaconda3\envs\myenv1\python.exe`，不要再使用默认 Python、base 环境或错误路径 `D:\anaconda3\envs\myevn1\python.exe`。
- `myenv1` 中旧 `torch 2.11.0+cu130` / `torchvision 0.26.0+cu130` 已卸载，已安装 `torch 2.11.0+cu126`、`torchvision 0.26.0+cu126`、`torchaudio 2.11.0+cu126`。
- CUDA 12.6 PyTorch 验证通过：`torch.cuda.is_available()` 为 True，GPU 为 `NVIDIA GeForce RTX 4060 Ti`，10-step torch GPU smoke test 通过，未再观察到 OpenMP 冲突。
- 环境技术上可支持下一步 DQN，但正式训练仍必须等待参数确认表获用户确认。

## 2026-04-26 17:09:05 Workflow Self-Improvement Memory

workflow1 具备自我升级机制。Codex 在用户要求优化工作流时，应通过 workflow-self-improvement-scout 自动搜索 GitHub 和开源社区，评估可升级项，安全转化为本地 skills、recipes、registries 和 runners；高风险外部插件进入 approval queue 等待用户确认。

## 2026-04-26 17:22:53 One-line Research Workflow Memory

workflow1 的一句话 dry-run 路由已补强。后续 python -m workflow1 --stage dry-run --goal "..." 应返回结构化 intent/mode/required skills/planned stages/quality gates/approval_required/block_reason，而不是只返回泛化 ok。真实数据处理、清洗、训练、正式 DQN 仍需用户授权和参数确认。


## 2026-04-26 18:30:50 Experimental DQN memory

- workflow1 已完成一次 `自动合成参数 DQN 实验版 / self-synthesized DQN experimental run`，工作包 `outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`。
- 本轮证明 one-line dry-run、canonical 数据、文献证据、myenv1 GPU、DQN 训练代码、输出系统可以闭环。
- 该结果不是 formal DQN；正式版本仍需用户确认参数并另建 formal config。
- reward 中人口/规模 proxy 必须归一化后进入 DQN。

## 2026-04-26 Research Quality Long-Term Memory

后续所有科研任务都必须执行科研质量核验：数据生成与派生数据核验、多模型对比、baseline 公平性、reward/收敛/约束审计、图表和表格 QA、顶级期刊文献对标、引用核验、论文论断保护、Reviewer 2 风格自审。发现缺口时，Codex 应通过 workflow-self-improvement-scout 搜索并安全吸收相关 skill 或工具，高风险项进入 approval queue。

## 2026-04-26 20:51:24 DQN experimental run guardrail

本轮 DQN 修正版输出只能作为 experimental 参考；即使多模型对比和质量门控完成，也不能作为 formal DQN 或正式监管政策结论，直到用户逐项确认参数并重跑 formal config。

## 2026-04-26 20:55:03 DQN experimental run guardrail

本轮 DQN 修正版输出只能作为 experimental 参考；即使多模型对比和质量门控完成，也不能作为 formal DQN 或正式监管政策结论，直到用户逐项确认参数并重跑 formal config。

## 2026-04-26 20:57:02 DQN experimental run guardrail

本轮 DQN 修正版输出只能作为 experimental 参考；即使多模型对比和质量门控完成，也不能作为 formal DQN 或正式监管政策结论，直到用户逐项确认参数并重跑 formal config。


## 2026-04-26 输出解释与论文升级长期记忆

所有图、表、模型输出、代码、Word 和文献输出必须带解释、来源、阅读方式、局限和 evidence map。DQN/RL experimental 结果不得写成 formal 监管结论。Zotero 只允许 sidecar notes/BibTeX/RIS/CSV 待导入，未经确认不得写 SQLite。


## 2026-04-26 输出解释与论文升级长期记忆

所有图、表、模型输出、代码、Word 和文献输出必须带解释、来源、阅读方式、局限和 evidence map。DQN/RL experimental 结果不得写成 formal 监管结论。Zotero 只允许 sidecar notes/BibTeX/RIS/CSV 待导入，未经确认不得写 SQLite。


## 2026-04-26 输出解释与论文升级长期记忆

所有图、表、模型输出、代码、Word 和文献输出必须带解释、来源、阅读方式、局限和 evidence map。DQN/RL experimental 结果不得写成 formal 监管结论。Zotero 只允许 sidecar notes/BibTeX/RIS/CSV 待导入，未经确认不得写 SQLite。


## 2026-04-26 输出解释与论文升级长期记忆

所有图、表、模型输出、代码、Word 和文献输出必须带解释、来源、阅读方式、局限和 evidence map。DQN/RL experimental 结果不得写成 formal 监管结论。Zotero 只允许 sidecar notes/BibTeX/RIS/CSV 待导入，未经确认不得写 SQLite。


## 2026-04-26 输出解释与论文升级长期记忆

所有图、表、模型输出、代码、Word 和文献输出必须带解释、来源、阅读方式、局限和 evidence map。DQN/RL experimental 结果不得写成 formal 监管结论。Zotero 只允许 sidecar notes/BibTeX/RIS/CSV 待导入，未经确认不得写 SQLite。


## Output Explanation Co-location Memory

解释要贴着结果走：每个输出目录必须有 README/local explanation，关键 artifact 应有同名 `.explanation.md`；`10_输出解释与索引/` 仅作导航。
