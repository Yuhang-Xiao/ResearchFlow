# Lessons Learned

## 2026-04-24 Auto-Repair Lessons

- 后续任务中，Codex 应自主修复轻量依赖缺失、路径错误、中文文件名问题、普通图表/表格输出问题和非关键代码错误；只有在 API/权限/手动配置、原始数据无法读取、关键字段缺失、核心外部参数缺失、可能破坏原始数据或会影响科研结论的问题上才停止询问用户。
- 缺少 `tabulate` 时不要停止，可用内置 Markdown 表格生成函数；缺少 `matplotlib`/`seaborn` 时不要停止，可用 SVG、CSV、Markdown 或纯 Python 替代图表输出。
- 中文路径或 Word/PDF 文件名传递失败时，优先用 `pathlib`、相对路径、目录扫描和文件名匹配。
- 所有自动修复和降级执行必须写入任务 error log，并区分“已自动修复”“已降级处理”“未解决需用户处理”。

本文件用于记录每轮运行后沉淀的可复用经验。当前尚未开始新的真实数据处理任务。

## 数据问题经验

- 待补充。

## 清洗规则经验

- 保留原始中文字段名。
- cleaning-plan 只生成建议，不代表已执行清洗。

## 标签工程经验

- AFB1、限量、合格/不合格、风险等级、暴露风险等标签应在明确字段含义和参考标准后构建。

## 模型设定经验

- POMDP/DQN 不应默认训练；必须先判断是否存在状态、动作、奖励、时间顺序或监管策略轨迹。

## 文献方法经验

- 待根据 `references/` 和 Zotero/deepread 笔记补充。

## 失败和修正

- 迁移后发现历史任务状态可能污染新任务，因此需要用 `project_state/current_focus.md` 和 `conversation_handoff.md` 明确当前状态。

## 下次自动流程应避免的问题

- 不要把历史四川分类任务当作当前任务。
- 不要读取或处理 raw 数据，除非用户明确启动对应阶段。
- 不要将参考资料建议直接套用到实际数据。


## 2026-04-24

- 花生 AFB1 任务中，`检测数值` 可能同时包含初检与复检，应复检优先并保留原始文本。
- AFB1 识别不能用“生物毒素”泛化，需要 `黄曲霉`、`AFB1`、`B1/B₁` 等上下文关键词与人工复核标记。
- 后续 POMDP/DQN 前必须先有省份—时间—环节计数面板，以及成本、预算、产能、消费量、人口、体重、BMDL 等外部参数。

## 2026-04-24 Beta-Binomial Belief Update Lessons

- 在没有专家先验时，可用 Beta(1,1) 作为弱信息先验启动原型，但必须在报告中标记为可调整假设。
- 对 AFB1 风险建议同时保留“全样本分母”和“AFB1相关记录条件分母”两条信念轨道，便于后续监管目标在检出概率与条件严重性之间切换。
- belief-MDP 状态表应保留 alpha、beta、后验均值、后验方差、样本覆盖强度和浓度可用率，以同时表达风险水平与不确定性。

## 2026-04-24 Beta-Binomial Belief Update Lessons

- 在没有专家先验时，可用 Beta(1,1) 作为弱信息先验启动原型，但必须在报告中标记为可调整假设。
- 对 AFB1 风险建议同时保留“全样本分母”和“AFB1相关记录条件分母”两条信念轨道，便于后续监管目标在检出概率与条件严重性之间切换。
- belief-MDP 状态表应保留 alpha、beta、后验均值、后验方差、样本覆盖强度和浓度可用率，以同时表达风险水平与不确定性。

## 2026-04-24 Upstream Verification Lessons

- 任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。
- 计数面板中的 `浓度可用记录数` 对 AFB1 风险建模应采用 AFB1 相关浓度可用口径，而不是全表任意检测数值可用口径。
- `是否超标` 应优先由统一单位后的浓度和法规限量计算，再与原始判定结果交叉校验。

## 2026-04-24 Beta-Binomial Belief Update Lessons

- 在没有专家先验时，可用 Beta(1,1) 作为弱信息先验启动原型，但必须在报告中标记为可调整假设。
- 对 AFB1 风险建议同时保留“全样本分母”和“AFB1相关记录条件分母”两条信念轨道，便于后续监管目标在检出概率与条件严重性之间切换。
- belief-MDP 状态表应保留 alpha、beta、后验均值、后验方差、样本覆盖强度和浓度可用率，以同时表达风险水平与不确定性。

## 2026-04-24 Upstream Verification Lessons

- 任何下游模型任务启动前，必须先执行上游输出查验。发现上游遗漏问题时，应优先自动修复并重建受影响产物；不得带着已知错误进入下游模型。
- 计数面板中的 `浓度可用记录数` 对 AFB1 风险建模应采用 AFB1 相关浓度可用口径，而不是全表任意检测数值可用口径。
- `是否超标` 应优先由统一单位后的浓度和法规限量计算，再与原始判定结果交叉校验。

## 20260424

- 消费量数据与监管面板年份不一致时，可用同省最近年份作为 prototype 回退，但必须标记人工复核，不能作为正式论文结论直接使用。
- 省级人口英文长表可通过省份中英文映射、同年优先和最近年份回退接入 belief-MDP 状态特征。
- 截图给出的 BMDL P1/P5/P95/P99 若与敏感性命名方向存在歧义，应保留情景值并记录歧义，避免强行解释为普通统计分位数。
- 每个实质性任务必须创建 `outputs/YYYYMMDD_中文任务名/` 独立输出目录，并将关键结果、报告、图表、日志和 README 同步整理到该目录。

## 20260424

- 消费量数据与监管面板年份不一致时，可用同省最近年份作为 prototype 回退，但必须标记人工复核，不能作为正式论文结论直接使用。
- 省级人口英文长表可通过省份中英文映射、同年优先和最近年份回退接入 belief-MDP 状态特征。
- 截图给出的 BMDL P1/P5/P95/P99 若与敏感性命名方向存在歧义，应保留情景值并记录歧义，避免强行解释为普通统计分位数。
- 每个实质性任务必须创建 `outputs/YYYYMMDD_中文任务名/` 独立输出目录，并将关键结果、报告、图表、日志和 README 同步整理到该目录。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 20260424

- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。
- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。
- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。

## 2026-04-24 23:56

- `latest/archive` 适合机器可读和历史保底，但不适合做人类主入口；科研工作流更需要按“时间 + 工作内容”的任务包组织。
- canonical 文件应保留在标准目录以保护 pipeline，任务包保存完整可读副本以保护可追溯性。

## 2026-04-24 23:57

- `latest/archive` 适合机器可读和历史保底，但不适合做人类主入口；科研工作流更需要按“时间 + 工作内容”的任务包组织。
- canonical 文件应保留在标准目录以保护 pipeline，任务包保存完整可读副本以保护可追溯性。

## 2026-04-25 00:20

- 科研工作流的主查看入口应按任务组织，而不是按文件状态组织。
- hash 去重应保守执行：删除缓存和完全重复辅助副本，保护唯一数据、报告、代码、配置和参考资料。
- `data/01_raw` 只允许 inventory sidecar，不参与移动和删除。
## 2026-04-25 11:40

- DQN 正式运行前必须区分“技术可跑”和“策略可用”：在没有真实动作、成本、预算和约束参数时，只能做 sandbox prototype。
- 当前环境未安装 `torch` 时，可用 `sklearn.MLPRegressor` 做 Fitted Q iteration 作为轻量烟测，但需在报告中明确不是完整 PyTorch DQN。
- 食品安全监管 DQN 更接近 constrained/safe RL：reward 不应只优化风险降低，还应把预算、产能、最低覆盖、召回/处置成本和信息价值纳入约束或惩罚。
- Zotero Desktop 本地 API 端口未开启时，可退回 Zotero Web API；中文 note 写入需使用 UTF-8 脚本，避免 PowerShell 管道污染中文路径或正文。

## 2026-04-25 12:08

- 正式 DQN 前必须先做 document-governed modeling：研究计划若只给出概念结构，Codex 只能生成候选参数表，不能把经验值写成正式参数。
- 检查 Python/torch 时不能只看默认 Python；本轮默认 Python 无 `torch`，但相邻 Conda 环境 `myenv1` 有 PyTorch，说明环境结论必须逐解释器记录。
- 用户给出的环境名可能存在拼写差异；发现候选环境时应记录但不得擅自替换为正式解释器。
- Zotero note 出现大量 `?????` 时，应判为不可直接引用，并优先追溯 PDF 或正式出版页面。

## 2026-04-25 13:00

- PyTorch CUDA build 必须与本机驱动能力匹配；`cu130` 在当前机器上会导致 CUDA 不可用，`cu126` 验证通过。
- DQN 环境修复必须使用解释器显式路径执行 `python.exe -m pip`，避免误装到 base 或默认 Python。
- pip 卸载/升级后可能留下 `~orch`、`~umpy` 等临时目录；这些是非阻断警告，但后续清理时仍需保守确认，不应删除系统 DLL 或整个环境。
- 通过 10-step GPU forward/backward smoke test 比单纯 `import torch` 更可靠，可同时验证 CUDA、autograd、optimizer 和 OpenMP 冲突状态。

## 2026-04-26 16:28:01 DQN 文献增强建模经验

- PEANUT formal DQN 应表述为 MOE/EDI 风险驱动的 belief-MDP / constrained MDP，而不是直接从 sandbox prototype 继承 state/action/reward。
- DQN 文献只能证明近似动态规划和训练机制；食品安全监管参数必须由用户文档、监管约束、风险评估参数和用户确认共同决定。
- Zotero note 中含 ????? 的 DQN 方法笔记不可作为正式依据；应追溯 PDF/出版页面或重做无乱码中文笔记。

## 2026-04-26 17:09:05 Workflow self-improvement lesson

- 工作流升级应以本地轻量 adaptation 为默认路径，优先新增 SKILL.md、recipe、registry、stub 和 dry-run，而不是安装或执行外部项目。
- Zotero MCP、AutoML agent、data science agent 等外部集成有价值，但涉及服务、依赖、数据库或第三方代码执行，必须进入 approval queue。

## 2026-04-26 17:22:53 One-line dry-run lesson

- 一句话启动能力不能只返回 ok；必须返回 intent、mode、required skills、planned stages、quality gates、approval_required、block_reason 和 run package/project_state 要求。
- 正式 DQN 即使用户写“已确认参数”，也应先 dry-run 检查确认表与训练许可，不得直接训练。


## 2026-04-26 18:30:50 DQN experimental lessons

- 报告生成不应依赖可选 `tabulate`；缺失时可用 CSV fenced block。
- reward 中人口或规模 proxy 必须归一化，否则会导致 Q 值和 loss 数量级异常。
- Matplotlib SVG 在当前环境会提示 CJK 字体缺字；后续可配置中文字体，但不影响核心 CSV/Excel/模型输出。

## 2026-04-26 Research Quality Lessons

- 后续科研结果必须 evidence-first；所有模型、图表、表格、论文段落和引用都要通过对应质量门。
- 多模型比较、baseline fairness、reward/convergence/constraint audit 是正式模型结果进入论文前的硬性条件。
- 外部验证工具可作为方法来源，但安装、MCP、API、Zotero 数据库写入和大型依赖必须进入 approval queue。

## 2026-04-26 20:51:24 DQN 修正版训练经验

- PNG 主图与 chart QA 可防止 SVG 中文异常和空图问题。
- reward 需要显式 decomposition 和 robust rescaling，否则 cost/penalty 容易压过 risk reward。
- 高维二元动作空间暂不宜直接训练，应先转为 top-k、factorized action 或组合优化后处理。

## 2026-04-26 20:55:03 DQN 修正版训练经验

- PNG 主图与 chart QA 可防止 SVG 中文异常和空图问题。
- reward 需要显式 decomposition 和 robust rescaling，否则 cost/penalty 容易压过 risk reward。
- 高维二元动作空间暂不宜直接训练，应先转为 top-k、factorized action 或组合优化后处理。

## 2026-04-26 20:57:02 DQN 修正版训练经验

- PNG 主图与 chart QA 可防止 SVG 中文异常和空图问题。
- reward 需要显式 decomposition 和 robust rescaling，否则 cost/penalty 容易压过 risk reward。
- 高维二元动作空间暂不宜直接训练，应先转为 top-k、factorized action 或组合优化后处理。


## 2026-04-26 DQN 输出复核经验

旧 DQN 包可能包含 0 字节图或近似空表；最新图即使非空也可能语义不足（如全 0 约束图）。未来必须做空图、全 0、无差异和中文字体 QA，并生成解释性图或说明。


## 2026-04-26 DQN 输出复核经验

旧 DQN 包可能包含 0 字节图或近似空表；最新图即使非空也可能语义不足（如全 0 约束图）。未来必须做空图、全 0、无差异和中文字体 QA，并生成解释性图或说明。


## 2026-04-26 DQN 输出复核经验

旧 DQN 包可能包含 0 字节图或近似空表；最新图即使非空也可能语义不足（如全 0 约束图）。未来必须做空图、全 0、无差异和中文字体 QA，并生成解释性图或说明。


## 2026-04-26 DQN 输出复核经验

旧 DQN 包可能包含 0 字节图或近似空表；最新图即使非空也可能语义不足（如全 0 约束图）。未来必须做空图、全 0、无差异和中文字体 QA，并生成解释性图或说明。


## 2026-04-26 DQN 输出复核经验

旧 DQN 包可能包含 0 字节图或近似空表；最新图即使非空也可能语义不足（如全 0 约束图）。未来必须做空图、全 0、无差异和中文字体 QA，并生成解释性图或说明。
