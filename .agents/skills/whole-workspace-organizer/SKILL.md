---
name: whole-workspace-organizer
description: Scan, clean, deduplicate, classify, and index the entire workflow1 workspace while preserving raw data and canonical pipeline files.
---

# Whole Workspace Organizer

## 何时触发

每次实质性任务结束后、用户要求整理目录时、发现散落文件或重复文件时触发。

## 扫描范围

扫描 root、`.agents/`、`.codex/`、`skills/`、`src/`、`prompts/`、`references/`、`data/`、`reports/`、`experiments/`、`outputs/`、`archive/` 和 `project_state/`。

## 去重

对可处理文件计算 SHA256。允许删除 hash 完全一致的重复副本、`__pycache__/`、`.pytest_cache/`、`.ipynb_checkpoints/`、Excel 临时锁文件、空临时文件和明确无价值测试残留。禁止删除原始数据、唯一研究文档、唯一报告、唯一代码、唯一配置、唯一数据结果和项目状态文件。

## 根目录清理

根目录只保留核心入口文件和一级功能目录。散落报告、数据、参考资料、脚本必须归入任务工作包、标准目录、`references/` 或 `outputs/_待复核/`。

## 标准目录

- `data/01_raw/` 永远不修改、不删除、不重命名、不移动。
- `data/03_primary/` 只保留 canonical 清洗主表。
- `data/04_feature/` 只保留 pipeline 必需 canonical 特征。
- `reports/` 只保留项目级索引与摘要。
- `experiments/` 只保留项目级实验入口和 canonical 实验索引。

## 待复核

唯一但无法自动判断归属的文件进入 `outputs/_待复核/YYYYMMDD_未归类唯一文件/`，并写入待复核日志。

## 索引和验证

整理后更新 `run_index.md`、`run_manifest.csv`、`latest_canonical_outputs.yaml`、`project_state/artifact_index.md` 和 `project_state/workspace_structure.md`，并运行 `import workflow1` 与 `python -m workflow1 --stage launch` 轻量验证。

长期规则：以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；任务结束后更新 run index。

## Document-Governed DQN Cleanup Rule

During cleanup after DQN/POMDP/belief-MDP/RL work, preserve every run-package readiness artifact, literature audit, environment audit, parameter confirmation table, and model-spec extraction file. Do not delete Zotero notes, PDFs, research-plan documents, raw data, or sandbox outputs; if a DQN output is a prototype, keep it labeled as prototype and do not promote it to formal canonical status without user confirmation.

The cleanup check must confirm that future DQN tasks will start with:

1. `document-governed-modeling`
2. `zotero-literature-auditor`
3. `environment-auditor`
4. `dqn-readiness-auditor`
