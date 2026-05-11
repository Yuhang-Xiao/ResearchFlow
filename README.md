# workflow1

workflow1 是一个 Codex 辅助的科研工作流框架。它把数据投喂、语料投喂、任务理解、模型注册表、质量门、自动修复、报告生成和可复现打包组织成一个可扩展的 Research Operating System。

这个公开仓库只保留框架本体和合成示例。真实数据、真实语料、模型产物、运行输出、API key、Zotero 私有配置和历史项目状态都应保留在本地，并默认被 Git 忽略。

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

检查入口：

```powershell
python -m workflow1 --stage launch
python -m workflow1 --stage intake --raw-dir examples
python -m workflow1 --stage validation --raw-dir examples
```

合成示例 dry-run：

```powershell
python -m workflow1 --stage dry-run --goal "启动自动科研成品模式：数据文件是 examples/synthetic_research_demo.csv，研究目标是演示一个合成回归任务。"
```

## Repository Layout

- `src/workflow1/`: Python package and workflow entry points.
- `model_registry/`: task taxonomy, model families, metric maps, validation maps, explainability maps, and repair strategies.
- `workflow_recipes/`: reusable workflow recipes and quality-gate policies.
- `skills/` and `.agents/skills/`: Codex-facing local skills.
- `data/`: local data workspace; real data is ignored by Git.
- `references/`: local research plans, standards, papers, and notes; private documents are ignored by Git.
- `outputs/`: local run packages and output indexes; generated outputs are ignored by Git.
- `reports/` and `experiments/`: local generated reports and experiment artifacts; ignored by Git.
- `project_state/`: lightweight local memory and next-step files. Review before publishing.
- `examples/`: public synthetic examples only.

## Feeding Data

Use one of these patterns:

```powershell
# Option 1: put a local file under data/01_raw
python -m workflow1 --stage intake --raw-dir data/01_raw

# Option 2: point the workflow at a local file or directory
$env:WORKFLOW1_DATA_FILE="D:\path\to\local_dataset.xlsx"
python -m workflow1 --stage auto-research-product --goal "研究目标是 ..."
```

Rules:

- Keep raw data immutable.
- Do not commit real `.csv`, `.xlsx`, model files, rendered papers, or generated run packages.
- Use `examples/synthetic_research_demo.csv` only for demonstration; it is synthetic and not evidence for any research claim.

## Feeding Literature And Corpus

Use local-only inputs:

- Put research plans, standards, PDF notes, and method documents under `references/`.
- Put large RAG chunks, instruction examples, or training pairs under `research_corpus/`.
- Use Zotero only through the configured MCP/API path, and only after a writeback plan is confirmed.
- Never commit API keys, Zotero library secrets, private PDFs, local notes, or generated literature evidence maps from unpublished work.

For Zotero, copy the example env file and keep the real file local:

```powershell
Copy-Item .codex\zotero_mcp.env.example .codex\zotero_mcp.env
```

## Main Commands

```powershell
python -m workflow1 --stage launch
python -m workflow1 --stage continue
python -m workflow1 --stage intake --raw-dir data/01_raw
python -m workflow1 --stage validation --raw-dir data/01_raw
python -m workflow1 --stage cleaning-plan --raw-dir data/01_raw
python -m workflow1 --stage dry-run --goal "启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。"
```

Product-mode contract:

```text
启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。
```

workflow1 should infer the task type from the data profile and research goal, then route through registry selection, baselines, metrics, validation strategy, explainability, figure/table planning, literature evidence, quality gates, auto-repair, and reproducibility packaging. Heavy external dependencies, API keys, Zotero writes, and unknown third-party code require explicit authorization.

## GitHub Release Cleanup

Before pushing a public branch, run the built-in cleanup workflow. The backup directory must be outside this repository.

```powershell
python -m workflow1 --stage github-release-cleanup-scan

$backup = "D:\桌面\workflow1_private_backup_$(Get-Date -Format yyyyMMdd_HHmmss)"
python -m workflow1 --stage github-release-cleanup --backup-to $backup --apply --keep-synthetic-example
```

The cleanup stage:

- backs up every selected file to the desktop backup folder;
- verifies SHA256 before deleting repository files;
- stores cleanup manifests only in the external backup folder;
- resets local state/output directories to public template placeholders;
- removes real data, generated outputs, local corpora, model artifacts, caches, private config, and historical one-off task scripts.

Post-cleanup checks:

```powershell
git status --short
git ls-files
python -m workflow1 --stage launch
python -m workflow1 --stage intake --raw-dir examples
python -m workflow1 --stage validation --raw-dir examples
python -m workflow1 --stage dry-run --goal "启动自动科研成品模式：数据文件是 examples/synthetic_research_demo.csv，研究目标是演示一个合成回归任务。"
```

Push on a release branch:

```powershell
git switch -c codex/github-release-cleanup
git add -A
git commit -m "Prepare workflow1 for public GitHub release"
git push -u origin codex/github-release-cleanup
```

Do not force-push or merge automatically. Review the GitHub file browser before making the repository public.

## Security Commitments

- Real datasets are local-only.
- Generated outputs are local-only.
- API keys and tokens are never stored in repository files.
- Zotero writeback uses MCP/API only; never edit Zotero SQLite directly.
- Large dependencies, external plugins, long-running services, paid access, and unknown third-party code require explicit authorization.
- Public examples are synthetic and clearly labeled.
