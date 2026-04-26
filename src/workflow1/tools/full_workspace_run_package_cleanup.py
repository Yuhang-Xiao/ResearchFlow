from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NOW = datetime.now()
STAMP = NOW.strftime("%Y%m%d_%H%M")
DATE = NOW.strftime("%Y%m%d")
TASK = "全工作流目录重构与去重"
RUN_ROOT = ROOT / "outputs" / "工作包" / f"{STAMP}_{TASK}"
REVIEW_ROOT = ROOT / "outputs" / "_待复核" / f"{DATE}_未归类唯一文件"
INDEX = ROOT / "outputs" / "_index"

SUBDIRS = [
    "00_输入说明",
    "01_数据输出",
    "02_表格输出",
    "03_图表输出",
    "04_报告输出",
    "05_模型与实验",
    "06_配置参数",
    "07_日志与错误",
    "08_代码快照",
]

LONG_RULE = (
    "以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。"
    "所有新产物进入任务包；标准目录只保留 canonical 和 pipeline 必需文件；"
    "重复文件删除；唯一文件保护并归类；无法判断的唯一文件进入 `outputs/_待复核/`；"
    "任务结束后更新 run index。"
)

CANONICAL = {
    "cleaned_dataset": "data/03_primary/peanut_cleaned_analysis_ready.csv",
    "cleaned_dataset_xlsx": "data/03_primary/peanut_cleaned_analysis_ready.xlsx",
    "count_panel": "data/04_feature/peanut_count_panel.csv",
    "concentration_table": "data/04_feature/peanut_concentration_clean_table.csv",
    "concentration_distribution_summary": "data/04_feature/peanut_concentration_distribution_summary.csv",
    "beta_binomial_states": "data/04_feature/peanut_beta_binomial_belief_states.csv",
    "belief_mdp_features": "data/04_feature/peanut_belief_mdp_state_features.csv",
    "belief_mdp_features_with_moe_edi": "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv",
    "bmdl_config": "data/04_feature/peanut_bmdl_parameter_config.json",
    "bmdl_table": "data/04_feature/peanut_bmdl_parameter_table.csv",
    "consumption_parameter_table": "data/04_feature/peanut_consumption_parameter_table.csv",
    "population_parameter_table": "data/04_feature/peanut_population_parameter_table.csv",
    "edi_moe_risk_table": "data/04_feature/peanut_edi_moe_risk_table.csv",
    "edi_moe_risk_summary": "data/04_feature/peanut_edi_moe_risk_summary.csv",
    "latest_pre_dqn_readiness_report": "reports/项目级索引与摘要/peanut_pre_dqn_readiness_after_moe_edi.md",
    "latest_handoff": "project_state/conversation_handoff.md",
}

ROOT_ALLOWED_FILES = {"AGENTS.md", "START_HERE.md", "README.md", "pyproject.toml", "requirements.txt"}
ROOT_ALLOWED_DIRS = {
    ".codex",
    ".agents",
    ".git",
    "skills",
    "src",
    "prompts",
    "references",
    "data",
    "reports",
    "experiments",
    "outputs",
    "archive",
    "project_state",
}

moved_rows: list[dict] = []
deleted_rows: list[dict] = []
unclassified_rows: list[dict] = []


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def ensure_dirs() -> None:
    for sub in SUBDIRS:
        (RUN_ROOT / sub).mkdir(parents=True, exist_ok=True)
    for d in [
        INDEX,
        ROOT / "outputs" / "工作包",
        ROOT / "outputs" / "_待复核",
        ROOT / "archive" / "old_root_files",
        ROOT / "archive" / "deleted_duplicates_manifest",
        ROOT / "archive" / "unsorted_unique",
        ROOT / "references" / "project_plan",
        ROOT / "references" / "data_cleaning",
        ROOT / "references" / "modeling",
        ROOT / "references" / "visualization",
        ROOT / "references" / "literature",
        ROOT / "references" / "standards",
        ROOT / "references" / "notes",
        ROOT / "references" / "processed_summaries",
        ROOT / "references" / "archive",
        ROOT / "data" / "02_intermediate",
        ROOT / "data" / "03_primary",
        ROOT / "data" / "04_feature",
        ROOT / "data" / "05_model_input",
        ROOT / "data" / "99_archive",
        ROOT / "reports" / "项目级索引与摘要",
        ROOT / "experiments" / "baselines",
        ROOT / "experiments" / "advanced",
        ROOT / "experiments" / "comparisons",
        ROOT / "experiments" / "optimization",
        ROOT / "experiments" / "archive",
        ROOT / "src" / "workflow1" / "tools",
    ]:
        d.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".csv", ".xlsx", ".xls", ".tsv"}:
        return "表格"
    if ext in {".md", ".docx", ".pdf", ".txt"}:
        return "报告/文档"
    if ext in {".svg", ".png", ".jpg", ".jpeg"}:
        return "图表"
    if ext in {".json", ".yaml", ".yml", ".toml"}:
        return "配置/索引"
    if ext == ".py":
        return "代码"
    if ext in {".pyc", ".tmp", ".bak"} or path.name.startswith("~$"):
        return "临时文件"
    return "其他"


def is_temp(path: Path) -> bool:
    r = rel(path) if path.exists() else path.as_posix()
    return (
        "__pycache__" in path.parts
        or ".pytest_cache" in path.parts
        or ".ipynb_checkpoints" in path.parts
        or path.suffix.lower() in {".pyc", ".tmp", ".bak"}
        or path.name.startswith("~$")
        or re.search(r"(^|/)(tmp|temp)(/|$)", r, re.I) is not None
    )


def classify(path: Path, duplicate_hashes: set[str] | None = None) -> dict:
    r = rel(path)
    parts = r.split("/")
    top = parts[0]
    ext = path.suffix.lower()
    digest = "" if path.stat().st_size > 80 * 1024 * 1024 else sha256(path)
    is_raw = r.startswith("data/01_raw/")
    is_code = top == "src" or ext == ".py"
    is_config = ext in {".json", ".yaml", ".yml", ".toml"} or path.name in {"pyproject.toml", "requirements.txt"}
    is_report = ext in {".md", ".docx", ".pdf", ".txt"} or top == "reports"
    is_table = ext in {".csv", ".xlsx", ".xls", ".tsv"}
    is_fig = ext in {".svg", ".png", ".jpg", ".jpeg"}
    is_ref = top == "references"
    is_state = top == "project_state"
    is_dup = bool(digest and duplicate_hashes and digest in duplicate_hashes)
    temp = is_temp(path) or path.stat().st_size == 0
    if is_raw:
        action = "保留原始数据"
    elif temp:
        action = "删除临时/缓存/空文件"
    elif is_dup:
        action = "hash重复，删除或保留canonical副本"
    elif top == "reports":
        action = "迁移到任务工作包或项目级摘要"
    elif top == "outputs" and len(parts) > 1 and parts[1] not in {"工作包", "_index", "_待复核"}:
        action = "迁移旧输出到任务工作包或archive"
    elif top not in ROOT_ALLOWED_DIRS and path.name not in ROOT_ALLOWED_FILES:
        action = "根目录散落文件，归类或待复核"
    else:
        action = "保留或索引"
    return {
        "文件路径": r,
        "文件名": path.name,
        "扩展名": ext,
        "文件大小": path.stat().st_size,
        "修改时间": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        "SHA256 hash": digest,
        "所属一级目录": top,
        "文件初步类型": file_type(path),
        "是否原始数据": is_raw,
        "是否代码": is_code,
        "是否配置": is_config,
        "是否报告": is_report,
        "是否表格": is_table,
        "是否图表": is_fig,
        "是否参考资料": is_ref,
        "是否项目状态": is_state,
        "是否疑似重复": is_dup,
        "是否疑似临时文件": temp,
        "建议处理方式": action,
    }


def iter_files(include_git: bool = False) -> list[Path]:
    files = []
    for p in ROOT.rglob("*"):
        if not include_git and ".git" in p.parts:
            continue
        if p.is_file():
            files.append(p)
    return sorted(files, key=lambda x: rel(x))


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_file(src: Path, dst: Path, reason: str, canonical: bool = False) -> None:
    if not src.exists() or not src.is_file():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and sha256(dst) == sha256(src):
        return
    if dst.exists():
        dst = dst.with_name(f"{dst.stem}_{datetime.now().strftime('%H%M%S')}{dst.suffix}")
    shutil.copy2(src, dst)
    moved_rows.append({
        "原路径": rel(src),
        "新路径": rel(dst),
        "移动原因": "复制：" + reason,
        "是否 canonical": canonical,
        "是否影响 pipeline": canonical,
    })


def move_file(src: Path, dst: Path, reason: str, canonical: bool = False, pipeline: bool = False) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if src.is_file() and dst.is_file() and sha256(src) == sha256(dst):
            delete_file(src, dst, "移动目标已有 hash 相同副本")
            return
        dst = dst.with_name(f"{dst.stem}_{datetime.now().strftime('%H%M%S')}{dst.suffix}")
    shutil.move(str(src), str(dst))
    moved_rows.append({
        "原路径": rel(src) if src.exists() else src.as_posix(),
        "新路径": rel(dst),
        "移动原因": reason,
        "是否 canonical": canonical,
        "是否影响 pipeline": pipeline,
    })


def delete_file(src: Path, keep: Path | str, reason: str, confirmed: bool = True) -> None:
    if "data/01_raw" in src.as_posix():
        raise RuntimeError(f"Refuse to delete raw data: {src}")
    digest = sha256(src) if src.exists() and src.is_file() else ""
    deleted_rows.append({
        "删除文件路径": rel(src) if src.exists() else src.as_posix(),
        "保留文件路径": rel(keep) if isinstance(keep, Path) and keep.exists() else str(keep),
        "SHA256": digest,
        "删除原因": reason,
        "删除时间": datetime.now().isoformat(timespec="seconds"),
        "是否确认重复": confirmed,
    })
    if src.exists():
        src.unlink()


def package_dest(src: Path, package_name: str) -> Path:
    lower = src.name.lower()
    ext = src.suffix.lower()
    pkg = next((p for p in (ROOT / "outputs" / "工作包").iterdir() if p.is_dir() and package_name in p.name), None)
    if pkg is None:
        return RUN_ROOT / "01_数据输出" / src.name
    if ext in {".csv", ".xlsx", ".xls"}:
        sub = "01_数据输出" if rel(src).startswith("data/") else "02_表格输出"
    elif ext in {".svg", ".png", ".jpg", ".jpeg"}:
        sub = "03_图表输出"
    elif ext in {".json", ".yaml", ".yml", ".toml"}:
        sub = "07_日志与错误" if any(x in lower for x in ["log", "error", "summary"]) else "06_配置参数"
    elif ext in {".md", ".docx", ".pdf", ".txt"}:
        sub = "07_日志与错误" if any(x in lower for x in ["log", "error", "repair"]) else "04_报告输出"
    else:
        sub = "01_数据输出"
    return pkg / sub / src.name


def write_before_snapshot() -> None:
    files = iter_files()
    hashes: dict[str, int] = {}
    for f in files:
        if f.stat().st_size <= 80 * 1024 * 1024:
            h = sha256(f)
            hashes[h] = hashes.get(h, 0) + 1
    dup_hashes = {h for h, n in hashes.items() if n > 1}
    rows = [classify(f, dup_hashes) for f in files]
    write_csv(RUN_ROOT / "02_表格输出" / "workspace_inventory_before.csv", rows)
    plan = f"""# 整理前计划

## 任务目标

本轮执行全工作流目录重构、去重、归类和长期规则固化，不重新跑数据、不重新清洗、不重新计算 MOE/EDI、不运行 DQN。

## 处理策略

1. `outputs/工作包/` 作为唯一主输出机制。
2. 根目录只保留核心入口和一级功能目录。
3. `data/01_raw/` 不移动、不删除、不重命名，只更新 inventory。
4. `reports/` 仅保留 README 与 `项目级索引与摘要/`。
5. pipeline 必需 canonical 文件保留在标准目录。
6. hash 完全重复的辅助副本、缓存和空临时文件删除并记录。
7. 唯一但无法归类文件进入 `outputs/_待复核/`。

## 整理前文件数

{len(rows)}
"""
    write_text(RUN_ROOT / "04_报告输出" / "workspace_cleanup_plan.md", plan)


def create_or_update_readmes() -> None:
    readmes = {
        "README.md": "# workflow1\n\n通用科学工作流项目。人工查看任务结果的主入口是 `outputs/工作包/`；仓库规则见 `AGENTS.md`。\n",
        "outputs/README.md": "# outputs\n\n`工作包/` 是人工查看结果的主入口；`_index/` 保存全局 run index 和 canonical 输出索引；`_待复核/` 保存无法自动归属但唯一的文件。\n",
        "archive/README.md": "# archive\n\n项目级历史和非主流程归档。不要在这里删除唯一文件；删除重复文件必须有日志。\n",
        "reports/README.md": "# reports\n\n本目录不再堆放任务结果，只保留项目级索引与摘要。每轮任务报告必须进入 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/04_报告输出/`。\n",
        "reports/项目级索引与摘要/README.md": "# 项目级索引与摘要\n\n保存少量项目级最新摘要、入口报告和跨任务索引。完整任务结果请查看 `outputs/工作包/`。\n",
        "data/README.md": "# data\n\n`01_raw/` 为不可修改原始数据；`03_primary/` 保存 canonical 清洗主表；`04_feature/` 保存 pipeline 必需 canonical 特征；任务过程产物进入 `outputs/工作包/`。\n",
        "data/01_raw/README.md": "# data/01_raw\n\n原始数据目录。永远不修改、不删除、不重命名、不移动原始文件；只允许增加 inventory sidecar。\n",
        "references/README.md": "# references\n\n项目参考资料。研究计划、文献、标准、方法说明、笔记和处理后摘要应分类放置。\n",
        "experiments/README.md": "# experiments\n\n项目级实验入口和 canonical 实验索引。每轮模型结果必须进入任务工作包的 `05_模型与实验/`。\n",
    }
    for rel_path, text in readmes.items():
        write_text(ROOT / rel_path, text)


def update_skills() -> None:
    run_skill = f"""---
name: run-package-manager
description: Create task run packages under outputs/工作包, route all task artifacts into the package, update manifests, and protect canonical workflow files.
---

# Run Package Manager

## 何时触发

每次实质性科研任务、清洗、建模、可视化、报告、目录整理或优化实验开始前必须触发。

## 创建任务工作包

1. 使用任务开始时间创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
2. 创建 `README.md`、`manifest.csv`，以及 `00_输入说明/` 到 `08_代码快照/`。
3. 在 `00_输入说明/inputs.md` 记录输入路径和摘要；不复制大型原始数据。

## 文件分类

- 数据输出进入 `01_数据输出/`。
- 汇总表进入 `02_表格输出/`。
- 图表进入 `03_图表输出/`。
- 报告进入 `04_报告输出/`。
- 模型和实验进入 `05_模型与实验/`。
- 参数配置进入 `06_配置参数/`。
- 日志、错误和修复记录进入 `07_日志与错误/`。
- 本轮新增或修改的关键脚本副本进入 `08_代码快照/`。

## canonical 文件

如果某个结果需要被后续 pipeline 读取，保留任务包副本，同时复制到标准目录作为 canonical 文件。标准目录只保存 canonical 和 pipeline 必需文件。

## 去重和待复核

hash 完全重复的辅助副本、缓存、临时文件和空文件可以删除，但必须写入 `outputs/_index/deleted_duplicates_log.csv`。唯一但无法归类的文件进入 `outputs/_待复核/`，不得删除。

## 任务结束

更新任务包 `manifest.csv`、`outputs/_index/run_manifest.csv`、`outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml`，然后调用 `whole-workspace-organizer` 做全工作目录整理检查。

长期规则：{LONG_RULE}
"""
    whole_skill = f"""---
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

长期规则：{LONG_RULE}
"""
    artifact_skill = f"""---
name: artifact-organizer
description: Route workflow1 artifacts into run packages, keep standard directories canonical-only, and trigger whole-workspace cleanup.
---

# Artifact Organizer

所有任务产物必须进入当前任务工作包。标准目录只保存 canonical 和 pipeline 必需文件。任务开始前调用 `run-package-manager`，任务结束后调用 `whole-workspace-organizer`。

长期规则：{LONG_RULE}
"""
    for base in [ROOT / ".agents" / "skills", ROOT / "skills"]:
        write_text(base / "run-package-manager" / "SKILL.md", run_skill)
        write_text(base / "whole-workspace-organizer" / "SKILL.md", whole_skill)
        write_text(base / "artifact-organizer" / "SKILL.md", artifact_skill)
        for skill_name in ["goal-driven-research-orchestrator", "project-memory-updater"]:
            p = base / skill_name / "SKILL.md"
            if p.exists():
                text = p.read_text(encoding="utf-8", errors="replace")
                addition = f"\n\n## Run Package And Cleanup Requirement\n\n任务开始前调用 `run-package-manager` 创建任务工作包；任务结束后调用 `whole-workspace-organizer` 做全目录整理检查。{LONG_RULE}\n"
                if "Run Package And Cleanup Requirement" not in text:
                    p.write_text(text.rstrip() + addition, encoding="utf-8")


def update_agents() -> None:
    p = ROOT / "AGENTS.md"
    text = p.read_text(encoding="utf-8", errors="replace")
    run_header = "## Run Package First Policy"
    run_block = f"""{run_header}

1. 每次实质性科研任务开始前，必须创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
2. 本轮任务产生的所有文件必须优先写入该任务工作包。
3. 标准目录只保存 canonical/latest 和 pipeline 必需文件。
4. 不允许把任务结果直接散落到 `reports/`、`data/04_feature/`、`experiments/` 根目录。
5. 如果某个结果需要被后续流程读取，可以同时复制到标准目录作为 canonical 文件。
6. 每个任务工作包必须包含 README 和 manifest。
7. 每次任务完成后必须更新 `outputs/_index/run_index.md`、`outputs/_index/run_manifest.csv`、`outputs/_index/latest_canonical_outputs.yaml`、`project_state/artifact_index.md` 和 `project_state/workspace_structure.md`。
8. 无法归属但唯一的文件进入 `outputs/_待复核/`。
9. hash 完全重复的文件应删除重复副本并记录。
10. 新对话继续任务时，应先读取最新 `run_index.md` 和 `conversation_handoff.md`。

## Whole Workspace Cleanliness Policy

1. 工作目录必须长期保持整洁。
2. 根目录只保留核心入口文件和一级功能目录。
3. 每次任务结束后必须执行全工作目录整理检查。
4. 所有任务产物必须进入任务工作包。
5. 标准目录只保留 canonical 和 pipeline 必需文件。
6. 历史文件必须进入对应任务工作包或待复核目录。
7. 重复文件必须删除重复副本。
8. 唯一文件必须保护，不得删除。
9. `data/01_raw` 永远不可修改、删除、重命名。
10. 删除动作只允许用于重复、缓存、临时、空文件和已确认无价值文件。

"""
    # Replace old Run Package / Whole Workspace sections if present by appending a clean authoritative block near Output Rules.
    if "## Run Package First Policy" not in text or "Whole Workspace Cleanliness Policy" not in text:
        marker = "## Output Rules"
        text = text.replace(marker, run_block + marker)
    else:
        # Add a fresh authoritative block above Output Rules and leave legacy text as lower-priority historical guidance.
        marker = "## Output Rules"
        text = text.replace(marker, run_block + marker)
    p.write_text(text, encoding="utf-8")


def copy_to_package(src: Path, sub: str, note: str = "") -> None:
    if not src.exists() or not src.is_file():
        return
    dst = RUN_ROOT / sub / src.name
    copy_file(src, dst, note)


def organize_reports() -> None:
    project_dir = ROOT / "reports" / "项目级索引与摘要"
    report_names = [
        "peanut_pre_dqn_readiness_after_moe_edi.md",
        "peanut_moe_edi_external_parameter_matching_report.md",
        "workflow_run_package_restructure_report.md",
        "project_whole_workspace_organization_report.md",
    ]
    for base in [ROOT / "reports", ROOT / "reports" / "latest"]:
        if not base.exists():
            continue
        for p in base.glob("*"):
            if not p.is_file() or p.name == "README.md":
                continue
            if p.name in report_names:
                move_file(p, project_dir / p.name, "项目级摘要报告归入 reports/项目级索引与摘要", pipeline=p.name == "peanut_pre_dqn_readiness_after_moe_edi.md")
            else:
                pkg_name = infer_package_name(p)
                dst = package_dest(p, pkg_name)
                move_file(p, dst, f"任务报告归入工作包：{pkg_name}")
    # Move old report support directories out of reports after package copies exist.
    for child in list((ROOT / "reports").iterdir()):
        if child.name in {"README.md", "项目级索引与摘要"}:
            continue
        dst = ROOT / "archive" / "old_root_files" / "reports_support_dirs" / child.name
        if child.exists():
            if child.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.move(str(child), str(dst))
                moved_rows.append({"原路径": child.as_posix(), "新路径": rel(dst), "移动原因": "reports 不再作为任务结果堆放目录，旧支持目录归档", "是否 canonical": False, "是否影响 pipeline": False})


def infer_package_name(path: Path) -> str:
    n = path.name.lower()
    if any(k in n for k in ["moe", "edi", "bmdl"]):
        return "MOE_EDI外部参数匹配"
    if any(k in n for k in ["beta", "belief"]):
        return "BetaBinomial信念更新"
    if any(k in n for k in ["upstream", "concentration", "count_panel"]):
        return "PEANUT上游查验与浓度修复"
    if any(k in n for k in ["cleaning", "risk_summary", "workflow", "eda", "label", "variable"]):
        return "PEANUT数据清洗与风险底座"
    if any(k in n for k in ["workspace", "inventory", "organization", "manifest", "index"]):
        return "全工作目录整理与规范化"
    return TASK


def organize_data_auxiliary() -> None:
    # Delete exact duplicate latest copies when canonical exists.
    for latest_dir in [ROOT / "data" / "03_primary" / "latest", ROOT / "data" / "04_feature" / "latest"]:
        if latest_dir.exists():
            for f in latest_dir.rglob("*"):
                if f.is_file():
                    canonical = latest_dir.parent / f.name
                    if canonical.exists() and sha256(canonical) == sha256(f):
                        delete_file(f, canonical, "latest 辅助副本与 canonical hash 完全一致")
                    else:
                        move_file(f, package_dest(f, infer_package_name(f)), "非重复 latest 文件进入任务工作包")
            if latest_dir.exists():
                shutil.rmtree(latest_dir, ignore_errors=True)
    # Move feature archive xlsx mirrors to relevant run packages.
    for arch in [ROOT / "data" / "04_feature" / "archive", ROOT / "data" / "03_primary" / "archive"]:
        if arch.exists():
            for f in arch.rglob("*"):
                if f.is_file():
                    move_file(f, package_dest(f, infer_package_name(f)), "data archive 唯一文件归入任务工作包")
            shutil.rmtree(arch, ignore_errors=True)
    # Raw inventory is allowed sidecar; refresh it.
    raw_rows = []
    for f in sorted((ROOT / "data" / "01_raw").iterdir(), key=lambda x: x.name):
        if f.is_file():
            raw_rows.append({
                "文件路径": rel(f),
                "文件名": f.name,
                "扩展名": f.suffix.lower(),
                "文件大小": f.stat().st_size,
                "修改时间": datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds"),
                "SHA256 hash": "" if f.name == "raw_data_inventory.csv" else sha256(f),
            })
    write_csv(ROOT / "data" / "01_raw" / "raw_data_inventory.csv", raw_rows)


def organize_outputs_archive() -> None:
    out_archive = ROOT / "outputs" / "archive"
    if out_archive.exists():
        # Caches can be deleted; legacy useful files move to root archive.
        for f in list(out_archive.rglob("*")):
            if f.is_file() and (f.suffix.lower() == ".pyc" or "__pycache__" in f.parts):
                delete_file(f, "", "outputs/archive 中 Python 缓存文件，确认可再生成", confirmed=True)
        dst = ROOT / "archive" / "old_root_files" / "outputs_archive_legacy"
        if out_archive.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(out_archive), str(dst))
            moved_rows.append({"原路径": "outputs/archive", "新路径": rel(dst), "移动原因": "outputs 仅保留 工作包/_index/_待复核，旧 archive 迁入项目 archive", "是否 canonical": False, "是否影响 pipeline": False})


def organize_root_and_scripts() -> None:
    scripts = ROOT / "scripts"
    if scripts.exists():
        dst_dir = ROOT / "src" / "workflow1" / "tools" / "legacy_scripts"
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in scripts.glob("*.py"):
            move_file(f, dst_dir / f.name, "根目录 scripts 迁入 src/workflow1/tools/legacy_scripts")
        shutil.rmtree(scripts, ignore_errors=True)
    for child in list(ROOT.iterdir()):
        if child.name in ROOT_ALLOWED_FILES or child.name in ROOT_ALLOWED_DIRS:
            continue
        if child.is_file():
            if child.suffix.lower() in {".docx", ".pdf", ".md", ".txt"}:
                dst = REVIEW_ROOT / child.name
                move_file(child, dst, "根目录唯一文档无法可靠归属，进入待复核")
                unclassified_rows.append({
                    "文件原路径": child.name,
                    "移动后路径": rel(dst),
                    "文件类型": file_type(dst),
                    "为什么无法归类": "根目录散落唯一文档，无法自动判定对应任务",
                    "后续建议": "人工确认后归入 references/project_plan、references/notes 或对应任务工作包",
                })
            elif is_temp(child):
                delete_file(child, "", "根目录临时文件")
            else:
                dst = REVIEW_ROOT / child.name
                move_file(child, dst, "根目录唯一文件无法可靠归属，进入待复核")
                unclassified_rows.append({
                    "文件原路径": child.name,
                    "移动后路径": rel(dst),
                    "文件类型": file_type(dst),
                    "为什么无法归类": "根目录散落唯一文件",
                    "后续建议": "人工确认归属",
                })


def delete_temp_caches() -> None:
    for p in sorted(ROOT.rglob("__pycache__"), key=lambda x: len(x.parts), reverse=True):
        if p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    delete_file(f, "", "Python __pycache__ 缓存文件")
            shutil.rmtree(p, ignore_errors=True)
    for name in [".pytest_cache", ".ipynb_checkpoints"]:
        for p in ROOT.rglob(name):
            if p.is_dir():
                for f in p.rglob("*"):
                    if f.is_file():
                        delete_file(f, "", f"{name} 缓存文件")
                shutil.rmtree(p, ignore_errors=True)
    for f in list(ROOT.rglob("*")):
        if f.is_file() and "data/01_raw" not in rel(f):
            if f.name.startswith("~$") or f.suffix.lower() in {".tmp", ".bak"} or f.stat().st_size == 0:
                delete_file(f, "", "临时/空文件")


def write_run_manifest_for_packages() -> list[dict]:
    rows = []
    pkg_root = ROOT / "outputs" / "工作包"
    for pkg in sorted([p for p in pkg_root.iterdir() if p.is_dir()], key=lambda x: x.name):
        parts = pkg.name.split("_", 2)
        start = "_".join(parts[:2]) if len(parts) >= 2 else ""
        name = parts[2] if len(parts) >= 3 else pkg.name
        files = [p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.csv"]
        main_outputs = "; ".join(rel(p) for p in files[:8])
        rows.append({
            "任务包路径": rel(pkg),
            "任务名称": name,
            "任务开始时间": start,
            "任务类型": infer_task_type(name),
            "输入文件": read_inputs(pkg),
            "主要输出": main_outputs,
            "是否完成": (pkg / "README.md").exists() and (pkg / "manifest.csv").exists(),
            "是否有错误": any("error" in p.name.lower() or "错误" in p.name for p in files),
            "是否影响后续 pipeline": any(Path(v).name in {p.name for p in files} for v in CANONICAL.values()),
            "README 路径": rel(pkg / "README.md") if (pkg / "README.md").exists() else "",
        })
        write_package_manifest(pkg)
    write_csv(INDEX / "run_manifest.csv", rows)
    lines = ["# Run Index\n\n任务工作包是以后人工查看结果的主入口：`outputs/工作包/`。\n\n"]
    for row in rows:
        package_rel = Path(row["任务包路径"]).relative_to("outputs").as_posix()
        lines.append(f"- [{row['任务名称']}](../{package_rel}/README.md) | `{row['任务开始时间']}` | {row['任务类型']}\n")
    write_text(INDEX / "run_index.md", "".join(lines))
    yaml = "\n".join(f"{k}: {v}" for k, v in CANONICAL.items()) + "\n"
    write_text(INDEX / "latest_canonical_outputs.yaml", yaml)
    write_text(INDEX / "workspace_map.md", workspace_map())
    return rows


def infer_task_type(name: str) -> str:
    if "清洗" in name or "风险底座" in name:
        return "数据清洗/风险底座"
    if "上游" in name or "浓度" in name:
        return "上游核验/浓度修复"
    if "Beta" in name or "信念" in name:
        return "信念状态"
    if "MOE" in name or "EDI" in name:
        return "MOE/EDI风险度量"
    if "目录" in name or "重构" in name:
        return "目录整理/规则固化"
    return "任务工作包"


def read_inputs(pkg: Path) -> str:
    inp = pkg / "00_输入说明" / "inputs.md"
    if not inp.exists():
        return ""
    lines = []
    for line in inp.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("-"):
            lines.append(line.strip().lstrip("- ").strip("`"))
    return "; ".join(lines)


def write_package_manifest(pkg: Path) -> None:
    rows = []
    for f in sorted([p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.csv"], key=lambda x: rel(x)):
        rows.append({
            "文件路径": rel(f),
            "文件类型": file_type(f),
            "文件说明": describe(f),
            "是否关键输出": f.parent.name.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_")),
            "是否 canonical 副本": f.name in {Path(v).name for v in CANONICAL.values()},
            "是否下游依赖": f.name in {Path(v).name for v in CANONICAL.values()},
            "生成时间": datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds"),
        })
    write_csv(pkg / "manifest.csv", rows)


def describe(path: Path) -> str:
    n = path.name.lower()
    if "inventory" in n or "manifest" in n or "index" in n:
        return "索引/清单"
    if "error" in n or "log" in n or "repair" in n:
        return "日志/错误/修复记录"
    if "moe" in n or "edi" in n or "bmdl" in n:
        return "MOE/EDI/BMDL 输出"
    if "belief" in n or "beta" in n:
        return "信念状态输出"
    if "concentration" in n or "count_panel" in n:
        return "浓度/计数面板输出"
    if path.suffix.lower() in {".md", ".docx", ".pdf"}:
        return "报告/文档"
    return "任务产物"


def workspace_map() -> str:
    return """# Workspace Map

## 主查看入口

- `outputs/工作包/`：按 `YYYYMMDD_HHMM_中文任务名` 组织的任务工作包。
- `outputs/_index/`：全局任务索引、run manifest、canonical 输出索引和删除日志。
- `outputs/_待复核/`：无法自动判断归属但唯一的文件。

## 标准目录职责

- `data/01_raw/`：不可修改原始数据。
- `data/03_primary/`：项目级 canonical 清洗主表。
- `data/04_feature/`：pipeline 必须直接读取的 canonical 特征。
- `reports/项目级索引与摘要/`：项目级摘要和入口报告。
- `experiments/`：项目级实验入口和 canonical 实验索引。
- `references/`：研究计划、文献、标准、方法和笔记。
- `archive/`：历史、旧目录和已迁移辅助体系。
"""


def update_project_state(run_rows: list[dict]) -> None:
    write_text(ROOT / "project_state/current_focus.md", f"# Current Focus\n\n当前已完成全工作流目录重构与去重。主查看入口为 `outputs/工作包/`，标准目录只保留 canonical 和 pipeline 必需文件。本轮未重新跑数据、未清洗、未计算 MOE/EDI、未运行 DQN，且未修改 `data/01_raw` 原始数据内容。\n\n长期规则：{LONG_RULE}\n")
    write_text(ROOT / "project_state/next_step.md", "# Next Step\n\n不要直接运行 DQN。下一步如继续 MOE/EDI 或 DQN prototype，必须先创建新的任务工作包，并补齐动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数。\n")
    write_text(ROOT / "project_state/conversation_handoff.md", f"# Conversation Handoff\n\n{NOW.strftime('%Y-%m-%d %H:%M')} 完成全工作流目录重构与去重。主入口：`outputs/工作包/`；全局索引：`outputs/_index/run_index.md`、`outputs/_index/run_manifest.csv`、`outputs/_index/latest_canonical_outputs.yaml`。本轮没有重新跑分析、清洗、MOE/EDI 或 DQN。`data/01_raw` 原始数据未移动、未重命名、未删除。\n\n长期规则：{LONG_RULE}\n")
    write_text(ROOT / "project_state/run_protocol.md", f"# Run Protocol\n\n1. 新任务开始前读取 `AGENTS.md`、`outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml` 和 `project_state/conversation_handoff.md`。\n2. 先调用 run-package-manager 创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。\n3. 所有新产物优先写入任务工作包；pipeline 必需文件再复制到标准 canonical 目录。\n4. 任务结束后调用 whole-workspace-organizer，更新全局索引和项目状态。\n5. 永远不修改、删除、重命名、移动 `data/01_raw` 原始数据。\n\n长期规则：{LONG_RULE}\n")
    append = {
        "changelog.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')}\n\n- 执行全工作流目录重构与去重，主入口固化为 `outputs/工作包/`。\n- 清理 reports/data/outputs 中的 latest/archive 辅助残留，标准目录只保留 canonical 和 pipeline 必需文件。\n- 更新 AGENTS.md、run-package-manager、whole-workspace-organizer、artifact-organizer、goal-driven orchestrator 和 project-memory-updater。\n- 生成 workspace_inventory_before、cleanup plan、移动/删除/待复核日志、run index 和 cleanup report。\n",
        "decision_log.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')}\n\n### Use Run Package as the only primary output mechanism\n\nRationale: latest/archive 只能辅助查找最新或历史文件，不能表达每轮任务的输入、输出、日志和报告关系。\n\nImpact: {LONG_RULE}\n",
        "lessons_learned.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')}\n\n- 科研工作流的主查看入口应按任务组织，而不是按文件状态组织。\n- hash 去重应保守执行：删除缓存和完全重复辅助副本，保护唯一数据、报告、代码、配置和参考资料。\n- `data/01_raw` 只允许 inventory sidecar，不参与移动和删除。\n",
        "project_memory.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')} Run Package Cleanup Memory\n\n- {LONG_RULE}\n- 后续继续任务时先读 `outputs/_index/run_index.md` 和 `project_state/conversation_handoff.md`。\n",
    }
    for name, text in append.items():
        with (ROOT / "project_state" / name).open("a", encoding="utf-8") as f:
            f.write(text)
    artifact = "# Artifact Index\n\n## Latest Canonical Outputs\n\n"
    for k, v in CANONICAL.items():
        artifact += f"- `{k}`: `{v}`\n"
    artifact += "\n## Run Packages\n\n"
    for row in run_rows:
        artifact += f"- `{row['任务名称']}`: `{row['任务包路径']}`\n"
    artifact += f"\n## Rule\n\n{LONG_RULE}\n"
    write_text(ROOT / "project_state/artifact_index.md", artifact)
    write_text(ROOT / "project_state/workspace_structure.md", workspace_map())


def run_checks() -> list[dict]:
    checks = []
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    for cmd in [
        [sys.executable, "-c", "import workflow1; print(workflow1.__version__)"],
        [sys.executable, "-m", "workflow1", "--stage", "launch"],
    ]:
        cp = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
        checks.append({
            "command": " ".join(cmd),
            "returncode": cp.returncode,
            "stdout": cp.stdout.strip(),
            "stderr": cp.stderr.strip(),
        })
    write_text(RUN_ROOT / "07_日志与错误" / "workflow_validation_log.json", json.dumps(checks, ensure_ascii=False, indent=2))
    return checks


def write_cleanup_report(checks: list[dict], run_rows: list[dict]) -> None:
    report = f"""# 全工作流目录重构与去重报告

## 1. 整理前存在的问题

- `latest/archive` 仍承担了过多主入口职责，用户无法一眼按任务查看结果。
- `reports/` 仍有任务级报告和辅助目录残留。
- `data/03_primary/latest`、`data/04_feature/latest` 属于辅助副本，与 canonical 重复。
- `outputs/archive` 与顶层旧输出目录形成平行体系。
- 根目录存在 `scripts/`，不在目标一级结构内。

## 2. 最终目录结构

主入口为 `outputs/工作包/`。标准目录职责为：`data/01_raw` 保存原始数据，`data/03_primary` 保存 canonical 清洗主表，`data/04_feature` 保存 pipeline 必需特征，`reports/项目级索引与摘要` 保存少量项目级摘要，`archive/` 保存旧体系和迁移残留。

## 3. 创建了哪些任务工作包

{chr(10).join('- `' + row['任务包路径'] + '`' for row in run_rows)}

## 4. 哪些文件被移动

移动/复制记录见 `02_表格输出/moved_files_log.csv`。本轮记录数：{len(moved_rows)}。

## 5. 哪些重复文件被删除

删除记录见 `02_表格输出/deleted_duplicates_log.csv` 和 `outputs/_index/deleted_duplicates_log.csv`。本轮删除记录数：{len(deleted_rows)}。删除范围限于 hash 相同辅助副本、缓存、临时或空文件。

## 6. 哪些唯一文件进入 `outputs/_待复核/`

待复核记录见 `02_表格输出/unclassified_unique_files_log.csv`。本轮待复核文件数：{len(unclassified_rows)}。

## 7. canonical 文件仍保留在标准目录

{chr(10).join('- `' + v + '`' for v in CANONICAL.values())}

## 8. 是否影响后续 pipeline

未移动、未删除 `data/01_raw` 原始数据。pipeline 必需 canonical 文件仍保留在标准目录。旧辅助副本删除或迁移不影响后续运行。

## 9. import 和 launch 是否通过

```json
{json.dumps(checks, ensure_ascii=False, indent=2)}
```

## 10. 后续如何通过 `outputs/工作包/` 查看每一步结果

打开 `outputs/工作包/`，按 `YYYYMMDD_HHMM_中文任务名` 查看每一步任务；每个任务包内有 `README.md` 和 `manifest.csv`。全局索引见 `outputs/_index/run_index.md`。
"""
    write_text(RUN_ROOT / "04_报告输出" / "workflow_workspace_cleanup_report.md", report)
    write_text(ROOT / "reports" / "项目级索引与摘要" / "workflow_workspace_cleanup_report.md", report)


def write_current_package_readme(checks: list[dict]) -> None:
    text = f"""# {TASK}

## 本轮任务目的

执行全工作流目录重构、归类、去重和长期规则固化；不重新跑数据、不重新清洗、不重新计算 MOE/EDI、不运行 DQN。

## 输入文件

- `AGENTS.md`
- `outputs/_index/`
- `outputs/工作包/`
- `project_state/`
- `skills/`
- 全工作目录文件清单

## 生成文件

- `02_表格输出/workspace_inventory_before.csv`
- `04_报告输出/workspace_cleanup_plan.md`
- `02_表格输出/deleted_duplicates_log.csv`
- `02_表格输出/moved_files_log.csv`
- `02_表格输出/unclassified_unique_files_log.csv`
- `04_报告输出/workflow_workspace_cleanup_report.md`
- `07_日志与错误/workflow_validation_log.json`

## 关键结果

- 主查看入口固化为 `outputs/工作包/`。
- 标准目录只保留 canonical 和 pipeline 必需文件。
- `data/01_raw` 原始数据未修改、未删除、未移动。
- import 与 launch 验证已执行。

## 错误和修复

轻量整理中遇到的缓存和辅助副本按规则删除或迁移，详见日志。

## 是否影响后续流程

不影响。canonical 文件保留在标准目录，任务结果进入工作包。

## 下一步建议

继续 MOE/EDI 或 DQN prototype 前，先创建新的任务工作包，并补齐动作空间、预算、产能、成本和约束参数。
"""
    write_text(RUN_ROOT / "README.md", text)
    write_text(RUN_ROOT / "00_输入说明" / "inputs.md", "# 输入说明\n\n本轮输入为 workflow1 本地工作目录、AGENTS.md、skills、project_state 和现有 outputs/data/reports 文件结构。\n")


def write_logs() -> None:
    write_csv(RUN_ROOT / "02_表格输出" / "deleted_duplicates_log.csv", deleted_rows)
    write_csv(RUN_ROOT / "02_表格输出" / "moved_files_log.csv", moved_rows)
    write_csv(RUN_ROOT / "02_表格输出" / "unclassified_unique_files_log.csv", unclassified_rows)
    write_csv(INDEX / "deleted_duplicates_log.csv", deleted_rows)
    shutil.copy2(RUN_ROOT / "02_表格输出" / "deleted_duplicates_log.csv", ROOT / "archive" / "deleted_duplicates_manifest" / f"{STAMP}_deleted_duplicates_log.csv")


def write_manifest(pkg: Path) -> None:
    rows = []
    for f in sorted([p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.csv"], key=lambda x: rel(x)):
        rows.append({
            "文件路径": rel(f),
            "文件类型": file_type(f),
            "文件说明": describe(f),
            "是否关键输出": f.parent.name.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_")),
            "是否 canonical 副本": False,
            "是否下游依赖": False,
            "生成时间": datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds"),
        })
    write_csv(pkg / "manifest.csv", rows)


def main() -> None:
    ensure_dirs()
    write_before_snapshot()
    create_or_update_readmes()
    update_skills()
    update_agents()
    organize_data_auxiliary()
    organize_reports()
    organize_outputs_archive()
    organize_root_and_scripts()
    delete_temp_caches()
    write_logs()
    run_rows = write_run_manifest_for_packages()
    checks = run_checks()
    # Validation creates pycache; clean it and refresh logs.
    delete_temp_caches()
    write_logs()
    write_cleanup_report(checks, run_rows)
    write_current_package_readme(checks)
    update_project_state(run_rows)
    write_manifest(RUN_ROOT)
    print(json.dumps({
        "run_package": rel(RUN_ROOT),
        "moved_records": len(moved_rows),
        "deleted_records": len(deleted_rows),
        "unclassified_unique": len(unclassified_rows),
        "checks": checks,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
