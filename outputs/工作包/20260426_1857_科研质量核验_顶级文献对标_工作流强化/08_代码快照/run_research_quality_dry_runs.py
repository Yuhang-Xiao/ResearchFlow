from __future__ import annotations

import ast
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]

GOALS = [
    "核验当前模型结果并与顶级期刊对标",
    "运行多模型比较并生成质量审计报告",
    "生成论文结果部分并导出 Word",
    "扩充当前项目核心文献并写入 Zotero 笔记",
    "优化当前工作流并搜索验证类 skill",
]


def main() -> int:
    rows: list[dict[str, str]] = []
    report = [
        "# Research Quality Workflow Dry-run Report",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
    ]
    for goal in GOALS:
        proc = subprocess.run(
            [sys.executable, "-m", "workflow1", "--stage", "dry-run", "--goal", goal],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        report.extend([f"## {goal}", "", "```text", stdout, "```", ""])
        if stderr:
            report.extend(["stderr:", "```text", stderr, "```", ""])
        data = ast.literal_eval(stdout)
        plan = data.get("details", {}).get("one_line_plan", {})
        rows.append(
            {
                "goal": plan.get("goal", ""),
                "matched_intent": plan.get("matched_intent") or plan.get("intent", ""),
                "selected_recipe": plan.get("selected_recipe", ""),
                "skills_to_call": ";".join(plan.get("required_skills", [])),
                "required_inputs": ";".join(plan.get("required_inputs", [])),
                "quality_gates": ";".join(plan.get("quality_gates", plan.get("common_quality_gates", []))),
                "expected_outputs": ";".join(plan.get("expected_outputs", [])),
                "stop_conditions": ";".join(plan.get("stop_conditions", [])),
                "approval_required_items": ";".join(plan.get("approval_required", [])),
                "status": data.get("status", ""),
                "returncode": str(proc.returncode),
            }
        )
    (RUN / "04_报告输出" / "research_quality_workflow_dry_run_report.md").write_text("\n".join(report), encoding="utf-8")
    with (RUN / "02_表格输出" / "research_quality_workflow_dry_run_results.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
