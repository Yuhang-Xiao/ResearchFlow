from __future__ import annotations

import csv
import hashlib
import os
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


PROTECTED_PREFIXES = [
    "data/01_raw",
    "references",
    "project_state",
    "research_quality",
    "model_registry",
    "workflow_recipes",
    "workflow_improvement",
    "skills",
    ".agents/skills",
    "src",
]

KNOWN_LATEST_OR_CANONICAL = {
    "outputs/工作包/20260426_1857_科研质量核验_顶级文献对标_工作流强化": "latest_run_package / research quality canonical context",
    "outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练": "latest DQN experimental run; needed as baseline for revised experiment",
    "outputs/工作包/20260426_1616_DQN文献增强建模方案与参数确认": "latest DQN literature/model-spec preparation",
    "data/03_primary/peanut_cleaned_analysis_ready.csv": "canonical cleaned PEANUT table",
    "data/03_primary/peanut_cleaned_analysis_ready.xlsx": "canonical cleaned PEANUT table",
    "data/04_feature/peanut_concentration_clean_table.csv": "canonical concentration clean table",
    "data/04_feature/peanut_count_panel.csv": "canonical count panel",
    "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv": "canonical belief-MDP/MOE-EDI state features",
    "experiments/optimization/peanut_dqn_auto_model.pt": "latest DQN experimental model artifact",
    "experiments/optimization/peanut_dqn_auto_policy.csv": "latest DQN experimental policy artifact",
    "experiments/optimization/peanut_dqn_auto_policy_comparison.csv": "latest DQN experimental comparison artifact",
    "experiments/optimization/peanut_dqn_auto_training_metrics.csv": "latest DQN experimental metrics artifact",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    if not path.is_file() or path.stat().st_size > 200 * 1024 * 1024:
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        rows = [{"note": "no rows"}]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, text: str) -> None:
    old = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    if text.strip() not in old:
        path.write_text(old.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def classify(path: Path) -> dict[str, str] | None:
    r = rel(path)
    name = path.name
    lower = name.lower()
    size = str(path.stat().st_size if path.is_file() else sum((f.stat().st_size for f in path.rglob("*") if f.is_file()), 0))
    mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    if r.startswith("data/01_raw"):
        return {
            "path": r,
            "type": "protected_raw_data",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "protect_do_not_delete",
            "risk_level": "blocked",
            "reason": "data/01_raw is immutable",
            "requires_user_confirmation": "not_deletable",
        }

    if r in KNOWN_LATEST_OR_CANONICAL:
        return {
            "path": r,
            "type": "active_or_canonical",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "skip_unless_user_explicitly_overrides",
            "risk_level": "high",
            "reason": KNOWN_LATEST_OR_CANONICAL[r],
            "requires_user_confirmation": "yes",
        }

    cache_markers = {"__pycache__", ".pytest_cache", ".ipynb_checkpoints"}
    if path.is_dir() and name in cache_markers:
        return {
            "path": r,
            "type": "cache_directory",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "recommended_delete",
            "risk_level": "low",
            "reason": "standard cache directory",
            "requires_user_confirmation": "yes_current_turn_no_delete",
        }

    if path.is_file() and (name.startswith("~$") or lower.endswith(".tmp") or lower.endswith(".temp")):
        return {
            "path": r,
            "type": "temporary_file",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "recommended_delete",
            "risk_level": "low",
            "reason": "temporary or Excel lock file",
            "requires_user_confirmation": "yes_current_turn_no_delete",
        }

    if path.is_file() and path.stat().st_size == 0 and any(part in r for part in ["outputs/", "reports/", "experiments/"]):
        return {
            "path": r,
            "type": "empty_output_file",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "recommended_delete",
            "risk_level": "low",
            "reason": "empty file under output/report/experiment area",
            "requires_user_confirmation": "yes_current_turn_no_delete",
        }

    if r.startswith("experiments/optimization/peanut_dqn_auto_"):
        return {
            "path": r,
            "type": "old_or_current_dqn_experimental_artifact",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "candidate_requires_explicit_selection",
            "risk_level": "medium",
            "reason": "DQN experimental artifact; latest revision should normally compare against it before deletion",
            "requires_user_confirmation": "yes",
        }

    if r.startswith("outputs/工作包/") and path.is_dir() and path != RUN:
        category = "historical_run_package"
        recommendation = "candidate_requires_explicit_selection"
        risk = "medium"
        reason = "historical run package; likely old output but may be unique provenance"
        if "DQN" in name or "科研质量核验" in name or "文献增强" in name:
            risk = "high"
            reason = "recent DQN/quality/literature package; needed for current continuation unless user explicitly deletes"
        return {
            "path": r,
            "type": category,
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": recommendation,
            "risk_level": risk,
            "reason": reason,
            "requires_user_confirmation": "yes",
        }

    if r.startswith("reports/项目级索引与摘要/") and path.is_file():
        return {
            "path": r,
            "type": "project_summary_report",
            "size_bytes": size,
            "last_write_time": mtime,
            "recommendation": "candidate_requires_explicit_selection",
            "risk_level": "medium",
            "reason": "project-level report may be superseded, but can carry unique summary context",
            "requires_user_confirmation": "yes",
        }

    return None


def find_candidates() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates: list[dict[str, str]] = []
    protected: list[dict[str, str]] = []

    # Cache and temp dirs/files across workspace.
    for p in ROOT.rglob("*"):
        if ".git" in p.parts:
            continue
        item = classify(p)
        if not item:
            continue
        if item["recommendation"].startswith("protect") or item["type"] == "active_or_canonical":
            protected.append(item)
        else:
            candidates.append(item)

    # Duplicate report/output files by hash, kept as review candidates only.
    by_hash: dict[str, list[Path]] = {}
    for base in ["reports", "experiments", "outputs/工作包"]:
        root = ROOT / base
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if f.is_file() and f.stat().st_size > 0 and f.stat().st_size < 50 * 1024 * 1024:
                h = sha256_file(f)
                if h:
                    by_hash.setdefault(h, []).append(f)
    for h, files in by_hash.items():
        if len(files) < 2:
            continue
        files_sorted = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
        keep = files_sorted[0]
        for dup in files_sorted[1:]:
            r = rel(dup)
            if r.startswith("data/01_raw"):
                continue
            candidates.append({
                "path": r,
                "type": "duplicate_by_sha256",
                "size_bytes": str(dup.stat().st_size),
                "last_write_time": datetime.fromtimestamp(dup.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "recommendation": "candidate_requires_explicit_selection",
                "risk_level": "medium",
                "reason": f"duplicate hash with newer/kept file {rel(keep)}; sha256={h}",
                "requires_user_confirmation": "yes",
            })

    # De-duplicate candidate rows by path/type/reason.
    seen = set()
    unique: list[dict[str, str]] = []
    for row in candidates:
        key = (row["path"], row["type"], row["reason"])
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique, protected


def write_outputs(candidates: list[dict[str, str]], protected: list[dict[str, str]]) -> None:
    recommended = [r for r in candidates if r["recommendation"] == "recommended_delete"]
    review = [r for r in candidates if r["recommendation"] != "recommended_delete"]
    write_csv(RUN / "02_表格输出" / "delete_candidates.csv", candidates)
    write_csv(RUN / "02_表格输出" / "recommended_delete_list.csv", recommended)
    write_csv(RUN / "02_表格输出" / "delete_candidates_review_required.csv", review)
    write_csv(RUN / "02_表格输出" / "protected_or_skipped_files.csv", protected)
    write_csv(RUN / "02_表格输出" / "located_current_assets.csv", [
        {
            "asset_type": "latest_dqn_experimental_run_package",
            "path": "outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练",
            "status": "protect_for_next_dqn_revision",
            "reason": "最新 DQN experimental run，修正版实验需要读取或对比",
        },
        {
            "asset_type": "latest_research_quality_upgrade_package",
            "path": "outputs/工作包/20260426_1857_科研质量核验_顶级文献对标_工作流强化",
            "status": "protect",
            "reason": "最新质量核验体系升级任务包",
        },
        {
            "asset_type": "latest_dqn_literature_modeling_package",
            "path": "outputs/工作包/20260426_1616_DQN文献增强建模方案与参数确认",
            "status": "protect_for_dqn_document_governance",
            "reason": "DQN 文献增强与参数确认依据",
        },
        {
            "asset_type": "canonical_peanut_cleaned_table",
            "path": "data/03_primary/peanut_cleaned_analysis_ready.csv",
            "status": "protect",
            "reason": "当前 canonical PEANUT 清洗表",
        },
        {
            "asset_type": "canonical_peanut_belief_moe_edi_features",
            "path": "data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv",
            "status": "protect",
            "reason": "当前 DQN/MOE/EDI 输入特征",
        },
        {
            "asset_type": "latest_dqn_experiment_standard_outputs",
            "path": "experiments/optimization/peanut_dqn_auto_*",
            "status": "candidate_only_after_user_confirmation",
            "reason": "最新 experimental DQN 输出；删除前应先完成修正版对比或确认不再需要",
        },
    ])
    write_csv(RUN / "02_表格输出" / "delete_plan.csv", [
        {
            "step": "1",
            "action": "scan_only",
            "status": "completed",
            "notes": "No files deleted. Waiting for user to select paths from delete_candidates.csv.",
        },
        {
            "step": "2",
            "action": "delete_selected_targets",
            "status": "pending_user_selection",
            "notes": "Will only run after explicit user confirmation.",
        },
        {
            "step": "3",
            "action": "update_indexes_then_continue_dqn",
            "status": "blocked_until_deletion_confirmation",
            "notes": "DQN revised experiment must wait until deletion/index update is complete.",
        },
    ])
    write_csv(RUN / "02_表格输出" / "deleted_files_log.csv", [
        {
            "path": "",
            "status": "no_delete_per_user_latest_instruction",
            "time": NOW,
            "notes": "User said: 先不要删除。Only scan candidates this turn.",
        }
    ])
    (RUN / "07_日志与错误" / "delete_error_log.md").write_text(
        "# Delete Error Log\n\n未执行删除；本轮仅扫描候选。未发现阻断性扫描错误。\n",
        encoding="utf-8",
    )
    top_recommended = "\n".join(f"- `{r['path']}`：{r['reason']} ({r['size_bytes']} bytes)" for r in recommended[:40]) or "- 暂无低风险推荐删除项。"
    top_review = "\n".join(f"- `{r['path']}`：{r['reason']} [{r['risk_level']}]" for r in review[:40]) or "- 暂无需复核候选。"
    report = f"""# 指定清理候选扫描报告

生成时间：{NOW}

## 本轮执行边界

- 已创建任务包：`{RUN.relative_to(ROOT).as_posix()}`
- 未删除任何文件。
- 未修改 `data/01_raw/`。
- 未继续 DQN 训练。
- DQN 修正版 experimental run 被阻塞，等待你从候选清单中指定实际删除目标后再继续。

## 候选统计

- 推荐删除的低风险缓存/临时项：{len(recommended)}
- 需要你明确选择的历史工作包、旧实验或重复产物：{len(review)}
- 已保护或跳过的 canonical / active 项：{len(protected)}

## 当前关键资产定位

- 最新 DQN experimental run：`outputs/工作包/20260426_1746_全流程验收与DQN自动参数训练`
- 最新科研质量核验升级：`outputs/工作包/20260426_1857_科研质量核验_顶级文献对标_工作流强化`
- 最新 DQN 文献增强建模方案：`outputs/工作包/20260426_1616_DQN文献增强建模方案与参数确认`
- 当前 canonical PEANUT 清洗表：`data/03_primary/peanut_cleaned_analysis_ready.csv`
- 当前 canonical DQN/MOE/EDI 特征：`data/04_feature/peanut_belief_mdp_state_features_with_moe_edi.csv`

## 推荐删除清单（低风险，但仍等待你确认）

{top_recommended}

## 需要你明确指定的候选

{top_review}

## 特别保护

- `data/01_raw/` 永不删除。
- 最新 DQN experimental run、科研质量升级任务包、DQN 文献增强任务包、canonical PEANUT 数据和 `experiments/optimization/peanut_dqn_auto_*` 均已标记为高风险或需确认，不会自动删除。
"""
    (RUN / "04_报告输出" / "指定清理候选扫描报告.md").write_text(report, encoding="utf-8")
    # Compatibility with the earlier requested name, but this is a scan-only report.
    (RUN / "04_报告输出" / "指定清理报告.md").write_text(report, encoding="utf-8")
    (RUN / "README.md").write_text(
        f"# 指定清理与DQN修正版继续实验\n\n创建时间：{NOW}\n\n本轮按用户最后指令仅执行删除候选扫描，未删除文件，未继续 DQN。\n",
        encoding="utf-8",
    )
    (RUN / "00_输入说明" / "inputs.md").write_text(
        "# 输入说明\n\n用户要求先不要删除，扫描 workflow1 中可删除缓存、旧工作包、旧 DQN 输出、重复报告和过期实验文件，生成候选清单后等待指定。\n",
        encoding="utf-8",
    )


def update_state() -> None:
    rel_run = RUN.relative_to(ROOT).as_posix()
    append_once(ROOT / "outputs" / "_index" / "run_index.md", f"""## {RUN.name}
- 路径：`{rel_run}`
- 结论：按用户最新指令仅完成删除候选扫描；未删除文件，未继续 DQN。等待用户从 `02_表格输出/delete_candidates.csv` 指定删除目标。
""")
    manifest = ROOT / "outputs" / "_index" / "run_manifest.csv"
    append_once(manifest, f"{rel_run},{RUN.name},{RUN.name[:13]},delete_scan_only,AGENTS.md; project_state; outputs/_index; experiments; reports; data/04_feature,delete_candidates.csv; recommended_delete_list.csv; 指定清理候选扫描报告.md,True,False,False,{rel_run}/README.md")
    (ROOT / "project_state" / "current_focus.md").write_text(
        f"# Current Focus\n\n当前完成：指定清理候选扫描。\n\n工作包：`{rel_run}`。\n\n状态：未删除任何文件；DQN 修正版 experimental run 暂停，等待用户指定删除目标并完成索引更新后继续。\n",
        encoding="utf-8",
    )
    (ROOT / "project_state" / "next_step.md").write_text(
        "# Next Step\n\n请从本轮 `02_表格输出/delete_candidates.csv` 或 `recommended_delete_list.csv` 中指定要删除的路径。确认后先执行删除与索引断链检查，再继续 DQN 修正版 experimental run。\n",
        encoding="utf-8",
    )
    append_once(ROOT / "project_state" / "changelog.md", f"## {NOW}\n\n- 创建 `{rel_run}`，完成删除候选扫描；未删除文件，未继续 DQN。\n")
    append_once(ROOT / "project_state" / "decision_log.md", f"## {NOW} 删除候选扫描先行\n\nDecision: 遵循用户最新指令，本轮只扫描候选，不执行删除，也不继续 DQN。\n\nRationale: 删除目标尚未由用户明确指定；DQN 修正版实验必须等待清理和索引更新完成。\n")
    (ROOT / "project_state" / "conversation_handoff.md").write_text(
        f"# Conversation Handoff\n\n{NOW} 完成“指定清理与DQN修正版继续实验”的第一步：删除候选扫描。\n\n主工作包：`{rel_run}`。\n\n关键文件：\n- `02_表格输出/delete_candidates.csv`\n- `02_表格输出/recommended_delete_list.csv`\n- `02_表格输出/delete_candidates_review_required.csv`\n- `04_报告输出/指定清理候选扫描报告.md`\n\n未删除文件；未运行 DQN。下一步等待用户指定删除路径。\n",
        encoding="utf-8",
    )


def write_manifest() -> None:
    rows = []
    for f in sorted(RUN.rglob("*")):
        if f.is_file():
            rows.append({
                "path": f.relative_to(RUN).as_posix(),
                "type": f.suffix.lstrip(".") or "file",
                "description": "delete candidate scan artifact",
                "created_at": NOW,
                "size_bytes": str(f.stat().st_size),
            })
    write_csv(RUN / "manifest.csv", rows)


def main() -> int:
    candidates, protected = find_candidates()
    write_outputs(candidates, protected)
    update_state()
    write_manifest()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
