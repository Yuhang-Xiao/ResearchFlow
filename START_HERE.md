# START HERE

workflow1 is a Codex-assisted scientific workflow scaffold. The public checkout is a framework template: it contains code, registries, recipes, skills, and synthetic examples, but no real user data or historical research outputs.

## Start With A Local Dataset

Place local data under `data/01_raw/` or set `WORKFLOW1_DATA_FILE` to a local path:

```powershell
python -m workflow1 --stage intake --raw-dir data/01_raw
python -m workflow1 --stage validation --raw-dir data/01_raw
python -m workflow1 --stage cleaning-plan --raw-dir data/01_raw
```

For a one-line research product dry-run:

```powershell
python -m workflow1 --stage dry-run --goal "启动自动科研成品模式：数据文件是 examples/synthetic_research_demo.csv，研究目标是演示一个合成回归任务。"
```

## Product Mode Prompt

```text
启动自动科研成品模式：数据文件是 XXX，研究目标是 XXX。
```

workflow1 should infer the target, task type, validation strategy, metrics, baseline families, explainability plan, figure/table plan, quality gates, and repair steps from the data profile and research goal. The user does not need to choose a model first.

## Safety

- Do not commit real data, generated outputs, model artifacts, local corpora, API keys, or Zotero private config.
- Keep raw data immutable.
- Use `github-release-cleanup-scan` before public pushes.
- Use `github-release-cleanup --apply --backup-to <outside-repo-folder>` only when an external backup location is available.

## Public Demo

`examples/synthetic_research_demo.csv` is a tiny synthetic dataset for command testing only. It is not real research evidence.
