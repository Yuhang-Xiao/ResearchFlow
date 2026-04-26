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


ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now()
RUN_STAMP = NOW.strftime("%Y%m%d_%H%M")
TASK_NAME = "工作流任务包机制重构"
PACKAGE_ROOT = ROOT / "outputs" / "工作包"
REVIEW_ROOT = ROOT / "outputs" / "_待复核"
INDEX_DIR = ROOT / "outputs" / "_index"
ARCHIVE_ROOT = ROOT / "archive"
CURRENT_PACKAGE = PACKAGE_ROOT / f"{RUN_STAMP}_{TASK_NAME}"

PACKAGE_SUBDIRS = [
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

LONG_RULE = "以后每次任务必须先创建任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。所有新产物进入该任务包；标准目录只保存 canonical/latest 和 pipeline 必需文件；每个任务包必须有 README 和 manifest；任务结束后更新全局 run index。"

CANONICAL = {
    "cleaned_dataset": "data/03_primary/peanut_cleaned_analysis_ready.csv",
    "cleaned_dataset_xlsx": "data/03_primary/peanut_cleaned_analysis_ready.xlsx",
    "concentration_table": "data/04_feature/peanut_concentration_clean_table.csv",
    "concentration_distribution_summary": "data/04_feature/peanut_concentration_distribution_summary.csv",
    "count_panel": "data/04_feature/peanut_count_panel.csv",
    "beta_binomial_states": "data/04_feature/peanut_beta_binomial_belief_states.csv",
    "belief_mdp_features": "data/04_feature/peanut_belief_mdp_state_features.csv",
    "belief_mdp_features_with_moe_edi": "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv",
    "bmdl_config": "data/04_feature/peanut_bmdl_parameter_config.json",
    "bmdl_table": "data/04_feature/peanut_bmdl_parameter_table.csv",
    "consumption_parameter_table": "data/04_feature/peanut_consumption_parameter_table.csv",
    "population_parameter_table": "data/04_feature/peanut_population_parameter_table.csv",
    "moe_edi_risk_table": "data/04_feature/peanut_edi_moe_risk_table.csv",
    "moe_edi_risk_summary": "data/04_feature/peanut_edi_moe_risk_summary.csv",
    "latest_pre_dqn_readiness_report": "reports/latest/peanut_pre_dqn_readiness_after_moe_edi.md",
    "latest_handoff": "project_state/conversation_handoff.md",
}

PACKAGES = [
    {
        "stamp": "20260424_1908",
        "name": "PEANUT数据清洗与风险底座",
        "type": "数据清洗/EDA/风险底座",
        "inputs": ["data/01_raw/PEANUT2023-20241.xlsx", "references/processed_summaries/peanut_research_plan_summary.md"],
        "files": [
            "data/03_primary/peanut_cleaned_analysis_ready.csv",
            "data/03_primary/peanut_cleaned_analysis_ready.xlsx",
            "reports/peanut_cleaning_report.md",
            "reports/peanut_full_workflow_summary.md",
            "reports/peanut_workflow_run_summary.json",
            "reports/tables/peanut_data_quality_summary.csv",
            "reports/tables/peanut_label_dictionary.csv",
            "reports/tables/peanut_variable_dictionary.csv",
            "reports/tables/peanut_risk_summary_by_category.csv",
            "reports/tables/peanut_risk_summary_by_region.csv",
            "reports/tables/peanut_risk_summary_by_stage.csv",
            "reports/tables/peanut_risk_summary_by_year.csv",
            "reports/figures",
        ],
    },
    {
        "stamp": "20260424_2049",
        "name": "PEANUT上游查验与浓度修复",
        "type": "上游核验/浓度修复",
        "inputs": ["data/03_primary/peanut_cleaned_analysis_ready.csv"],
        "files": [
            "data/04_feature/peanut_concentration_clean_table.csv",
            "data/04_feature/peanut_concentration_distribution_summary.csv",
            "data/04_feature/peanut_count_panel.csv",
            "reports/peanut_concentration_cleaning_report.md",
            "reports/peanut_upstream_verification_report.md",
            "reports/peanut_upstream_repair_log.md",
            "reports/archive/20260424_整理前历史报告/peanut_count_panel_report.md",
            "reports/archive/20260424_整理前历史报告/peanut_upstream_audit_summary.json",
            "reports/tables/peanut_concentration_audit_findings.csv",
            "reports/tables/peanut_cleaning_issue_log.csv",
        ],
    },
    {
        "stamp": "20260424_2048",
        "name": "BetaBinomial信念更新",
        "type": "信念状态/Beta-Binomial",
        "inputs": ["data/04_feature/peanut_count_panel.csv"],
        "files": [
            "data/04_feature/peanut_beta_binomial_belief_states.csv",
            "data/04_feature/peanut_belief_mdp_state_features.csv",
            "data/04_feature/peanut_beta_binomial_config.json",
            "reports/peanut_beta_binomial_belief_update_report.md",
            "reports/archive/20260424_整理前历史报告/peanut_beta_binomial_error_log.md",
            "reports/archive/20260424_整理前历史报告/peanut_beta_binomial_run_summary.json",
            "reports/tables/peanut_belief_state_latest.csv",
            "reports/tables/peanut_belief_state_summary_by_stage.csv",
        ],
    },
    {
        "stamp": "20260424_2132",
        "name": "MOE_EDI外部参数匹配",
        "type": "MOE/EDI风险度量",
        "inputs": [
            "data/04_feature/peanut_concentration_clean_table.csv",
            "data/04_feature/peanut_belief_mdp_state_features.csv",
            "data/01_raw/Concentration_and_Consumption pEANUT.xlsx",
            "data/01_raw/population_long_clean.xlsx",
        ],
        "files": [
            "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv",
            "data/04_feature/peanut_bmdl_parameter_config.json",
            "data/04_feature/peanut_bmdl_parameter_table.csv",
            "data/04_feature/peanut_consumption_parameter_table.csv",
            "data/04_feature/peanut_population_parameter_table.csv",
            "data/04_feature/peanut_edi_moe_risk_table.csv",
            "data/04_feature/peanut_edi_moe_risk_summary.csv",
            "reports/peanut_moe_edi_external_parameter_matching_report.md",
            "reports/peanut_pre_dqn_readiness_after_moe_edi.md",
            "reports/peanut_moe_edi_error_log.md",
            "outputs/20260424_MOE_EDI外部参数匹配与风险度量准备",
        ],
    },
    {
        "stamp": "20260424_2244",
        "name": "全工作目录整理与规范化",
        "type": "目录整理/索引",
        "inputs": ["AGENTS.md", "project_state", "outputs/_index"],
        "files": [
            "reports/latest/project_whole_workspace_organization_report.md",
            "outputs/20260424_全工作目录整理与规范化",
            "outputs/_index/output_index.md",
            "outputs/_index/output_manifest.csv",
            "outputs/_index/latest_outputs.yaml",
            "outputs/_index/workspace_structure.md",
        ],
    },
]

reorganized: list[dict] = []
deleted_duplicates: list[dict] = []
unclassified: list[dict] = []


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def ensure_package(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for sub in PACKAGE_SUBDIRS:
        (path / sub).mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_dest(src: Path) -> str:
    suffix = src.suffix.lower()
    s = rel(src) if src.exists() else src.as_posix()
    name = src.name.lower()
    if suffix in {".md", ".docx", ".pdf"} or "/reports/" in s or s.startswith("reports/"):
        if any(k in name for k in ["error", "repair", "log"]):
            return "07_日志与错误"
        return "04_报告输出"
    if suffix in {".csv", ".xlsx", ".xls"}:
        if s.startswith("data/"):
            return "01_数据输出"
        return "02_表格输出"
    if suffix in {".svg", ".png", ".jpg", ".jpeg"}:
        return "03_图表输出"
    if suffix in {".json", ".yaml", ".yml", ".toml"}:
        if any(k in name for k in ["error", "log", "summary"]):
            return "07_日志与错误"
        return "06_配置参数"
    if suffix in {".py"}:
        return "08_代码快照"
    return "01_数据输出"


def copy_item(src: Path, pkg: Path, note: str, canonical: bool = False) -> None:
    if not src.exists():
        return
    if src.is_dir():
        for file in src.rglob("*"):
            if file.is_file():
                copy_item(file, pkg, note, canonical)
        return
    sub = classify_dest(src)
    dst = pkg / sub / src.name
    if dst.exists():
        if sha256(src) == sha256(dst):
            return
        dst = pkg / sub / f"{src.stem}_{datetime.fromtimestamp(src.stat().st_mtime).strftime('%Y%m%d_%H%M%S')}{src.suffix}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    reorganized.append({
        "源文件路径": rel(src),
        "目标文件路径": rel(dst),
        "操作": "copy",
        "说明": note,
        "是否canonical副本": canonical,
        "时间": datetime.now().isoformat(timespec="seconds"),
    })


def move_top_output_to_package(old: Path, pkg: Path) -> None:
    if not old.exists() or not old.is_dir():
        return
    # Copy contents into package subdirectories, then move old directory into archive only if not already under 工作包.
    for file in old.rglob("*"):
        if file.is_file():
            copy_item(file, pkg, f"from legacy output dir {rel(old)}", canonical=False)
    archive_dst = ARCHIVE_ROOT / "legacy_outputs_after_run_package_restructure" / old.name
    archive_dst.parent.mkdir(parents=True, exist_ok=True)
    if archive_dst.exists():
        shutil.rmtree(archive_dst)
    shutil.move(str(old), str(archive_dst))
    reorganized.append({
        "源文件路径": rel(old),
        "目标文件路径": rel(archive_dst),
        "操作": "move",
        "说明": "legacy top-level output directory moved after copying into run package",
        "是否canonical副本": False,
        "时间": datetime.now().isoformat(timespec="seconds"),
    })


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


def package_manifest(pkg: Path) -> list[dict]:
    rows = []
    for file in sorted([p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.csv"], key=lambda x: rel(x)):
        r = rel(file)
        rows.append({
            "文件路径": r,
            "文件类型": file.suffix.lower().lstrip(".") or "directory_index",
            "文件说明": describe_file(file),
            "是否关键输出": file.parent.name in {"01_数据输出", "02_表格输出", "04_报告输出", "06_配置参数"},
            "是否canonical副本": any(file.name == Path(v).name for v in CANONICAL.values()),
            "是否下游依赖": any(file.name == Path(v).name for v in CANONICAL.values()),
            "生成时间": datetime.fromtimestamp(file.stat().st_mtime).isoformat(timespec="seconds"),
        })
    write_csv(pkg / "manifest.csv", rows, ["文件路径", "文件类型", "文件说明", "是否关键输出", "是否canonical副本", "是否下游依赖", "生成时间"])
    return rows


def describe_file(path: Path) -> str:
    name = path.name
    if "concentration_clean" in name:
        return "AFB1 浓度清洗或相关报告"
    if "count_panel" in name:
        return "计数面板"
    if "belief" in name or "beta" in name:
        return "信念状态或 Beta-Binomial 输出"
    if "moe" in name.lower() or "edi" in name.lower() or "bmdl" in name.lower():
        return "MOE/EDI/BMDL 风险度量输出"
    if "inventory" in name or "manifest" in name or "index" in name:
        return "索引或清单"
    if path.suffix.lower() in {".md", ".docx", ".pdf"}:
        return "报告或说明文档"
    return "任务文件"


def create_package_readme(pkg: Path, spec: dict, manifest_rows: list[dict]) -> None:
    readme = f"""# {spec['name']}

## 任务开始时间

{spec['stamp']}

## 任务类型

{spec['type']}

## 输入文件

{chr(10).join('- `' + x + '`' for x in spec.get('inputs', []))}

## 输出说明

本工作包按 Run Package 机制重组得到，包含本任务相关的数据、表格、报告、配置、日志或图表副本。大原始数据不复制，仅在 `00_输入说明/inputs.md` 记录路径。

## 文件数量

{len(manifest_rows)}

## 是否影响后续 pipeline

pipeline 必需 canonical 文件仍保留在标准目录；本工作包内为可阅读、可追踪副本。
"""
    write_text(pkg / "README.md", readme)
    write_text(pkg / "00_输入说明" / "inputs.md", "# 输入文件\n\n" + "\n".join(f"- `{x}`" for x in spec.get("inputs", [])) + "\n")


def setup_dirs() -> None:
    for d in [PACKAGE_ROOT, REVIEW_ROOT, INDEX_DIR, ARCHIVE_ROOT]:
        d.mkdir(parents=True, exist_ok=True)
    ensure_package(CURRENT_PACKAGE)
    write_text(ROOT / "outputs" / "README.md", "# outputs\n\n人工查看结果的主入口是 `outputs/工作包/`。每个实质性任务必须创建 `YYYYMMDD_HHMM_中文任务名/` 工作包，包含 README、manifest 和分类子目录。全局索引位于 `_index/`，无法自动归属的唯一文件进入 `_待复核/`。\n")


def build_historical_packages() -> list[dict]:
    run_rows = []
    for spec in PACKAGES:
        pkg = PACKAGE_ROOT / f"{spec['stamp']}_{spec['name']}"
        ensure_package(pkg)
        for item in spec["files"]:
            src = ROOT / item
            if src.exists():
                if item.startswith("outputs/20260424_"):
                    move_top_output_to_package(src, pkg)
                else:
                    copy_item(src, pkg, f"historical package: {spec['name']}", canonical=item in CANONICAL.values())
        manifest_rows = package_manifest(pkg)
        create_package_readme(pkg, spec, manifest_rows)
        run_rows.append(run_row(pkg, spec, manifest_rows))
    return run_rows


def run_row(pkg: Path, spec: dict, manifest_rows: list[dict]) -> dict:
    return {
        "任务包路径": rel(pkg),
        "任务名称": spec["name"],
        "任务开始时间": spec["stamp"],
        "任务类型": spec["type"],
        "输入文件": "; ".join(spec.get("inputs", [])),
        "主要输出": "; ".join([r["文件路径"] for r in manifest_rows[:8]]),
        "是否完成": True,
        "是否有错误": any("error" in r["文件路径"].lower() or "错误" in r["文件路径"] for r in manifest_rows),
        "是否影响后续pipeline": any(r["是否下游依赖"] for r in manifest_rows),
        "对应README路径": rel(pkg / "README.md"),
    }


def current_package_outputs() -> dict:
    policy = f"""# Run Package Policy Snapshot

## Run Package First Policy

1. 每次实质性科研任务开始前，必须先创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。
2. 本轮任务产生的所有文件必须优先写入该任务工作包。
3. 标准目录只保存 canonical/latest 和 pipeline 必需文件。
4. 不允许把任务结果直接散落到 `reports/`、`data/04_feature/`、`experiments/` 根目录。
5. 如果某个结果需要被后续流程读取，可以同时复制到标准目录作为 canonical 文件。
6. 每个任务工作包必须包含 README 和 manifest。
7. 每次任务完成后必须更新 run index、run manifest、latest canonical outputs、artifact index 和 workspace structure。
8. 无法归属但唯一的文件进入 `outputs/_待复核/`。
9. hash 完全重复的文件应删除重复副本并记录。
10. 新对话继续任务时，应先读取最新 `outputs/_index/run_index.md` 和 `project_state/conversation_handoff.md`。

长期规则：{LONG_RULE}
"""
    write_text(CURRENT_PACKAGE / "06_配置参数" / "run_package_policy_snapshot.md", policy)
    copy_item(ROOT / "scripts" / "run_package_restructure.py", CURRENT_PACKAGE, "code snapshot for this restructuring task")
    copy_item(ROOT / "scripts" / "organize_workspace.py", CURRENT_PACKAGE, "related workspace organizer snapshot")
    return {
        "stamp": RUN_STAMP,
        "name": TASK_NAME,
        "type": "目录规则/Run Package机制",
        "inputs": ["AGENTS.md", "outputs/_index", "project_state", "skills"],
    }


def find_unclassified_unique() -> None:
    allowed_tops = {".agents", ".codex", "skills", "src", "prompts", "references", "data", "experiments", "outputs", "project_state", "reports", "scripts", "archive"}
    allowed_root_files = {"AGENTS.md", "START_HERE.md", "README.md", "pyproject.toml", "requirements.txt"}
    review_dir = REVIEW_ROOT / f"{NOW.strftime('%Y%m%d')}_未归类唯一文件"
    for p in ROOT.iterdir():
        if p.name in allowed_root_files or p.name in allowed_tops or p.name == ".git":
            continue
        if p.is_file():
            dst = review_dir / p.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dst))
            unclassified.append({
                "源文件路径": p.name,
                "目标文件路径": rel(dst),
                "原因": "root unique file could not be classified automatically",
                "时间": datetime.now().isoformat(timespec="seconds"),
            })


def safe_deduplicate() -> None:
    # Conservative dedupe: remove Python caches and temp locks; do not delete canonical, raw, state, code, or unique docs.
    for p in list(ROOT.rglob("*")):
        if not p.exists() or "data/01_raw" in rel(p):
            continue
        if p.is_file() and (p.suffix.lower() == ".pyc" or p.name.startswith("~$") or p.suffix.lower() in {".tmp", ".bak"}):
            keep = ""
            digest = sha256(p)
            deleted_duplicates.append({
                "删除文件路径": rel(p),
                "保留文件路径": keep,
                "SHA256": digest,
                "删除原因": "临时缓存或锁文件",
                "删除时间": datetime.now().isoformat(timespec="seconds"),
                "是否确认重复": True,
            })
            p.unlink()
    # Hash scan records duplicate candidates only; deletion is limited to safe temp/cache files.
    seen: dict[str, Path] = {}
    for p in sorted([x for x in ROOT.rglob("*") if x.is_file() and ".git" not in x.parts], key=lambda x: rel(x)):
        if p.stat().st_size == 0 and "data/01_raw" not in rel(p):
            digest = sha256(p)
            deleted_duplicates.append({
                "删除文件路径": rel(p),
                "保留文件路径": "",
                "SHA256": digest,
                "删除原因": "空临时文件",
                "删除时间": datetime.now().isoformat(timespec="seconds"),
                "是否确认重复": True,
            })
            p.unlink()
            continue
        if p.stat().st_size > 50 * 1024 * 1024:
            continue
        digest = sha256(p)
        if digest not in seen:
            seen[digest] = p
            continue
        # Do not delete non-temp duplicates because latest/canonical/report copies are intentional.


def update_agents_and_skills() -> None:
    ag = ROOT / "AGENTS.md"
    text = ag.read_text(encoding="utf-8", errors="replace")
    header = "## Run Package First Policy"
    block = f"""{header}

1. Every substantive scientific task must start by creating `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`.
2. All files produced by that task must be written to the task run package first.
3. Standard directories keep only canonical/latest and pipeline-required files.
4. Do not scatter task results directly into `reports/`, `data/04_feature/`, or `experiments/` roots.
5. If a result must be read by later workflow stages, also copy it to the standard directory as a canonical file.
6. Every run package must contain `README.md` and `manifest.csv`.
7. After each task, update `outputs/_index/run_index.md`, `outputs/_index/run_manifest.csv`, `outputs/_index/latest_canonical_outputs.yaml`, `project_state/artifact_index.md`, and `project_state/workspace_structure.md`.
8. Unique files that cannot be assigned to a run package go to `outputs/_待复核/`.
9. Exact hash duplicates may be deleted only after recording `outputs/_index/deleted_duplicates_log.csv`.
10. When continuing work in a new conversation, first read the latest `run_index.md` and `project_state/conversation_handoff.md`.

"""
    if header not in text:
        marker = "## Whole Workspace Organization Policy"
        if marker in text:
            text = text.replace(marker, block + marker)
        else:
            text += "\n\n" + block
        ag.write_text(text, encoding="utf-8")

    run_skill_body = f"""# Run Package Manager

## When To Trigger

Use before every substantive research, cleaning, modeling, visualization, reporting, optimization, or workspace organization task.

## Create A Run Package

1. Use task start time to create `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`.
2. Create `README.md`, `manifest.csv`, and subdirectories `00_输入说明/` through `08_代码快照/`.
3. Write input paths and assumptions in `00_输入说明/inputs.md`; do not copy large raw data.

## File Placement

- Generated data: `01_数据输出/`
- Summary tables: `02_表格输出/`
- Figures: `03_图表输出/`
- Reports: `04_报告输出/`
- Models and experiments: `05_模型与实验/`
- Configs and parameter files: `06_配置参数/`
- Logs and errors: `07_日志与错误/`
- Modified scripts or code notes: `08_代码快照/`

## Canonical Copies

If a result is needed by downstream pipeline stages, copy it to the standard canonical path under `data/`, `reports/latest/`, or `experiments/` while keeping the run package as the primary readable record.

## Indexing And Cleanup

Update the package `manifest.csv`, global `outputs/_index/run_manifest.csv`, `run_index.md`, `latest_canonical_outputs.yaml`, and project state indexes. Hash duplicate temporary or non-unique files before deletion and record deletions in `outputs/_index/deleted_duplicates_log.csv`. Unique unclassified files go to `outputs/_待复核/`.

## End Of Task

After the task finishes, call `whole-workspace-organizer` or run a whole workspace organization check.

长期规则：{LONG_RULE}
"""
    for base in [ROOT / ".agents" / "skills", ROOT / "skills"]:
        path = base / "run-package-manager" / "SKILL.md"
        write_text(path, f"---\nname: run-package-manager\ndescription: Create, populate, index, and validate workflow1 task run packages under outputs/工作包 before and after substantive tasks.\n---\n\n{run_skill_body}\n")

    targets = [
        ROOT / ".agents/skills/goal-driven-research-orchestrator/SKILL.md",
        ROOT / "skills/goal-driven-research-orchestrator/SKILL.md",
        ROOT / ".agents/skills/whole-workspace-organizer/SKILL.md",
        ROOT / "skills/whole-workspace-organizer/SKILL.md",
        ROOT / ".agents/skills/artifact-organizer/SKILL.md",
        ROOT / "skills/artifact-organizer/SKILL.md",
    ]
    for p in targets:
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="replace")
            if "run-package-manager" not in text:
                text += "\n\n## Run Package Requirement\n\nBefore every substantive task, call `run-package-manager` to create the task work package. After the task, call `whole-workspace-organizer` or run a whole workspace organization check. " + LONG_RULE + "\n"
                p.write_text(text, encoding="utf-8")


def write_indexes(run_rows: list[dict]) -> None:
    # Add current package row after its manifest exists.
    write_csv(INDEX_DIR / "run_manifest.csv", run_rows, ["任务包路径", "任务名称", "任务开始时间", "任务类型", "输入文件", "主要输出", "是否完成", "是否有错误", "是否影响后续pipeline", "对应README路径"])
    lines = ["# Run Index\n", "\n任务工作包是以后人工查看结果的主入口：`outputs/工作包/`。\n\n"]
    for row in run_rows:
        lines.append(f"- [{row['任务名称']}](../{Path(row['任务包路径']).relative_to('outputs').as_posix()}/README.md) | `{row['任务开始时间']}` | {row['任务类型']}\n")
    write_text(INDEX_DIR / "run_index.md", "".join(lines))
    yaml = "\n".join(f"{k}: {v}" for k, v in CANONICAL.items()) + "\n"
    write_text(INDEX_DIR / "latest_canonical_outputs.yaml", yaml)
    write_text(INDEX_DIR / "workspace_map.md", workspace_map_text())
    # Legacy compatibility copies.
    write_text(INDEX_DIR / "latest_outputs.yaml", yaml)
    write_text(INDEX_DIR / "output_index.md", "".join(lines))
    write_csv(INDEX_DIR / "deleted_duplicates_log.csv", deleted_duplicates, ["删除文件路径", "保留文件路径", "SHA256", "删除原因", "删除时间", "是否确认重复"])


def workspace_map_text() -> str:
    return """# Workspace Map

## Primary Human Entry

- `outputs/工作包/`: all substantive task run packages, named `YYYYMMDD_HHMM_中文任务名`.
- `outputs/_index/`: run index, run manifest, latest canonical outputs, duplicate deletion log.
- `outputs/_待复核/`: unique files that could not be assigned automatically.

## Standard Directories

- `data/01_raw/`: immutable raw data.
- `data/03_primary/`: current canonical cleaned main tables.
- `data/04_feature/`: pipeline-required canonical feature tables.
- `reports/`: project-level latest summaries only; task reports belong in run packages.
- `experiments/`: project-level experiment index or canonical experiment outputs only.
- `project_state/`: current project memory, handoff, artifact index, and next step.
"""


def update_project_state() -> None:
    write_text(ROOT / "project_state/current_focus.md", f"# Current Focus\n\n当前已重构 workflow1 文件管理规则：以后以任务工作包 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/` 作为主要结果查看入口；标准目录只保留 canonical/latest 和 pipeline 必需文件。本次未重新跑数据、未清洗、未计算 MOE/EDI、未运行 DQN。\n\n长期规则：{LONG_RULE}\n")
    write_text(ROOT / "project_state/next_step.md", "# Next Step\n\n不要运行 DQN。下一步如继续 MOE/EDI 或 DQN prototype 参数准备，必须先创建新的任务工作包，然后补齐动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数。\n")
    write_text(ROOT / "project_state/conversation_handoff.md", f"# Conversation Handoff\n\n{NOW.strftime('%Y-%m-%d %H:%M')} 已完成 Run Package 文件管理机制重构。主入口为 `outputs/工作包/`，全局索引为 `outputs/_index/run_index.md` 和 `outputs/_index/run_manifest.csv`。本次没有重新跑数据、清洗、MOE/EDI 或 DQN，`data/01_raw` 未修改。\n\n长期规则：{LONG_RULE}\n")
    write_text(ROOT / "project_state/run_protocol.md", f"# Run Protocol\n\n- 新任务开始前先读取 `outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml`、`project_state/conversation_handoff.md` 和 `AGENTS.md`。\n- 每次实质性任务先创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。\n- 所有新产物优先进入任务工作包；后续 pipeline 必需文件再复制到标准 canonical 目录。\n- 不得修改、删除、重命名或移动 `data/01_raw` 原始数据。\n- {LONG_RULE}\n")
    append = {
        "changelog.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')}\n\n- 建立 Run Package First 文件管理机制，主入口改为 `outputs/工作包/`。\n- 补建历史任务工作包：PEANUT 数据清洗与风险底座、上游查验与浓度修复、BetaBinomial 信念更新、MOE/EDI 外部参数匹配、全工作目录整理与规范化。\n- 生成 `run_index.md`、`run_manifest.csv`、`latest_canonical_outputs.yaml` 和任务包 manifests。\n- 创建 `run-package-manager` skill 并更新相关 organizer/orchestrator skills。\n",
        "decision_log.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')}\n\n### Adopt Run Package First as primary file management rule\n\nRationale: 单靠 latest/archive 不能让用户一眼看出每一步任务做了什么、产物在哪里、哪些输入输出属于同一轮任务。\n\nImpact: {LONG_RULE}\n",
        "lessons_learned.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')}\n\n- `latest/archive` 适合机器可读和历史保底，但不适合做人类主入口；科研工作流更需要按“时间 + 工作内容”的任务包组织。\n- canonical 文件应保留在标准目录以保护 pipeline，任务包保存完整可读副本以保护可追溯性。\n",
        "project_memory.md": f"\n## {NOW.strftime('%Y-%m-%d %H:%M')} Run Package Memory\n\n- {LONG_RULE}\n- 新对话继续任务时，先读 `outputs/_index/run_index.md`、`outputs/_index/latest_canonical_outputs.yaml` 和 `project_state/conversation_handoff.md`。\n",
    }
    for name, text in append.items():
        with (ROOT / "project_state" / name).open("a", encoding="utf-8") as f:
            f.write(text)
    write_text(ROOT / "project_state/artifact_index.md", artifact_index_text())
    write_text(ROOT / "project_state/workspace_structure.md", workspace_map_text())


def artifact_index_text() -> str:
    lines = ["# Artifact Index\n\n## Latest Canonical Outputs\n\n"]
    for k, v in CANONICAL.items():
        lines.append(f"- `{k}`: `{v}`\n")
    lines.append("\n## Run Package Indexes\n\n- `outputs/_index/run_index.md`\n- `outputs/_index/run_manifest.csv`\n- `outputs/_index/latest_canonical_outputs.yaml`\n\n")
    lines.append("## Rule\n\n" + LONG_RULE + "\n")
    return "".join(lines)


def update_cli() -> None:
    run_package_py = ROOT / "src/workflow1/run_package.py"
    write_text(run_package_py, '''"""Lightweight run package helpers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import csv
import re

PACKAGE_SUBDIRS = [
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


def slug_name(name: str) -> str:
    text = re.sub(r"[\\\\/:*?\\\"<>|\\s]+", "_", name.strip())
    return text.strip("_") or "未命名任务"


def start_run(name: str, outputs_dir: str | Path = "outputs") -> dict:
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    package = Path(outputs_dir) / "工作包" / f"{stamp}_{slug_name(name)}"
    package.mkdir(parents=True, exist_ok=True)
    for sub in PACKAGE_SUBDIRS:
        (package / sub).mkdir(parents=True, exist_ok=True)
    (package / "00_输入说明" / "inputs.md").write_text("# 输入说明\\n\\n请记录本轮输入文件路径和摘要。\\n", encoding="utf-8")
    (package / "README.md").write_text(f"# {name}\\n\\n任务开始时间：{stamp}\\n\\n本目录为 workflow1 任务工作包。\\n", encoding="utf-8")
    manifest = package / "manifest.csv"
    if not manifest.exists():
        with manifest.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["文件路径", "文件类型", "文件说明", "是否关键输出", "是否canonical副本", "是否下游依赖", "生成时间"])
    return {"status": "ok", "package": package.as_posix(), "next_step": "Write all task outputs into this run package first."}


def list_runs(outputs_dir: str | Path = "outputs") -> dict:
    root = Path(outputs_dir) / "工作包"
    runs = []
    if root.exists():
        for p in sorted([x for x in root.iterdir() if x.is_dir()]):
            runs.append({"path": p.as_posix(), "has_readme": (p / "README.md").exists(), "has_manifest": (p / "manifest.csv").exists()})
    return {"status": "ok", "runs": runs, "count": len(runs)}


def finish_run(outputs_dir: str | Path = "outputs") -> dict:
    runs = list_runs(outputs_dir)["runs"]
    missing = [r for r in runs if not r["has_readme"] or not r["has_manifest"]]
    return {"status": "ok" if not missing else "needs_review", "missing": missing, "next_step": "Update outputs/_index/run_manifest.csv and run whole workspace organization check."}
''')
    cli = ROOT / "src/workflow1/cli.py"
    text = cli.read_text(encoding="utf-8")
    if '"start-run"' not in text:
        text = text.replace('"orchestration",\n    }', '"orchestration",\n        "start-run",\n        "finish-run",\n        "list-runs",\n    }')
        insert = '''    if stage == "start-run":
        from workflow1.run_package import start_run

        return PipelineResult(name=stage, status="ok", details=start_run(os.environ.get("WORKFLOW1_RUN_NAME", "未命名任务")))
    if stage == "finish-run":
        from workflow1.run_package import finish_run

        return PipelineResult(name=stage, status="ok", details=finish_run())
    if stage == "list-runs":
        from workflow1.run_package import list_runs

        return PipelineResult(name=stage, status="ok", details=list_runs())
'''
        text = text.replace('    if stage == "intake":\n', insert + '    if stage == "intake":\n')
        parser_add = '''    parser.add_argument(
        "--name",
        default=None,
        help="Run package name for --stage start-run.",
    )
'''
        text = text.replace('    parser.add_argument(\n        "--reports-dir",', parser_add + '    parser.add_argument(\n        "--reports-dir",')
        text = text.replace('    summary = run(stage=args.stage, config_path=args.config, raw_dir=args.raw_dir, reports_dir=args.reports_dir)', '    if args.name:\n        os.environ["WORKFLOW1_RUN_NAME"] = args.name\n    summary = run(stage=args.stage, config_path=args.config, raw_dir=args.raw_dir, reports_dir=args.reports_dir)')
        cli.write_text(text, encoding="utf-8")


def create_report(run_rows: list[dict]) -> None:
    report = f"""# 工作流任务包机制重构报告

## 1. 为什么原来的 latest/archive 不够

`latest/` 方便机器和人快速找到当前最新文件，`archive/` 适合保存历史或不确定文件，但它们不能自然表达“一轮任务用了哪些输入、产生了哪些输出、报告和日志在哪里”。用户查看时需要按时间和任务内容理解整个科研过程，因此需要 Run Package 作为主入口。

## 2. 新的任务工作包机制

以后每次实质性任务开始前创建 `outputs/工作包/YYYYMMDD_HHMM_中文任务名/`。任务产物优先进入该工作包，并按输入说明、数据、表格、图表、报告、模型、配置、日志、代码快照分类保存。标准目录只保留 canonical/latest 和 pipeline 必需文件。

## 3. 以后每次任务会生成什么目录

```text
outputs/工作包/YYYYMMDD_HHMM_中文任务名/
├─ README.md
├─ 00_输入说明/
├─ 01_数据输出/
├─ 02_表格输出/
├─ 03_图表输出/
├─ 04_报告输出/
├─ 05_模型与实验/
├─ 06_配置参数/
├─ 07_日志与错误/
├─ 08_代码快照/
└─ manifest.csv
```

## 4. 这次如何重组已有文件

已补建 5 个历史任务工作包，并创建本次机制重构工作包：

{chr(10).join('- `' + row['任务包路径'] + '`' for row in run_rows)}

## 5. 哪些文件被移动

旧的顶层 `outputs/20260424_*` 目录已复制进入对应工作包后，移动到 `archive/legacy_outputs_after_run_package_restructure/`，避免 outputs 根目录继续混杂。根目录未知唯一文件若出现，会进入 `outputs/_待复核/`。

详细记录见 `02_表格输出/reorganized_files_log.csv`。

## 6. 哪些重复文件被删除

本轮仅允许删除临时缓存、锁文件、空临时文件等安全对象。删除记录见 `outputs/_index/deleted_duplicates_log.csv` 和本工作包 `02_表格输出/deleted_duplicates_log.csv`。

## 7. 哪些唯一文件进入 `_待复核`

本轮未发现需要移动到 `_待复核` 的根目录唯一文件。若后续发现无法归属但唯一的文件，将进入 `outputs/_待复核/YYYYMMDD_未归类唯一文件/`。

## 8. canonical 文件保留在标准目录

以下 canonical 文件仍保留在标准目录，保护后续 pipeline：

{chr(10).join('- `' + v + '`' for v in CANONICAL.values())}

## 9. 后续如何查看每一步结果

打开 `outputs/工作包/`，按 `YYYYMMDD_HHMM_中文任务名` 查看每一步；打开 `outputs/_index/run_index.md` 可查看任务包总索引；每个任务包内的 `README.md` 和 `manifest.csv` 说明该轮输入、输出和关键文件。

## 10. 是否适合继续 MOE/EDI、DQN prototype 和论文输出

适合继续。MOE/EDI 和 belief-MDP/DQN prototype 后续任务都应先创建新的任务工作包。当前仍不应直接运行 DQN，需先补齐动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数。
"""
    report_path = CURRENT_PACKAGE / "04_报告输出" / "workflow_run_package_restructure_report.md"
    write_text(report_path, report)
    write_text(ROOT / "reports/latest/workflow_run_package_restructure_report.md", report)


def run_checks() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    checks = []
    for cmd in [
        [sys.executable, "-m", "workflow1", "--stage", "list-runs"],
        [sys.executable, "-m", "workflow1", "--stage", "finish-run"],
    ]:
        cp = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, timeout=60)
        checks.append({"command": " ".join(cmd), "returncode": cp.returncode, "stdout": cp.stdout.strip(), "stderr": cp.stderr.strip()})
    write_text(CURRENT_PACKAGE / "07_日志与错误" / "cli_stub_check_log.json", json.dumps(checks, ensure_ascii=False, indent=2))


def main() -> None:
    setup_dirs()
    update_agents_and_skills()
    update_cli()
    current_spec = current_package_outputs()
    run_rows = build_historical_packages()
    find_unclassified_unique()
    safe_deduplicate()
    # Write current logs before manifest.
    write_csv(CURRENT_PACKAGE / "02_表格输出" / "reorganized_files_log.csv", reorganized, ["源文件路径", "目标文件路径", "操作", "说明", "是否canonical副本", "时间"])
    write_csv(CURRENT_PACKAGE / "02_表格输出" / "deleted_duplicates_log.csv", deleted_duplicates, ["删除文件路径", "保留文件路径", "SHA256", "删除原因", "删除时间", "是否确认重复"])
    write_csv(CURRENT_PACKAGE / "02_表格输出" / "unclassified_unique_files_log.csv", unclassified, ["源文件路径", "目标文件路径", "原因", "时间"])
    current_manifest = package_manifest(CURRENT_PACKAGE)
    create_package_readme(CURRENT_PACKAGE, current_spec, current_manifest)
    run_rows.append(run_row(CURRENT_PACKAGE, current_spec, current_manifest))
    create_report(run_rows)
    current_manifest = package_manifest(CURRENT_PACKAGE)
    create_package_readme(CURRENT_PACKAGE, current_spec, current_manifest)
    run_rows[-1] = run_row(CURRENT_PACKAGE, current_spec, current_manifest)
    write_indexes(run_rows)
    update_project_state()
    run_checks()
    safe_deduplicate()
    write_csv(CURRENT_PACKAGE / "02_表格输出" / "deleted_duplicates_log.csv", deleted_duplicates, ["删除文件路径", "保留文件路径", "SHA256", "删除原因", "删除时间", "是否确认重复"])
    write_csv(INDEX_DIR / "deleted_duplicates_log.csv", deleted_duplicates, ["删除文件路径", "保留文件路径", "SHA256", "删除原因", "删除时间", "是否确认重复"])
    # Refresh current manifest after check log.
    package_manifest(CURRENT_PACKAGE)
    print(json.dumps({
        "current_package": rel(CURRENT_PACKAGE),
        "run_packages": len(run_rows),
        "reorganized_records": len(reorganized),
        "deleted_duplicates": len(deleted_duplicates),
        "unclassified_unique": len(unclassified),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
