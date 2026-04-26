# Run Protocol

1. 新任务开始前读取 `AGENTS.md`、`outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml` 和 `project_state/conversation_handoff.md`。
2. 先调用 run-package-manager 创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
3. 所有新产物优先写入任务工作包；pipeline 必需文件再复制到标准 canonical 目录。
4. 任务结束后调用 whole-workspace-organizer，更新全局索引和项目状态。
5. 永远不修改、删除、重命名、移动 `data/01_raw` 原始数据。

长期规则：以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。

## DQN Environment Protocol

1. DQN 环境安装、验证、smoke test 和正式训练必须显式使用 `D:\anaconda3\envs\myenv1\python.exe`。
2. 不允许用默认 `python`、base 环境或错误路径 `D:\anaconda3\envs\myevn1\python.exe` 执行正式 DQN。
3. 当前正式 DQN PyTorch 构建为 CUDA 12.6 / `cu126`；不得回退到 `cu130`，除非驱动升级并重新验证。
4. 正式 DQN 前必须通过 GPU smoke test；若 GPU 不可用，必须记录 CPU 降级并等待用户确认。

## Workflow Self-Improvement Protocol

短命令：优化当前工作流、让 Codex 自己寻找可升级的 skill、搜索 GitHub 改进 workflow。

执行顺序：创建 run package -> 扫描本地 capability gap -> 搜索 watchlist/GitHub -> 评估候选 -> 自动应用低风险本地升级 -> 高风险项进入 approval queue -> 执行 skills-doctor/dry-run -> 更新 ledger 和 project_state。

## One-line Dry-run Protocol

验收或启动前可先运行：python -m workflow1 --stage dry-run --goal "启动当前数据的自动科研流程"。

Dry-run 必须只返回计划，不处理真实数据、不重新清洗、不训练模型、不运行 DQN。输出应包含 intent、mode、required skills、planned stages、quality gates、approval_required 和 block_reason。


## Experimental DQN Protocol Note (2026-04-26 18:30:50)

当用户明确授权 self-synthesized experimental DQN 时，可以在不等待 formal 参数确认的情况下运行实验版训练，但必须标记 experimental，并不得覆盖 formal config 或写成正式政策结论。

## Research Quality Protocol

每次 durable 科研任务结束前必须执行科研质量核验与 workflow self-improvement review。dry-run 必须返回 matched intent、selected recipe、skills、required inputs、quality gates、expected outputs、stop conditions 和 approval-required items。

## 2026-04-26 20:51:24 Revised DQN protocol note

修正版 experimental DQN 应默认输出 PNG、chart QA、多模型对比、reward component summary、convergence diagnosis 和 result claim guard；formal DQN 前仍需参数确认。

## 2026-04-26 20:55:03 Revised DQN protocol note

修正版 experimental DQN 应默认输出 PNG、chart QA、多模型对比、reward component summary、convergence diagnosis 和 result claim guard；formal DQN 前仍需参数确认。

## 2026-04-26 20:57:02 Revised DQN protocol note

修正版 experimental DQN 应默认输出 PNG、chart QA、多模型对比、reward component summary、convergence diagnosis 和 result claim guard；formal DQN 前仍需参数确认。


## Output Explanation Protocol Addendum

每次 durable task 必须生成 artifact/table/figure/model/code explanations、artifact-to-evidence map、experimental/formal 状态标记和必要的 DOCX/render QA。


## Output Explanation Protocol Addendum

每次 durable task 必须生成 artifact/table/figure/model/code explanations、artifact-to-evidence map、experimental/formal 状态标记和必要的 DOCX/render QA。


## Output Explanation Protocol Addendum

每次 durable task 必须生成 artifact/table/figure/model/code explanations、artifact-to-evidence map、experimental/formal 状态标记和必要的 DOCX/render QA。


## Output Explanation Protocol Addendum

每次 durable task 必须生成 artifact/table/figure/model/code explanations、artifact-to-evidence map、experimental/formal 状态标记和必要的 DOCX/render QA。


## Output Explanation Protocol Addendum

每次 durable task 必须生成 artifact/table/figure/model/code explanations、artifact-to-evidence map、experimental/formal 状态标记和必要的 DOCX/render QA。


## Local Explanation Addendum

每次 durable task 结束前检查是否存在 only-central-index 问题；如果解释只在总索引中，必须补本地解释和同名 explanation。
