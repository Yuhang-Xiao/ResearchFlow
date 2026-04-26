from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_DATE = date.today().strftime("%Y%m%d")
TASK_NAME = "全工作目录整理与规范化"
OUT_DIR = ROOT / "outputs" / f"{RUN_DATE}_{TASK_NAME}"
LONG_RULE = "后续任何任务完成后，必须执行全工作目录整理检查，而不是只整理 reports 或 data。所有任务输出必须进入 `outputs/YYYYMMDD_中文任务名/`，标准目录只保留 canonical/latest 和 pipeline 必需文件。"

STANDARD_DIRS = [
    ".codex",
    ".agents/skills",
    "skills",
    "src/workflow1",
    "prompts",
    "references/data_cleaning",
    "references/modeling",
    "references/visualization",
    "references/literature",
    "references/standards",
    "references/notes",
    "references/project_plan",
    "references/processed_summaries",
    "references/archive/unsorted",
    "data/01_raw",
    "data/02_intermediate/archive",
    "data/03_primary/archive",
    "data/04_feature/latest",
    "data/04_feature/archive",
    "data/05_model_input",
    "data/05_model_input/archive",
    "data/99_archive",
    "reports/latest",
    "reports/tables/latest",
    "reports/tables/archive",
    "reports/figures/latest",
    "reports/figures/archive/unsorted",
    "reports/archive",
    "experiments/baselines",
    "experiments/advanced",
    "experiments/comparisons",
    "experiments/optimization",
    "experiments/archive",
    "outputs/_index",
    "outputs/archive/unsorted_root_files",
    "project_state/archive",
]

OUT_SUBDIRS = ["data", "reports", "tables", "figures", "logs", "configs", "manifests", "archive"]

CANONICAL_FEATURES = [
    "peanut_count_panel.csv",
    "peanut_concentration_clean_table.csv",
    "peanut_concentration_distribution_summary.csv",
    "peanut_beta_binomial_belief_states.csv",
    "peanut_belief_mdp_state_features.csv",
    "peanut_belief_mdp_state_features_with_moe_edi.csv",
    "peanut_bmdl_parameter_config.json",
    "peanut_bmdl_parameter_table.csv",
    "peanut_consumption_parameter_table.csv",
    "peanut_population_parameter_table.csv",
    "peanut_edi_moe_risk_table.csv",
    "peanut_edi_moe_risk_summary.csv",
]

CANONICAL_PRIMARY = [
    "peanut_cleaned_analysis_ready.csv",
    "peanut_cleaned_analysis_ready.xlsx",
]

LATEST_REPORTS = [
    "peanut_cleaning_report.md",
    "peanut_concentration_cleaning_report.md",
    "peanut_upstream_verification_report.md",
    "peanut_upstream_repair_log.md",
    "peanut_beta_binomial_belief_update_report.md",
    "peanut_moe_edi_external_parameter_matching_report.md",
    "peanut_pre_dqn_readiness_after_moe_edi.md",
    "peanut_full_workflow_summary.md",
    "peanut_workflow_run_summary.json",
    "peanut_moe_edi_error_log.md",
]

LATEST_TABLES = [
    "peanut_belief_state_latest.csv",
    "peanut_belief_state_summary_by_stage.csv",
    "peanut_cleaning_issue_log.csv",
    "peanut_concentration_audit_findings.csv",
    "peanut_data_quality_summary.csv",
    "peanut_label_dictionary.csv",
    "peanut_risk_summary_by_category.csv",
    "peanut_risk_summary_by_region.csv",
    "peanut_risk_summary_by_stage.csv",
    "peanut_risk_summary_by_year.csv",
    "peanut_variable_dictionary.csv",
    "schema_inventory_PEANUT2023-20241.csv",
]

CORE_STATE = [
    "current_focus.md",
    "next_step.md",
    "changelog.md",
    "decision_log.md",
    "lessons_learned.md",
    "project_memory.md",
    "run_protocol.md",
    "conversation_handoff.md",
    "roadmap.yaml",
    "artifact_index.md",
    "workspace_structure.md",
]

log_rows: list[dict] = []


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def log(action: str, src: Path | str, dst: Path | str = "", note: str = "") -> None:
    log_rows.append(
        {
            "action": action,
            "source": str(src),
            "destination": str(dst),
            "note": note,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    log("ensure_dir", rel(path) if path.exists() else path.as_posix(), "", "")


def copy_file(src: Path, dst: Path, note: str = "") -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return
    shutil.copy2(src, dst)
    log("copy", rel(src), rel(dst), note)


def move_file(src: Path, dst: Path, note: str = "") -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        stem, suffix = dst.stem, dst.suffix
        dst = dst.with_name(f"{stem}_{RUN_DATE}_{int(datetime.now().timestamp())}{suffix}")
    shutil.move(str(src), str(dst))
    log("move", rel(src), rel(dst), note)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    log("write", rel(path), "", "")


def classify_file(path: Path) -> dict:
    r = rel(path)
    name = path.name
    ext = path.suffix.lower()
    parts = r.split("/")
    top = parts[0] if parts else ""
    file_type = {
        ".csv": "table",
        ".xlsx": "spreadsheet",
        ".xls": "spreadsheet",
        ".md": "markdown",
        ".json": "config_or_json",
        ".yaml": "config",
        ".yml": "config",
        ".py": "python_code",
        ".svg": "figure",
        ".png": "figure",
        ".jpg": "image",
        ".jpeg": "image",
        ".pdf": "pdf",
        ".docx": "document",
        ".txt": "text",
    }.get(ext, "other")
    is_raw = r.startswith("data/01_raw/")
    is_archive = "/archive/" in r or r.startswith("outputs/archive/") or r.startswith("data/99_archive/")
    is_temp = bool(re.search(r"(__pycache__|\\.pyc$|~\\$|\\.tmp$|\\.bak$|\\.log$|temp|tmp)", r, re.I))
    downstream_names = set(CANONICAL_FEATURES + CANONICAL_PRIMARY)
    downstream_names.update(["AGENTS.md", "START_HERE.md", "pyproject.toml", "requirements.txt"])
    is_downstream = name in downstream_names or r.startswith("src/") or r in [f"project_state/{x}" for x in CORE_STATE]
    is_latest = (
        name in downstream_names
        or "/latest/" in r
        or name in LATEST_REPORTS
        or name in LATEST_TABLES
    )
    is_history = is_archive or r.startswith("outputs/202") or (top == "reports" and name not in LATEST_REPORTS and ext in [".md", ".json"])
    if is_raw:
        category = "原始数据"
    elif top in [".agents", "skills"]:
        category = "技能/代理"
    elif top == "src":
        category = "源代码"
    elif top == "data":
        category = "数据产物"
    elif top == "reports":
        category = "报告/表格/图表"
    elif top == "outputs":
        category = "任务输出/索引"
    elif top == "references":
        category = "参考资料"
    elif top == "project_state":
        category = "项目状态"
    elif top == "experiments":
        category = "实验产物"
    elif top == "prompts":
        category = "提示词"
    else:
        category = "根目录/未归类"
    stat = path.stat()
    return {
        "文件路径": r,
        "文件名": name,
        "扩展名": ext,
        "所属目录": Path(r).parent.as_posix(),
        "文件大小": stat.st_size,
        "修改时间": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "文件类型": file_type,
        "初步分类": category,
        "是否可能是原始数据": is_raw,
        "是否可能是canonical_latest": is_latest,
        "是否可能是历史产物": is_history,
        "是否可能是临时文件": is_temp,
        "是否可能影响后续pipeline": is_downstream,
    }


def iter_files() -> list[Path]:
    skip_dirs = {".git", ".pytest_cache", "__pycache__"}
    files = []
    for p in ROOT.rglob("*"):
        if any(part in skip_dirs for part in p.parts):
            continue
        if p.is_file():
            files.append(p)
    return sorted(files, key=lambda x: rel(x))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    log("write", rel(path), "", f"{len(rows)} rows")


def markdown_table(rows: list[dict], cols: list[str], limit: int = 30) -> str:
    rows = rows[:limit]
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for row in rows:
        vals = [str(row.get(c, "")).replace("|", "\\|") for c in cols]
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out)


def create_readmes() -> None:
    readmes = {
        "README.md": "# workflow1\n\n通用科学工作流脚手架。当前项目包含 PEANUT/AFB1 风险监管 workflow 的清洗、belief state、MOE/EDI 原型输出。入口说明见 `START_HERE.md`，长期规则见 `AGENTS.md`。\n",
        "data/README.md": "# data\n\n- `01_raw/`：原始数据，不修改、不删除、不重命名。\n- `02_intermediate/`：中间产物。\n- `03_primary/`：清洗后的主分析数据。\n- `04_feature/`：特征、面板、belief states、MOE/EDI 风险表；`latest/` 保存最新副本，`archive/` 保存历史或重复产物。\n- `05_model_input/`：建模输入矩阵。\n- `99_archive/`：历史数据归档。\n",
        "data/01_raw/README.md": "# data/01_raw\n\n原始数据区。不得修改、删除、重命名或移动这里的原始文件。本目录仅允许增加 README、inventory 等非破坏性索引文件。\n",
        "data/02_intermediate/README.md": "# data/02_intermediate\n\n中间解析或轻度转换数据。历史中间结果放入 `archive/`。\n",
        "data/03_primary/README.md": "# data/03_primary\n\n主清洗分析数据。当前 canonical PEANUT 清洗表保留在本目录，历史版本放入 `archive/`。\n",
        "data/04_feature/README.md": "# data/04_feature\n\n特征与风险度量数据。pipeline 依赖的 canonical 文件保留在本目录，同时复制到 `latest/`；历史、重复或不确定版本进入 `archive/`。\n",
        "data/05_model_input/README.md": "# data/05_model_input\n\n最终模型输入矩阵或切分数据。本次未运行模型。\n",
        "reports/README.md": "# reports\n\n报告根目录保留当前流程必要报告；`latest/` 保存最新关键报告副本，`archive/` 保存历史报告，`tables/` 和 `figures/` 分别保存表格与图表。\n",
        "experiments/README.md": "# experiments\n\n实验输出目录。`baselines/`、`advanced/`、`comparisons/`、`optimization/` 分别保存不同类型实验；旧实验进入 `archive/`。本次整理不运行模型。\n",
        "outputs/README.md": "# outputs\n\n每个实质性任务必须创建 `outputs/YYYYMMDD_中文任务名/` 独立输出目录。全局索引位于 `_index/`。\n",
        "references/README.md": "# references\n\n项目参考资料目录。文献 PDF 放 `literature/`，标准法规放 `standards/`，研究计划和笔记放 `notes/` 或 `project_plan/`，清洗/建模/可视化方法分别放入对应目录，处理后摘要放 `processed_summaries/`。\n",
        "references/processed_summaries/README.md": "# processed_summaries\n\n存放已阅读参考资料的可复用中文摘要、方法要点和后续 workflow 指引。\n",
        "outputs/_index/README.md": "# outputs/_index\n\n全项目任务输出索引、manifest、latest 输出映射和目录结构说明。\n",
        "reports/tables/README.md": "# reports/tables\n\n报告附表目录。当前关键附表复制到 `latest/`，历史或不确定附表进入 `archive/`。\n",
        "reports/figures/README.md": "# reports/figures\n\n图表目录。当前关键图表复制到 `latest/`，历史或不确定图表进入 `archive/`。\n",
        "reports/latest/README.md": "# reports/latest\n\n当前最新关键报告副本，便于快速查找；原 pipeline 所需文件若仍在原路径，应继续保留。\n",
        "outputs/archive/README.md": "# outputs/archive\n\n不确定、历史、缓存或无法归入具体任务目录的文件归档区。不在此处删除文件。\n",
        "experiments/optimization/README.md": "# experiments/optimization\n\nPOMDP、belief-MDP、DQN 或其他优化实验输出目录。本次整理未运行模型。\n",
        "references/literature/README.md": "# references/literature\n\n文献 PDF、论文资料和可引用来源。\n",
        "references/standards/README.md": "# references/standards\n\n食品安全标准、法规、限量依据和分类依据。\n",
        "references/notes/README.md": "# references/notes\n\n研究计划、会议记录、用户提供说明和无法归入文献/标准的参考材料。\n",
        "references/data_cleaning/README.md": "# references/data_cleaning\n\n数据清洗、字段解释、匹配规则和质量控制方法参考。\n",
        "references/modeling/README.md": "# references/modeling\n\n建模、风险评估、优化、MDP/DQN/POMDP 方法参考。\n",
        "references/visualization/README.md": "# references/visualization\n\n可视化模板、图表规范和展示方案参考。\n",
    }
    for rp, text in readmes.items():
        p = ROOT / rp
        if not p.exists() or rp in ["outputs/README.md", "references/README.md", "data/README.md", "reports/README.md", "experiments/README.md"]:
            write_text(p, text)


def organize_root() -> None:
    allowed_files = {"AGENTS.md", "START_HERE.md", "README.md", "pyproject.toml", "requirements.txt"}
    allowed_dirs = {".codex", ".agents", ".git", "skills", "src", "data", "reports", "experiments", "outputs", "references", "project_state", "prompts", "scripts"}
    for child in ROOT.iterdir():
        if child.name in allowed_files or child.name in allowed_dirs:
            continue
        if child.is_file():
            # Root document/report files are reference material unless clearly temporary.
            if child.suffix.lower() in [".docx", ".pdf", ".md"]:
                move_file(child, ROOT / "references" / "notes" / child.name, "root scattered document moved to references/notes")
            else:
                move_file(child, ROOT / "outputs" / "archive" / "unsorted_root_files" / child.name, "uncertain root file archived")


def organize_data() -> None:
    for name in CANONICAL_PRIMARY:
        src = ROOT / "data" / "03_primary" / name
        if src.exists():
            copy_file(src, ROOT / "data" / "03_primary" / "latest" / name, "canonical primary latest copy")
    for name in CANONICAL_FEATURES:
        src = ROOT / "data" / "04_feature" / name
        if src.exists():
            copy_file(src, ROOT / "data" / "04_feature" / "latest" / name, "canonical feature latest copy")
    # Archive duplicate spreadsheet feature mirrors while keeping CSV canonical files untouched.
    for p in (ROOT / "data" / "04_feature").glob("*.xlsx"):
        if p.name.replace(".xlsx", ".csv") in CANONICAL_FEATURES:
            move_file(p, ROOT / "data" / "04_feature" / "archive" / p.name, "xlsx duplicate of canonical CSV archived")
    raw_rows = [classify_file(p) for p in (ROOT / "data" / "01_raw").rglob("*") if p.is_file()]
    write_csv(ROOT / "data" / "01_raw" / "raw_data_inventory.csv", raw_rows)
    copy_file(ROOT / "data" / "01_raw" / "raw_data_inventory.csv", OUT_DIR / "tables" / "raw_data_inventory.csv", "raw inventory synced to task output")


def organize_reports() -> None:
    archive_dir = ROOT / "reports" / "archive" / f"{RUN_DATE}_整理前历史报告"
    for name in LATEST_REPORTS:
        src = ROOT / "reports" / name
        if src.exists():
            copy_file(src, ROOT / "reports" / "latest" / name, "latest report copy")
    for p in (ROOT / "reports").glob("*"):
        if p.name == "README.md":
            continue
        if p.is_file() and p.suffix.lower() in [".md", ".json"] and p.name not in LATEST_REPORTS:
            move_file(p, archive_dir / p.name, "historical root report archived")
    for name in LATEST_TABLES:
        src = ROOT / "reports" / "tables" / name
        if src.exists():
            copy_file(src, ROOT / "reports" / "tables" / "latest" / name, "latest report table copy")
    for p in (ROOT / "reports" / "figures").glob("*"):
        if p.is_file():
            copy_file(p, ROOT / "reports" / "figures" / "latest" / p.name, "latest figure copy")


def organize_outputs() -> None:
    for task_dir in [p for p in (ROOT / "outputs").iterdir() if p.is_dir() and re.match(r"^\d{8}_", p.name)]:
        for sub in ["data", "reports", "tables", "figures", "logs", "configs"]:
            (task_dir / sub).mkdir(exist_ok=True)
        readme = task_dir / "README.md"
        if not readme.exists():
            write_text(readme, f"# {task_dir.name}\n\n自动补充的任务目录 README。请查看各子目录中的数据、报告、表格、图表、日志和配置。\n")


def organize_references() -> None:
    # Keep existing references in place unless they are root-level documents with clear extension.
    rows = [classify_file(p) for p in (ROOT / "references").rglob("*") if p.is_file()]
    write_csv(ROOT / "references" / "reference_inventory.csv", rows)
    copy_file(ROOT / "references" / "reference_inventory.csv", OUT_DIR / "tables" / "reference_inventory.csv", "reference inventory synced")


def skill_metadata(path: Path) -> tuple[str, str, bool]:
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    name = ""
    desc = ""
    has_front = text.startswith("---")
    if has_front:
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if line.strip().startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                if line.strip().startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
    return name, desc, bool(name and desc)


def ensure_skill(path: Path, name: str, desc: str, body: str) -> None:
    text = f"---\nname: {name}\ndescription: {desc}\n---\n\n{body.strip()}\n"
    write_text(path, text)


def organize_skills() -> None:
    body = f"""# Whole Workspace Organizer

## When To Trigger

Use after every substantive workflow task and whenever the user asks to organize, archive, index, or normalize the whole workspace.

## Scan Scope

Scan the whole repository: root, `.agents/`, `.codex/`, `skills/`, `src/`, `data/`, `reports/`, `experiments/`, `outputs/`, `references/`, `project_state/`, and `prompts/`.

## Classification

- Raw data: files under `data/01_raw/`; never modify, rename, delete, or move.
- Canonical latest: pipeline-required files in standard directories and copies under `latest/`.
- Historical artifacts: old reports, duplicate exports, previous task outputs, and superseded figures/tables.
- Temporary files: cache, pyc, tmp, bak, editor leftovers, or test scratch outputs.
- References: literature, standards, notes, plans, processed summaries.
- Code/state: `src/`, skills, prompts, and `project_state/` files.

## Organization Rules

1. Create `outputs/YYYYMMDD_中文任务名/` with data, reports, tables, figures, logs, configs, manifests, and archive.
2. Keep pipeline-required canonical files at their expected paths; copy them into `latest/` rather than moving them.
3. Move historical or uncertain files to the nearest `archive/` or `archive/unsorted/`.
4. Do not delete files during organization.
5. Do not modify `data/01_raw` except README and inventory sidecar files.
6. Generate workspace inventory, raw/reference/skill/source inventories, output manifest, latest output YAML, and workspace structure files.
7. After organization, update `project_state/artifact_index.md` and `project_state/workspace_structure.md`.

## End-Of-Task Check

{LONG_RULE}
"""
    for base in [ROOT / ".agents" / "skills", ROOT / "skills"]:
        ensure_skill(base / "whole-workspace-organizer" / "SKILL.md", "whole-workspace-organizer", "Organize the entire workflow1 workspace, preserve pipeline-required latest artifacts, archive uncertain files, and update whole-project indexes after substantive tasks.", body)

    # Add minimal compatibility organizer skill if missing.
    artifact_body = f"""# Artifact Organizer

Use for organizing task artifacts. For workflow1, this skill must delegate to or run the whole-workspace organization check after every substantive task.

Required long-term rule: {LONG_RULE}
"""
    for base in [ROOT / ".agents" / "skills", ROOT / "skills"]:
        p = base / "artifact-organizer" / "SKILL.md"
        if not p.exists():
            ensure_skill(p, "artifact-organizer", "Organize task artifacts and trigger whole-workspace organization checks in workflow1.", artifact_body)
        else:
            text = p.read_text(encoding="utf-8", errors="replace")
            if "whole-workspace" not in text and "全工作目录整理" not in text:
                p.write_text(text.rstrip() + "\n\n## Whole Workspace Requirement\n\n" + LONG_RULE + "\n", encoding="utf-8")
                log("update", rel(p), "", "added whole workspace requirement")

    for p in [
        ROOT / ".agents" / "skills" / "goal-driven-research-orchestrator" / "SKILL.md",
        ROOT / "skills" / "goal-driven-research-orchestrator" / "SKILL.md",
    ]:
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="replace")
            if "whole-workspace-organizer" not in text:
                p.write_text(text.rstrip() + "\n\n## End-of-Task Organization\n\nAfter every substantive task, call `whole-workspace-organizer` or perform a whole workspace organization check. " + LONG_RULE + "\n", encoding="utf-8")
                log("update", rel(p), "", "added whole workspace organizer handoff")

    rows = []
    for base in [ROOT / ".agents" / "skills", ROOT / "skills"]:
        for skill_dir in sorted([p for p in base.iterdir() if p.is_dir()]):
            sk = skill_dir / "SKILL.md"
            name, desc, complete = skill_metadata(sk)
            counterpart = (ROOT / ("skills" if ".agents" in base.parts else ".agents/skills") / skill_dir.name / "SKILL.md")
            rows.append({
                "skill_dir": rel(skill_dir),
                "skill_name": name or skill_dir.name,
                "description": desc,
                "has_skill_md": sk.exists(),
                "has_name_and_description": complete,
                "counterpart_exists": counterpart.exists(),
                "canonical_note": "repo scoped .agents/skills preferred; skills/ kept for compatibility",
            })
    inv_md = "# Skills Inventory\n\n" + markdown_table(rows, ["skill_dir", "skill_name", "has_skill_md", "has_name_and_description", "counterpart_exists"], limit=200) + "\n"
    write_text(ROOT / "skills" / "skills_inventory.md", inv_md)
    write_text(ROOT / ".agents" / "skills" / "skills_inventory.md", inv_md)
    write_text(OUT_DIR / "reports" / "skills_inventory.md", inv_md)
    write_csv(OUT_DIR / "tables" / "skills_inventory.csv", rows)


def source_inventory() -> None:
    rows = [classify_file(p) for p in (ROOT / "src").rglob("*") if p.is_file()]
    md = "# Source Code Inventory\n\n" + markdown_table(rows, ["文件路径", "文件类型", "文件大小", "修改时间", "是否可能影响后续pipeline"], limit=200) + "\n"
    write_text(OUT_DIR / "reports" / "source_code_inventory.md", md)


def run_checks() -> list[dict]:
    checks = []
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    for cmd in [
        [sys.executable, "-c", "import workflow1; print(workflow1.__version__)"],
        [sys.executable, "-m", "workflow1", "--stage", "launch"],
    ]:
        try:
            cp = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
            checks.append({
                "command": " ".join(cmd),
                "returncode": cp.returncode,
                "stdout": cp.stdout.strip(),
                "stderr": cp.stderr.strip(),
            })
        except Exception as exc:
            checks.append({"command": " ".join(cmd), "returncode": -1, "stdout": "", "stderr": repr(exc)})
    write_text(OUT_DIR / "logs" / "source_check_log.json", json.dumps(checks, ensure_ascii=False, indent=2))
    return checks


def organize_caches() -> None:
    cache_root = ROOT / "outputs" / "archive" / f"cache_{RUN_DATE}"
    for p in sorted(ROOT.rglob("__pycache__"), key=lambda x: len(x.parts), reverse=True):
        if not p.is_dir() or "outputs" in p.parts:
            continue
        dst = cache_root / rel(p)
        if dst.exists():
            shutil.rmtree(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dst))
        log("move", rel(p), rel(dst), "python cache archived")
    pytest_cache = ROOT / ".pytest_cache"
    if pytest_cache.exists():
        dst = cache_root / ".pytest_cache"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(pytest_cache), str(dst))
        log("move", ".pytest_cache", rel(dst), "pytest cache archived")


def output_indexes(inventory_rows: list[dict]) -> None:
    manifest_rows = []
    for row in inventory_rows:
        path = row["文件路径"]
        name = row["文件名"]
        if path.startswith("outputs/") or row["是否可能是canonical_latest"] or row["是否可能影响后续pipeline"]:
            task = ""
            m = re.match(r"outputs/([^/]+)/", path)
            if m:
                task = m.group(1)
            manifest_rows.append({
                "文件路径": path,
                "文件名": name,
                "文件类型": row["文件类型"],
                "所属模块": row["初步分类"],
                "所属任务": task,
                "是否原始数据": row["是否可能是原始数据"],
                "是否canonical_latest": row["是否可能是canonical_latest"],
                "是否历史归档": row["是否可能是历史产物"],
                "是否下游依赖": row["是否可能影响后续pipeline"],
                "修改日期": row["修改时间"],
                "文件大小": row["文件大小"],
                "简要说明": describe_artifact(path, name),
            })
    write_csv(ROOT / "outputs" / "_index" / "output_manifest.csv", manifest_rows)
    copy_file(ROOT / "outputs" / "_index" / "output_manifest.csv", OUT_DIR / "manifests" / "output_manifest.csv", "manifest synced")

    latest = {
        "raw_peanut_data": "data/01_raw/PEANUT2023-20241.xlsx",
        "cleaned_dataset": "data/03_primary/peanut_cleaned_analysis_ready.csv",
        "count_panel": "data/04_feature/peanut_count_panel.csv",
        "concentration_table": "data/04_feature/peanut_concentration_clean_table.csv",
        "concentration_distribution_summary": "data/04_feature/peanut_concentration_distribution_summary.csv",
        "beta_binomial_states": "data/04_feature/peanut_beta_binomial_belief_states.csv",
        "belief_mdp_features": "data/04_feature/peanut_belief_mdp_state_features.csv",
        "belief_mdp_features_with_moe_edi": "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv",
        "consumption_parameter_table": "data/04_feature/peanut_consumption_parameter_table.csv",
        "population_parameter_table": "data/04_feature/peanut_population_parameter_table.csv",
        "edi_moe_risk_table": "data/04_feature/peanut_edi_moe_risk_table.csv",
        "latest_pre_dqn_readiness_report": "reports/latest/peanut_pre_dqn_readiness_after_moe_edi.md",
        "latest_moe_edi_report": "reports/latest/peanut_moe_edi_external_parameter_matching_report.md",
        "latest_handoff": "project_state/conversation_handoff.md",
        "latest_artifact_manifest": "outputs/_index/output_manifest.csv",
    }
    yaml_text = "\n".join([f"{k}: {v}" for k, v in latest.items()]) + "\n"
    write_text(ROOT / "outputs" / "_index" / "latest_outputs.yaml", yaml_text)
    copy_file(ROOT / "outputs" / "_index" / "latest_outputs.yaml", OUT_DIR / "manifests" / "latest_outputs.yaml", "latest outputs synced")

    index_md = "# Output Index\n\n## Latest Outputs\n\n" + "\n".join([f"- `{k}`: `{v}`" for k, v in latest.items()]) + "\n\n## Task Directories\n\n"
    for d in sorted([p for p in (ROOT / "outputs").iterdir() if p.is_dir() and p.name not in ["_index", "archive"]]):
        index_md += f"- `{rel(d)}`\n"
    write_text(ROOT / "outputs" / "_index" / "output_index.md", index_md)


def describe_artifact(path: str, name: str) -> str:
    mapping = {
        "peanut_concentration_clean_table.csv": "AFB1 浓度清洗 canonical 表",
        "peanut_count_panel.csv": "省份-年月-环节计数面板",
        "peanut_beta_binomial_belief_states.csv": "Beta-Binomial belief state 表",
        "peanut_belief_mdp_state_features.csv": "belief-MDP 状态特征",
        "peanut_belief_mdp_state_features_with_moe_edi.csv": "加入 MOE/EDI 的 belief-MDP 状态特征",
        "peanut_edi_moe_risk_table.csv": "EDI/MOE 风险明细",
        "peanut_moe_edi_external_parameter_matching_report.md": "MOE/EDI 外部参数匹配报告",
    }
    return mapping.get(name, "workspace artifact")


def workspace_structure() -> None:
    lines = ["# Workspace Structure\n"]
    for top in [".agents", ".codex", "skills", "src", "prompts", "references", "data", "reports", "experiments", "outputs", "project_state"]:
        p = ROOT / top
        if p.exists():
            lines.append(f"\n## `{top}/`\n")
            for child in sorted(p.iterdir(), key=lambda x: x.name):
                suffix = "/" if child.is_dir() else ""
                lines.append(f"- `{top}/{child.name}{suffix}`\n")
    text = "".join(lines)
    write_text(ROOT / "outputs" / "_index" / "workspace_structure.md", text)
    write_text(ROOT / "project_state" / "workspace_structure.md", text)
    copy_file(ROOT / "outputs" / "_index" / "workspace_structure.md", OUT_DIR / "manifests" / "workspace_structure.md", "workspace structure synced")


def update_agents() -> None:
    p = ROOT / "AGENTS.md"
    text = p.read_text(encoding="utf-8", errors="replace")
    header = "## Whole Workspace Organization Policy"
    block = f"""{header}

1. After every substantive task, Codex must run a whole workspace organization check.
2. The organization scope includes root, data, reports, outputs, references, experiments, src, skills, project_state, and prompts.
3. All task artifacts must go under `outputs/YYYYMMDD_中文任务名/`.
4. Standard directories should keep only canonical/latest or pipeline-required files.
5. Historical files must go into the corresponding archive.
6. Uncertain files go into archive/unsorted and must not be deleted.
7. `data/01_raw` must never be modified, deleted, renamed, or moved.
8. After every organization pass, update `outputs/_index/output_manifest.csv`, `outputs/_index/latest_outputs.yaml`, `project_state/artifact_index.md`, and `project_state/workspace_structure.md`.
9. Future tasks must not organize only local reports or data; they must run the whole workspace organization check.
10. If moving a file would break downstream workflow, keep a canonical latest copy at the pipeline-required path and update indexes.

"""
    if header not in text:
        marker = "## Project State Update Rules"
        text = text.replace(marker, block + marker)
        p.write_text(text, encoding="utf-8")
        log("update", "AGENTS.md", "", "added whole workspace organization policy")


def project_state_updates(checks: list[dict]) -> None:
    write_text(ROOT / "project_state" / "current_focus.md", f"# Current Focus\n\n当前已完成 workflow1 全工作目录整理与长期目录规范化。本次没有重新跑数据分析、清洗、MOE/EDI 或 DQN。后续重点是在保持目录整洁和索引更新的前提下，继续补齐 belief-MDP / DQN prototype 的动作、预算、成本、产能、约束参数。\n\n长期规则：{LONG_RULE}\n")
    write_text(ROOT / "project_state" / "next_step.md", "# Next Step\n\n不要运行 DQN。下一步先补齐或确认最小 belief-MDP / DQN prototype 所需动作空间、预算、产能、抽检成本、处置/召回损失、信息价值权重和约束参数；每次任务结束后执行全工作目录整理检查。\n")
    write_text(ROOT / "project_state" / "conversation_handoff.md", f"# Conversation Handoff\n\n{RUN_DATE} 已完成全工作目录整理与规范化。任务目录：`{rel(OUT_DIR)}/`。已生成 workspace inventory、output manifest、latest outputs、workspace structure、artifact index、skills/source inventories 和整理报告。未重新跑数据分析、清洗、MOE/EDI 或 DQN。`data/01_raw` 未移动、未重命名、未删除。\n\n长期规则：{LONG_RULE}\n")
    write_text(ROOT / "project_state" / "run_protocol.md", f"# Run Protocol\n\n- 启动任何实质性科研任务前，读取 `AGENTS.md`、项目状态、相关 references、上游输出和最新 artifact index。\n- 不得修改 `data/01_raw`。\n- 下游 MOE/EDI、belief-MDP、POMDP 或 DQN 前必须核验上游输出。\n- {LONG_RULE}\n")
    append = {
        "changelog.md": f"\n## {RUN_DATE}\n\n- 完成全工作目录整理与规范化，创建 `{rel(OUT_DIR)}/`。\n- 补齐长期目录结构、README、latest/archive 子目录、全局 output manifest、latest outputs、workspace structure 和 artifact index。\n- 新增 `whole-workspace-organizer` skill，并更新 artifact/goal-driven organizer 规则。\n- 本次未重新跑数据分析、清洗、MOE/EDI 或 DQN，未移动 `data/01_raw` 原始数据。\n",
        "decision_log.md": f"\n## {RUN_DATE}\n\n### Adopt whole-workspace organization after substantive tasks\n\nRationale: 当前 workflow1 已包含原始数据、标准数据层、任务 outputs、报告、图表、技能、代码和项目状态；只整理局部目录会导致最新产物和历史产物混杂。\n\nImpact: {LONG_RULE}\n",
        "lessons_learned.md": f"\n## {RUN_DATE}\n\n- 全目录整理应保守执行：pipeline 依赖文件保留原路径，同时复制到 `latest/`；历史和不确定文件归档但不删除。\n- `data/01_raw` 只允许增加 README 和 inventory sidecar，不移动原始文件。\n- 全局索引比人工记忆更可靠，后续任务应优先读取 `outputs/_index/latest_outputs.yaml` 和 `project_state/artifact_index.md`。\n",
        "project_memory.md": f"\n## {RUN_DATE} Whole workspace organization memory\n\n- {LONG_RULE}\n- 当前 canonical PEANUT 文件保留在 `data/03_primary/`、`data/04_feature/` 和 `reports/latest/`，全局索引在 `outputs/_index/`。\n",
    }
    for name, text in append.items():
        p = ROOT / "project_state" / name
        with p.open("a", encoding="utf-8") as f:
            f.write(text)


def artifact_index(manifest_rows: list[dict]) -> None:
    latest_path = ROOT / "outputs" / "_index" / "latest_outputs.yaml"
    latest = latest_path.read_text(encoding="utf-8") if latest_path.exists() else ""
    text = "# Artifact Index\n\n## Latest Canonical Artifacts\n\n"
    for line in latest.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            text += f"- `{k.strip()}`: `{v.strip()}`\n"
    text += "\n## Manifest\n\n- `outputs/_index/output_manifest.csv`\n- `outputs/_index/output_index.md`\n- `outputs/_index/workspace_structure.md`\n\n"
    text += "## Notes\n\n" + LONG_RULE + "\n"
    write_text(ROOT / "project_state" / "artifact_index.md", text)


def organization_report(checks: list[dict]) -> None:
    moved = [r for r in log_rows if r["action"] == "move"]
    copied = [r for r in log_rows if r["action"] == "copy"]
    dirs = [r for r in log_rows if r["action"] == "ensure_dir"]
    archive_files = []
    for base in [
        ROOT / "reports" / "archive",
        ROOT / "data" / "04_feature" / "archive",
        ROOT / "outputs" / "archive",
        ROOT / "references" / "archive",
        ROOT / "project_state" / "archive",
    ]:
        if base.exists():
            archive_files.extend([p for p in base.rglob("*") if p.is_file()])
    archive_rows = [classify_file(p) for p in archive_files]
    write_csv(OUT_DIR / "tables" / "archive_manifest.csv", archive_rows)
    archive_lines = "\n".join(f"- `{rel(p)}`" for p in archive_files[:80]) if archive_files else "无。"
    report = f"""# 全工作目录整理与规范化报告

## 1. 整理前目录问题

- 根目录存在散落 `.docx` 文档。
- `reports/` 根目录堆积多个历史 Markdown/JSON 报告。
- `data/04_feature/` 同时存在 canonical CSV 与重复 XLSX 导出。
- `outputs/` 缺少统一 `_index` manifest、latest outputs 和 workspace structure。
- skills 在 `.agents/skills/` 与 `skills/` 间存在兼容副本，需要索引说明。

## 2. 整理范围

本次覆盖 root、`.agents/`、`.codex/`、`skills/`、`src/`、`data/`、`reports/`、`experiments/`、`outputs/`、`references/`、`project_state/`、`prompts/`。未重新跑数据分析、清洗、MOE/EDI 或 DQN。

## 3. 创建或补齐的目录

- 标准 data/reports/outputs/references/experiments latest 与 archive 目录。
- 本轮任务目录 `{rel(OUT_DIR)}/` 及其 data、reports、tables、figures、logs、configs、manifests、archive 子目录。
- `outputs/_index/` 全局索引目录。

## 4. 移动或复制了哪些文件

- 本次幂等整理运行中移动文件数：{len(moved)}
- 复制文件数：{len(copied)}
- 操作日志见 `{rel(OUT_DIR / 'logs' / 'organization_actions.csv')}`。
- 当前 archive manifest 记录文件数：{len(archive_files)}，见 `{rel(OUT_DIR / 'tables' / 'archive_manifest.csv')}`。

## 5. canonical latest 文件

canonical 数据文件保留在原 pipeline 路径，并复制到 `latest/`：

{chr(10).join('- `data/04_feature/' + n + '`' for n in CANONICAL_FEATURES)}

报告 latest 副本位于 `reports/latest/`。

## 6. archive 文件

- `data/04_feature/archive/`：重复 XLSX feature 导出。
- `reports/archive/{RUN_DATE}_整理前历史报告/`：历史 root 报告。
- `references/notes/`：根目录散落文档。
- 不确定 root 文件会进入 `outputs/archive/unsorted_root_files/`。

当前 archive 文件清单节选：

{archive_lines}

## 7. outputs 归档与索引

已生成：

- `outputs/_index/output_index.md`
- `outputs/_index/output_manifest.csv`
- `outputs/_index/latest_outputs.yaml`
- `outputs/_index/workspace_structure.md`

## 8. 仍然不确定的文件

本轮未删除任何文件。不确定归属的文件按 archive/unsorted 原则处理；当前主要需人工关注的是 `references/notes/` 中从根目录移入的 Word 总结文档是否应进一步归入 project_plan 或 literature。

## 9. 是否影响后续 pipeline

未移动 `data/01_raw` 原始数据。pipeline 依赖的 canonical 数据文件保留在原路径。轻量检查结果：

```json
{json.dumps(checks, ensure_ascii=False, indent=2)}
```

## 10. 是否适合继续 MOE/EDI、DQN prototype 和论文输出

适合继续 MOE/EDI 后续整理、belief-MDP 环境设计和 DQN prototype 参数补齐。正式 DQN 仍需动作空间、预算、产能、抽检成本、处置/召回损失和约束参数。

## 11. 后续保持整洁的方法

{LONG_RULE}
"""
    write_text(ROOT / "reports" / "latest" / "project_whole_workspace_organization_report.md", report)
    copy_file(ROOT / "reports" / "latest" / "project_whole_workspace_organization_report.md", OUT_DIR / "reports" / "project_whole_workspace_organization_report.md", "organization report synced")


def main() -> None:
    for d in OUT_SUBDIRS:
        ensure_dir(OUT_DIR / d)
    for d in STANDARD_DIRS:
        ensure_dir(ROOT / d)
    create_readmes()
    organize_root()
    organize_outputs()
    organize_data()
    organize_reports()
    organize_references()
    organize_skills()
    source_inventory()
    update_agents()
    files = iter_files()
    inventory_rows = [classify_file(p) for p in files]
    write_csv(OUT_DIR / "tables" / "workspace_inventory.csv", inventory_rows)
    inv_md = "# Workspace Inventory\n\n" + f"- 文件总数：{len(inventory_rows)}\n- 生成日期：{RUN_DATE}\n\n"
    inv_md += markdown_table(inventory_rows, ["文件路径", "文件类型", "初步分类", "是否可能是canonical_latest", "是否可能是历史产物", "是否可能影响后续pipeline"], limit=200)
    write_text(OUT_DIR / "reports" / "workspace_inventory.md", inv_md)
    output_indexes(inventory_rows)
    # Re-read manifest rows for artifact index.
    workspace_structure()
    checks = run_checks()
    organize_caches()
    project_state_updates(checks)
    artifact_index([])
    organization_report(checks)
    write_csv(OUT_DIR / "logs" / "organization_actions.csv", log_rows)
    readme = f"""# {TASK_NAME}

## 任务目的

整理整个 workflow1 工作目录，建立长期目录规范、latest/archive 副本、全局索引和整理后报告。本次不重新跑数据分析、清洗、MOE/EDI 或 DQN。

## 关键输出

- `reports/workspace_inventory.md`
- `tables/workspace_inventory.csv`
- `tables/raw_data_inventory.csv`
- `reports/source_code_inventory.md`
- `reports/skills_inventory.md`
- `reports/project_whole_workspace_organization_report.md`
- `manifests/output_manifest.csv`
- `manifests/latest_outputs.yaml`
- `manifests/workspace_structure.md`
- `logs/organization_actions.csv`

## 关键假设

- `data/01_raw` 原始文件不可移动、不可重命名、不可删除。
- pipeline 依赖 canonical 文件保留原路径，同时复制到 `latest/`。
- 不确定文件不删除，进入 archive/unsorted 或 notes。

## 下一步建议

继续补齐 belief-MDP / DQN prototype 所需动作空间、预算、产能、成本和约束参数；每次任务结束后执行全工作目录整理检查。
"""
    write_text(OUT_DIR / "README.md", readme)
    # Final refresh so inventories include reports/logs/README files created late in the run.
    final_inventory_rows = [classify_file(p) for p in iter_files()]
    write_csv(OUT_DIR / "tables" / "workspace_inventory.csv", final_inventory_rows)
    final_inv_md = "# Workspace Inventory\n\n" + f"- 文件总数：{len(final_inventory_rows)}\n- 生成日期：{RUN_DATE}\n\n"
    final_inv_md += markdown_table(final_inventory_rows, ["文件路径", "文件类型", "初步分类", "是否可能是canonical_latest", "是否可能是历史产物", "是否可能影响后续pipeline"], limit=200)
    write_text(OUT_DIR / "reports" / "workspace_inventory.md", final_inv_md)
    output_indexes(final_inventory_rows)
    workspace_structure()
    artifact_index([])
    write_csv(OUT_DIR / "logs" / "organization_actions.csv", log_rows)
    print(json.dumps({
        "out_dir": str(OUT_DIR),
        "files_indexed": len(final_inventory_rows),
        "moves": len([r for r in log_rows if r["action"] == "move"]),
        "copies": len([r for r in log_rows if r["action"] == "copy"]),
        "checks": checks,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
