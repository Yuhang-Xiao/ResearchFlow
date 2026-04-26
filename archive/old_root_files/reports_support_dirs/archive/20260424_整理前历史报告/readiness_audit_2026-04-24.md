# 迁移后仓库就绪性审计报告

审计日期：2026-04-24  
审计范围：仓库控制层、技能层、源码/管线层、项目状态层、环境与可移植性风险、端到端科研工作流完整性。  
审计边界：未启动任何数据清洗、数据分析、建模、调参或可视化任务；仅做文件、配置、源码、依赖和状态一致性检查。

## 总体结论

当前仓库不建议直接启动新的端到端自动科研运行。仓库已经具备清晰的科研工作流规则、目录结构和一组说明型技能，但实际可执行管线仍主要是占位实现，项目状态仍绑定上一轮四川食品分类任务，且缺少 Python 项目清单和依赖锁定文件。

综合评级：PARTIALLY READY

## 1. 仓库指令与控制层

### AGENTS.md

状态：READY

- `AGENTS.md` 存在且可读。
- 项目目的明确：通用科学工作流脚手架，不预设领域、数据集、模型类型或报告格式。
- 默认流程覆盖 intake、schema profiling、cleaning/matching、validation、EDA、ML framing、method selection、baseline modeling、evaluation、visualization、reporting 和 workflow update。
- 数据分层规则清晰，明确 `data/01_raw` 不可原地修改。
- 语言策略与当前仓库中文优先需求一致。
- 目标驱动自动执行策略与当前预期一致：当原始数据和研究目标明确时允许自动推进清洗、EDA、建模、比较和更新。

### .codex/config.toml

状态：PARTIALLY READY

- `.codex/config.toml` 存在且可读。
- `preserve_raw_data = true` 与仓库规则一致。
- `analyze_data_by_default = false` 与自动执行策略不必然冲突，但需要解释为：没有明确研究目标时不默认分析；有明确原始数据和研究目标时按 `AGENTS.md` 自动执行。
- 配置仍是 starter 级别，没有声明运行环境、依赖、入口命令或技能/管线能力矩阵。

## 2. 技能层

状态：PARTIALLY READY

已发现技能：

- `autonomous-research-orchestrator`
- `baseline-trainer`
- `data-cleaning-matching`
- `data-schema-profiler`
- `eda-generator`
- `method-selector`
- `ml-problem-framer`
- `task-router`
- `workflow-updater`

结论：

- 所有已发现技能均包含 `SKILL.md`，且具备清楚的标题、使用时机或目的、输入、输出和推荐流程。
- 技能组合覆盖自动研究编排、schema profiling、数据清洗匹配、EDA、问题定义、方法选择、基线训练和工作流更新。
- 但 `SKILL.md` 未采用统一机器可读 metadata，例如显式 `name`、`description`、`version`、`inputs`、`outputs` 字段。
- 仍缺少独立技能：label engineering、data validation、tuning/comparison、visualization/reporter。

## 3. 源码与管线层

状态：NOT READY

检查结果：

- `python -m compileall -q src` 通过，未发现 Python 语法级阻断。
- 当前目录下直接 `import workflow1` 不可用，因为仓库使用 `src` 布局但没有安装配置或 `PYTHONPATH` 说明。
- `src/workflow1/orchestration.py` 仅提供轻量计划对象和阻断条件，不是可执行端到端 runner。
- `src/workflow1/pipelines/*` 多数子模块的 `run()` 返回 `status="not_implemented"`，实际是占位实现。
- `src/workflow1/pipelines/cleaning/category_reconstruction.py` 是上一轮四川食品分类任务的强数据集专用脚本，路径和字段名都绑定 `FINAL_SiChuan_2023_ALL_DATA`，不适合作为通用清洗模块。

会阻断实际使用的缺口：

- 没有通用数据 intake/profiling 执行入口。
- 没有通用原始数据验证器。
- 没有通用清洗规则引擎或清洗日志结构。
- 没有通用特征工程和 label engineering 模块。
- 没有通用 train/evaluate/split/metric 管线。
- 没有调参、模型比较和实验登记模块。
- 没有通用可视化导出管线。
- 没有统一 CLI 或 orchestrator runner 可从一个研究目标自动串联全流程。

## 4. 项目状态层

状态：PARTIALLY READY

存在且可读：

- `project_state/current_focus.md`
- `project_state/next_step.md`
- `project_state/changelog.md`
- `project_state/decision_log.md`
- `project_state/roadmap.yaml`

主要问题：

- `current_focus.md` 与原 `next_step.md` 仍指向上一轮 `FINAL_SiChuan_2023_ALL_DATA.xlsx` 产品分类任务。
- `decision_log.md` 已记录从 gated semi-autonomous 到 goal-driven autonomous execution 的策略变更，方向正确。
- `roadmap.yaml` 仍显示 `status: bootstrap` 和 `bootstrap/in_progress`，未反映迁移后审计与修复准备。
- 状态文件和历史报告中存在明显乱码字段名，例如 `鍘熷...`、`浜у...`、`鏄...`，说明历史产物或编码链路存在迁移风险。

## 5. 环境与可移植性风险

状态：PARTIALLY READY

当前机器可用项：

- Python 可用，版本为 `Python 3.13.9`。
- 当前环境中可找到 `pandas`、`numpy`、`sklearn`、`matplotlib`、`seaborn`、`openpyxl`、`yaml`。
- `python -m compileall -q src` 通过。

主要风险：

- 仓库根目录没有 `pyproject.toml`、`requirements.txt`、`environment.yml`、`setup.py` 或锁文件，无法保证换机后复现依赖。
- `src` 布局没有项目安装配置，当前目录直接导入 `workflow1` 失败。
- `rg --files` 在当前机器执行失败，错误为 Access is denied；不阻断 Python 工作流，但会影响日常快速审计和检索效率。
- 存在历史任务文件和归档引用：`FINAL_SiChuan_2023_ALL_DATA`、`MERGED_2023...`、`data/99_archive`、`reports/archive`。
- `data/01_raw` 仍包含 `FINAL_SiChuan_2023_ALL_DATA.xlsx`，并且 `data/99_archive` 也有同名文件，可能造成新运行数据选择歧义。
- 仓库根目录存在历史总结 Word 文件 `食品安全风险监测与优化_Codex科研工作流总结.docx`，说明当前仓库并非完全空白通用 scaffold。
- 多个历史报告和状态文件中有乱码文本，若后续自动读取这些文件作为上下文，可能污染字段判断、报告语言和人工复核说明。

## 6. 工作流完整性评级

| 区域 | 就绪度 | 理由 |
|---|---|---|
| 自动数据清洗 | PARTIALLY READY | 有规则、目录、技能说明和一个历史专用脚本，但缺少通用清洗引擎、验证报告结构和可复用清洗日志。 |
| 自动建模 | NOT READY | 有 ML framing、method selection、baseline trainer 技能说明，但源码没有 train/split/evaluate/metric/experiment tracking 实现。 |
| 自动可视化 | NOT READY | 有 `reports/figures` 目录和 EDA 技能说明，但没有可视化管线、中文字体策略、图表模板或导出验证。 |
| 迭代科学工作流执行 | PARTIALLY READY | 控制层和状态层机制存在，但状态仍绑定历史任务，orchestration 只是计划对象，没有端到端 runner。 |

## 7. 优先级缺口与修复计划

### Critical blockers

1. 添加项目环境清单：创建 `pyproject.toml` 或 `requirements.txt`，声明 Python 版本范围和核心依赖。
2. 让 `src` 布局可安装或可运行：提供 editable install 配置、CLI 入口或明确 `PYTHONPATH` 使用方式。
3. 将项目状态从历史四川分类任务切换回“迁移后通用科研工作流准备”状态，避免下一次自动运行误接旧任务。
4. 把历史任务专用脚本与通用管线隔离：保留为 archived/example 或 task-specific module，不作为默认 cleaning pipeline。
5. 实现最小可用通用 pipeline：intake/schema profiling、raw validation、cleaning plan/output log、EDA summary、model input builder、baseline train/evaluate、visualization export。

### Recommended improvements

1. 为每个 `SKILL.md` 增加机器可读 metadata，包括 `name`、`description`、`stage`、`inputs`、`outputs`、`blocks_on`。
2. 新增技能：`label-engineering`、`data-validation`、`tuning-comparison`、`visualization-reporter`。
3. 新增端到端 orchestrator runner，输入 raw path + research goal，输出阶段计划、执行记录和状态更新。
4. 建立报告规范，统一 schema inventory、validation report、EDA report、model report、visualization summary。
5. 修复或隔离乱码历史产物，至少不要让当前状态文件继续引用乱码字段作为下一步。
6. 增加轻量测试，例如 import test、pipeline placeholder test、path convention test、state file schema test。

### Nice-to-have upgrades

1. 增加 `Makefile`、`justfile` 或 PowerShell 脚本，统一 `audit`、`test`、`profile-schema`、`run-workflow` 命令。
2. 增加示例小数据集或 synthetic fixture，用于验证管线但不污染真实 `data/01_raw`。
3. 增加实验登记格式，例如 `experiments/runs/{run_id}/metrics.json`。
4. 增加可视化主题和中文字体预检。
5. 增加迁移检查脚本，自动检查依赖、路径、状态文件和数据目录歧义。

## 8. 本次审计产物

- 中文审计报告：`reports/readiness_audit_2026-04-24.md`
- 机器可读清单：`project_state/readiness_checklist_2026-04-24.yaml`
- 已更新：`project_state/next_step.md`
- 已更新：`project_state/changelog.md`

## 最终判断

仓库已具备科研工作流脚手架的方向和规则，但还没有达到在新电脑上直接开始端到端自动清洗、建模、调参、可视化的工程就绪状态。建议第一修复步是：补齐项目依赖/安装清单，并建立最小可运行的通用 pipeline runner；同时把项目状态从上一轮历史任务切换为迁移后待修复状态。
