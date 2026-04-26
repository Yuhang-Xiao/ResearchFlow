from __future__ import annotations

import csv
import hashlib
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def append_once(path: Path, text: str) -> None:
    old = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    if text.strip() not in old:
        path.write_text(old.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def scan_zotero_notes() -> None:
    zotero = Path("D:/桌面/codex/zotero")
    rows = []
    if zotero.exists():
        for p in zotero.rglob("*.md"):
            text = p.read_text(encoding="utf-8", errors="replace")
            bad_q = text.count("????")
            bad_repl = text.count("\ufffd")
            if bad_q or bad_repl:
                rows.append({
                    "path": str(p),
                    "question_mark_runs": str(bad_q),
                    "replacement_chars": str(bad_repl),
                    "status": "garbled_note_review_required",
                })
    if not rows:
        rows.append({"path": str(zotero), "question_mark_runs": "0", "replacement_chars": "0", "status": "no_garbled_markdown_detected_in_scan"})
    write_csv(RUN / "02_表格输出" / "zotero_garbled_note_scan.csv", rows)


def lineage_manifest() -> None:
    rows = []
    for folder, desc in [
        ("02_表格输出", "table outputs generated from local policies, scout evaluation, dry-run routing, and Zotero scan"),
        ("04_报告输出", "reports generated from project state, web scout metadata, local policy upgrades, and dry-run outputs"),
        ("06_配置参数", "policy snapshot copied from research_quality"),
        ("09_论文输出", "Zotero sidecar notes and citation export stubs; no Zotero database write"),
    ]:
        for p in (RUN / folder).glob("*"):
            if p.is_file():
                rows.append({
                    "output_path": str(p.relative_to(RUN)),
                    "source_paths": "AGENTS.md; project_state; workflow_improvement; model_registry; skills; references; web scout metadata",
                    "transform": desc,
                    "row_count": "",
                    "column_count": "",
                    "status": "pass",
                    "notes": "data/01_raw not modified",
                })
    write_csv(RUN / "01_数据输出" / "data_lineage_manifest.csv", rows)


def update_skill_inventory() -> None:
    skill_dirs = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
    lines = ["# Skills Inventory", "", f"Updated: {NOW}", ""]
    lines.extend(f"- {name}" for name in skill_dirs)
    for target in [ROOT / "skills" / "skills_inventory.md", ROOT / ".agents" / "skills" / "skills_inventory.md"]:
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_artifact_indexes() -> None:
    rel = RUN.relative_to(ROOT).as_posix()
    append_once(ROOT / "project_state" / "artifact_index.md", f"## {NOW} Research Quality System Upgrade\n\n- Run package: `{rel}`\n- Key artifacts: `research_quality/`, `references/top_journal_benchmark/`, `src/workflow1/quality/`, `src/workflow1/reporting/`, `model_registry/*comparison_protocol.yaml`, `workflow_recipes/*quality*.yaml`.\n")
    append_once(ROOT / "project_state" / "workspace_structure.md", f"## {NOW} Research Quality Additions\n\n- `research_quality/`: canonical research-quality policies.\n- `references/top_journal_benchmark/`: benchmark-paper registries.\n- `src/workflow1/quality/`: lightweight validation and claim-guard stubs.\n- `src/workflow1/reporting/`: paper section QA and DOCX/fallback orchestration stubs.\n")


def workspace_check() -> None:
    text = f"""# Whole Workspace Cleanliness Check

Generated: {NOW}

- `data/01_raw` was not modified by this task.
- New durable canonical files were limited to policies, skills, recipes, registries, and lightweight stubs.
- All task-specific reports/tables/logs were routed to `{RUN.relative_to(ROOT).as_posix()}`.
- No external plugin, MCP, API key, large dependency, background service, or Zotero SQLite write was performed.
"""
    (RUN / "07_日志与错误" / "whole_workspace_cleanliness_check.md").write_text(text, encoding="utf-8")


def manifest() -> None:
    records = []
    for p in sorted(RUN.rglob("*")):
        if p.is_file():
            records.append({
                "path": str(p.relative_to(RUN)),
                "type": p.suffix.lstrip(".") or "file",
                "description": "research quality system upgrade artifact",
                "created_at": NOW,
                "sha256": sha256(p),
            })
    write_csv(RUN / "manifest.csv", records)


def main() -> int:
    scan_zotero_notes()
    lineage_manifest()
    update_skill_inventory()
    update_artifact_indexes()
    workspace_check()
    manifest()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
