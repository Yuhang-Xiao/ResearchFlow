# ResearchFlow OS

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![PowerShell install](https://img.shields.io/badge/install-PowerShell-5391FE.svg)](#quick-install)
[![Public branch](https://img.shields.io/badge/branch-researchflow-2EA44F.svg)](#)
[![Data policy](https://img.shields.io/badge/data-local--only-brightgreen.svg)](#security-commitments)

**ResearchFlow OS** is a Codex-assisted scientific workflow framework. It gives you a reusable local research workspace for data intake, schema profiling, validation, cleaning plans, model and method routing, quality gates, explainability planning, reporting, and reproducibility packaging.

The public project name is **ResearchFlow OS**. The Python package and original command remain `workflow1`, and the installer also adds a friendlier `researchflow` command.

This repository is framework-only. Real data, private literature, generated reports, model artifacts, local corpora, private Zotero settings, and credentials stay on your machine.

---

## English

### Quick Install

Recommended install path for Windows PowerShell:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Yuhang-Xiao/workflow1/researchflow/install.ps1 -OutFile install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

After installation, open a new PowerShell window if PATH has not refreshed, then run:

```powershell
researchflow --stage launch
workflow1 --stage intake --raw-dir examples
```

Install to a custom folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -InstallDir D:\ResearchFlowOS
```

Developer install from an existing checkout:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

### Quick Start

Run the synthetic demo checks:

```powershell
researchflow --stage launch
researchflow --stage intake --raw-dir examples
researchflow --stage validation --raw-dir examples
researchflow --stage dry-run --goal "启动自动科研成品模式：数据文件是 examples/synthetic_research_demo.csv，研究目标是演示一个合成回归任务。"
```

The demo file is `examples/synthetic_research_demo.csv`. It is synthetic and only proves that the workflow can route commands.

### What ResearchFlow OS Does

- **Data-first workflow**: inspect files, schemas, missingness, and validation signals before downstream modeling.
- **Goal-driven routing**: infer task type, likely target structure, baselines, metrics, validation strategy, and explainability needs from a dataset and research goal.
- **Research quality gates**: keep model comparison, metric completeness, evidence mapping, figure/table QA, and reproducibility visible.
- **Local privacy boundary**: keep real inputs and generated outputs outside Git by default.
- **Extensible framework assets**: maintain registries, recipes, quality policies, templates, and Codex skills without tying the workflow to one research domain.

### Repository Map

```text
src/workflow1/                    Python package, CLI, orchestration, pipelines
framework/model_registry/         Task, metric, validation, model, and explanation maps
framework/workflow_recipes/       Reusable workflow recipes and safety policies
framework/research_quality/       Publication and reproducibility quality policies
framework/workflow_improvement/   Safe workflow self-improvement policies
framework/templates/              Product-mode report and package templates
framework/prompts/                Launch prompts and prompt snippets
.agents/skills/                   Codex-facing local workflow skills
examples/                         Public synthetic examples only
data/                             Local data workspace; real files are ignored
references/                       Local plans, papers, standards, and notes
outputs/                          Local run packages and indexes
reports/                          Local generated reports, figures, and tables
experiments/                      Local experiment artifacts
tools/                            Manual helper scripts
```

### Feed Data

Option 1: put local raw data under `data/01_raw/`.

```powershell
researchflow --stage intake --raw-dir data/01_raw
researchflow --stage validation --raw-dir data/01_raw
researchflow --stage cleaning-plan --raw-dir data/01_raw
```

Option 2: point the workflow at one local file.

```powershell
$env:WORKFLOW1_DATA_FILE="D:\path\to\local_dataset.xlsx"
researchflow --stage auto-research-product --goal "Research goal goes here."
```

Rules:

- Treat `data/01_raw/` as immutable.
- Do not commit real `.csv`, `.xlsx`, `.jsonl`, model files, rendered papers, or run packages.
- Use `examples/synthetic_research_demo.csv` for testing only.

### Feed Literature And Corpus

- Put project plans, standards, papers, and reading notes under `references/`.
- Put large local corpora, RAG chunks, or training examples under `research_corpus/`.
- Use Zotero only through an authorized MCP/API path.
- Keep private PDFs, unpublished notes, generated evidence maps, and credentials out of Git.

### Product Mode

Use this one-line contract:

```text
启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。
```

When the goal and data profile are sufficient, ResearchFlow OS should infer the task type, choose baselines and metrics, plan validation and explainability, prepare figure/table expectations, run quality gates, and package reproducible outputs. External services, paid access, database writeback, large dependencies, and unknown third-party code require explicit approval.

### Release Cleanup

Before publishing a public branch:

```powershell
researchflow --stage github-release-cleanup-scan

$backup = "D:\Desktop\workflow1_private_backup_$(Get-Date -Format yyyyMMdd_HHmmss)"
researchflow --stage github-release-cleanup --backup-to $backup --apply --keep-synthetic-example
```

The cleanup stage backs up selected files outside the repository, verifies SHA256 before deletion, and removes local data, outputs, corpora, caches, model artifacts, private config, and one-off historical scripts.

### Security Commitments

- Real datasets are local-only.
- Generated outputs are local-only.
- Credentials and private configuration are not tracked.
- Zotero writeback uses authorized MCP/API access only.
- Public examples are synthetic and clearly labeled.

---

## 中文

### 快速安装

Windows PowerShell 推荐安装方式：

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Yuhang-Xiao/workflow1/researchflow/install.ps1 -OutFile install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

安装完成后，如果 PATH 还没有刷新，重新打开一个 PowerShell 窗口，然后运行：

```powershell
researchflow --stage launch
workflow1 --stage intake --raw-dir examples
```

安装到指定目录：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -InstallDir D:\ResearchFlowOS
```

开发者从已有代码目录安装：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

### 快速开始

运行合成数据检查：

```powershell
researchflow --stage launch
researchflow --stage intake --raw-dir examples
researchflow --stage validation --raw-dir examples
researchflow --stage dry-run --goal "启动自动科研成品模式：数据文件是 examples/synthetic_research_demo.csv，研究目标是演示一个合成回归任务。"
```

`examples/synthetic_research_demo.csv` 是合成数据，只用于验证命令和路由，不是研究证据。

### 它能做什么

ResearchFlow OS 是一个 Codex 辅助科研工作流框架，用来把“本地数据文件 + 研究目标”组织成可审计、可复现的科研流程。

- **先理解数据**：先做文件、字段、缺失、异常和验证信号检查，再进入后续建模。
- **按目标路由方法**：根据数据和研究目标推断任务类型、目标结构、基线、指标、验证策略和解释性需求。
- **质量门禁可见**：保留模型比较、指标完整性、证据映射、图表 QA 和可复现检查。
- **隐私边界清楚**：真实数据和运行产物默认只留在本地，不进入 Git。
- **框架可扩展**：通过 registry、recipe、quality policy、template 和 Codex skill 扩展到不同科研任务。

### 目录结构

```text
src/workflow1/                    Python 包、CLI、编排和流水线
framework/model_registry/         任务、指标、验证、模型、解释性映射
framework/workflow_recipes/       可复用工作流配方和安全策略
framework/research_quality/       论文级质量和可复现策略
framework/workflow_improvement/   安全自我升级策略
framework/templates/              成品模式报告和工作包模板
framework/prompts/                启动提示和 prompt 片段
.agents/skills/                   Codex 本地技能入口
examples/                         公开合成示例
data/                             本地数据工作区，真实文件不提交
references/                       本地研究计划、论文、标准和笔记
outputs/                          本地任务工作包和索引
reports/                          本地报告、图表和表格
experiments/                      本地实验产物
tools/                            手动辅助脚本
```

### 数据投喂

方式一：把本地原始数据放到 `data/01_raw/`。

```powershell
researchflow --stage intake --raw-dir data/01_raw
researchflow --stage validation --raw-dir data/01_raw
researchflow --stage cleaning-plan --raw-dir data/01_raw
```

方式二：用环境变量指向某个本地数据文件。

```powershell
$env:WORKFLOW1_DATA_FILE="D:\path\to\local_dataset.xlsx"
researchflow --stage auto-research-product --goal "这里写研究目标。"
```

规则：

- `data/01_raw/` 是不可变原始数据层。
- 不提交真实 `.csv`、`.xlsx`、`.jsonl`、模型文件、渲染论文或任务工作包。
- `examples/synthetic_research_demo.csv` 只用于测试。

### 文献和语料投喂

- 研究计划、标准、论文和阅读笔记放入 `references/`。
- 大型本地语料、RAG 切片、训练样本放入 `research_corpus/`。
- Zotero 只通过授权 MCP/API 路径使用。
- 私有 PDF、未发表笔记、证据图谱和凭据不进入 Git。

### 自动科研成品模式

一行启动格式：

```text
启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。
```

当数据和目标足够清楚时，ResearchFlow OS 应自动推断任务类型，选择基线与指标，规划验证和解释性分析，准备图表/表格预期，运行质量门禁，并打包可复现输出。外部服务、付费访问、数据库写回、大型依赖和未知第三方代码都需要明确授权。

### 发布前清理

公开推送前先扫描：

```powershell
researchflow --stage github-release-cleanup-scan
```

再把备份目录放在仓库外执行清理：

```powershell
$backup = "D:\Desktop\workflow1_private_backup_$(Get-Date -Format yyyyMMdd_HHmmss)"
researchflow --stage github-release-cleanup --backup-to $backup --apply --keep-synthetic-example
```

清理阶段会先备份、校验 SHA256，再删除本地数据、输出、语料、缓存、模型产物、私有配置和历史一次性脚本。

### 安全承诺

- 真实数据只留在本地。
- 运行产物只留在本地。
- 凭据和私有配置不进入 Git。
- Zotero 写回只走授权 MCP/API。
- 公开示例均为合成数据并明确标注。
