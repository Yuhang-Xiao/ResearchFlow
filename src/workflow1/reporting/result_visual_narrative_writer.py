"""Create visualization plans and result-narrative maps."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_VISUAL_TASKS = [
    ("target_distribution", "response distribution, zero inflation, and long-tail risk"),
    ("seasonality", "calendar and seasonal pest-pressure pattern"),
    ("time_trend", "year-to-year descriptive trend"),
    ("location_difference", "spatial or grouped heterogeneity"),
    ("feature_correlation", "weather, calendar, and target association screening"),
    ("lag_relationship", "historical monitoring signal when operationally available"),
    ("model_comparison", "baseline and candidate model comparison"),
    ("observed_vs_predicted", "prediction agreement and systematic deviation"),
    ("residual_distribution", "residual spread and bias diagnostics"),
    ("extreme_error", "high-pressure or tail-error behavior"),
    ("permutation_importance", "model explanation and feature importance"),
    ("robustness_check", "time holdout or subgroup robustness evidence"),
]


def _write_simple_yaml(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["visualization_plan:"]
    for row in rows:
        lines.append("  -")
        for key, value in row.items():
            lines.append(f"      {key}: \"{str(value).replace(chr(34), chr(39))}\"")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_result_visual_narratives(*, run_dir: str | Path, primary_model: dict[str, Any]) -> dict[str, Path]:
    package = Path(run_dir)
    fig_dir = next((p for p in package.iterdir() if p.is_dir() and p.name.startswith("04_")), package / "04_图表与解释")
    fig_dir.mkdir(parents=True, exist_ok=True)
    figure_map_path = fig_dir / "figure_crossref_map.csv"
    figures = pd.read_csv(figure_map_path, encoding="utf-8-sig") if figure_map_path.exists() else pd.DataFrame()

    plan_rows = []
    for task, purpose in DEFAULT_VISUAL_TASKS:
        matched = ""
        if not figures.empty:
            for _, row in figures.iterrows():
                blob = " ".join(str(row.get(col, "")) for col in figures.columns).lower()
                if task.replace("_", " ") in blob or task in blob:
                    matched = str(row.get("figure_id", row.get("file", "")))
                    break
        plan_rows.append({"visual_task": task, "purpose": purpose, "matched_artifact": matched or "not_yet_available", "status": "pass" if matched else "review"})

    plan_path = fig_dir / "visualization_plan.yaml"
    _write_simple_yaml(plan_path, plan_rows)

    claim_rows = []
    if not figures.empty:
        for _, row in figures.iterrows():
            fig_id = str(row.get("figure_id", row.get("file", "figure")))
            caption = str(row.get("caption", ""))
            label = str(row.get("latex_label", ""))
            claim_rows.append(
                {
                    "figure_id": fig_id,
                    "latex_label": label,
                    "paper_section": "Results",
                    "claim_supported": f"{caption} This figure supports the descriptive or diagnostic interpretation linked to {fig_id}.",
                    "source_data": row.get("source_data", ""),
                    "qa_status": row.get("qa_status", "unknown"),
                    "body_reference_required": "yes",
                    "status": "pass" if str(row.get("qa_status", "")).lower() == "pass" else "review",
                }
            )
    claim_path = fig_dir / "figure_to_claim_map.csv"
    pd.DataFrame(claim_rows).to_csv(claim_path, index=False, encoding="utf-8-sig")

    narrative_path = fig_dir / "result_visual_narrative.md"
    primary = primary_model.get("model", "selected model")
    narrative_path.write_text(
        f"""# Result Visual Narrative

The visualization set is organized around the scientific argument rather than around file production. Descriptive figures establish the response distribution, seasonal timing, temporal variation, grouped heterogeneity, and candidate feature relationships. Diagnostic figures then connect the selected model (`{primary}`) to model comparison, observed-versus-predicted behavior, residual spread, tail-error concerns, and feature-importance interpretation.

Every figure used in the Results section must have source data, a caption, a LaTeX label, a body reference, and a claim map entry. Figures with `review` status are allowed as exploratory supplements but cannot support formal Results claims until repaired.
""",
        encoding="utf-8",
    )

    audit_rows = []
    for row in plan_rows:
        audit_rows.append(
            {
                "visual_task": row["visual_task"],
                "matched_artifact": row["matched_artifact"],
                "status": "pass" if row["status"] == "pass" or row["visual_task"] in {"lag_relationship", "extreme_error", "robustness_check"} else "fail",
            }
        )
    audit_path = fig_dir / "visualization_coverage_matrix.csv"
    pd.DataFrame(audit_rows).to_csv(audit_path, index=False, encoding="utf-8-sig")
    return {"plan": plan_path, "claim_map": claim_path, "narrative": narrative_path, "audit": audit_path}
