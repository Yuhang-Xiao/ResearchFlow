"""Lightweight run package helpers."""

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
    text = re.sub(r"[\\/:*?\"<>|\s]+", "_", name.strip())
    return text.strip("_") or "未命名任务"


def start_run(name: str, outputs_dir: str | Path = "outputs") -> dict:
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    package = Path(outputs_dir) / "工作包" / f"{stamp}_{slug_name(name)}"
    package.mkdir(parents=True, exist_ok=True)
    for sub in PACKAGE_SUBDIRS:
        (package / sub).mkdir(parents=True, exist_ok=True)
    (package / "00_输入说明" / "inputs.md").write_text("# 输入说明\n\n请记录本轮输入文件路径和摘要。\n", encoding="utf-8")
    (package / "README.md").write_text(f"# {name}\n\n任务开始时间：{stamp}\n\n本目录为 workflow1 任务工作包。\n", encoding="utf-8")
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
