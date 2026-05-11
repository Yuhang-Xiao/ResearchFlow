# START HERE

ResearchFlow OS is the public name of this Codex-assisted scientific workflow framework. The Python package remains `workflow1`; the installer exposes both `workflow1` and `researchflow` commands.

## Install From PowerShell

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/Yuhang-Xiao/workflow1/researchflow/install.ps1 -OutFile install.ps1
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

## Start With A Local Dataset

Put local data under `data/01_raw/`:

```powershell
researchflow --stage intake --raw-dir data/01_raw
researchflow --stage validation --raw-dir data/01_raw
researchflow --stage cleaning-plan --raw-dir data/01_raw
```

Or point the workflow at one local file:

```powershell
$env:WORKFLOW1_DATA_FILE="D:\path\to\local_dataset.xlsx"
researchflow --stage auto-research-product --goal "Research goal goes here."
```

## Product Mode Prompt

```text
启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。
```

ResearchFlow OS should infer the target, task type, validation strategy, metrics, baseline families, explainability plan, figure/table plan, quality gates, and repair steps from the data profile and research goal. The user does not need to choose a model first.

## Public Demo

```powershell
researchflow --stage dry-run --goal "启动自动科研成品模式：数据文件是 examples/synthetic_research_demo.csv，研究目标是演示一个合成回归任务。"
```

`examples/synthetic_research_demo.csv` is synthetic and only for command testing.

## Safety

- Keep `data/01_raw/` immutable.
- Keep framework assets under `framework/`.
- Keep Codex skills under `.agents/skills/`.
- Do not commit real data, generated outputs, rendered papers, model artifacts, local corpora, private notes, or credentials.
- Run `researchflow --stage github-release-cleanup-scan` before public pushes.

## 中文简版

ResearchFlow OS 是一个 Codex 辅助科研工作流框架。公开仓库只保留框架本体和合成示例；真实数据、私有语料、运行产物、模型文件和凭据都留在本地。使用时把数据放入 `data/01_raw/`，或用 `WORKFLOW1_DATA_FILE` 指向本地文件，然后通过 `researchflow` 命令运行 intake、validation、cleaning-plan 或自动科研成品模式。
