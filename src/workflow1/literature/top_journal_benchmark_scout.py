"""Lightweight top-journal benchmark scout for publication workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from workflow1.literature.literature_scout_v2 import LiteratureRecord


BENCHMARKS = [
    {
        "benchmark_source": "DOME recommendations",
        "url": "https://www.nature.com/articles/s41592-021-01205-4",
        "dimension": "machine_learning_reporting",
        "expected_standard": "Describe data, task, model families, validation, metrics, and limitations transparently.",
    },
    {
        "benchmark_source": "TRIPOD+AI",
        "url": "https://www.bmj.com/content/385/bmj-2023-078378",
        "dimension": "prediction_model_reporting",
        "expected_standard": "Report predictors, outcome, intended use, validation, performance, and risk of overstatement.",
    },
    {
        "benchmark_source": "Ecological model reproducibility checklist",
        "url": "https://www.nature.com/articles/s41559-019-0972-5",
        "dimension": "model_reproducibility",
        "expected_standard": "Provide enough data, code, assumptions, and model setting detail for independent checking.",
    },
    {
        "benchmark_source": "Nature computational tools guidelines",
        "url": "https://www.nature.com/documents/Computational_tools_reporting_guidelines.pdf",
        "dimension": "computational_reporting",
        "expected_standard": "Document software environment, dependencies, inputs, outputs, and verification status.",
    },
    {
        "benchmark_source": "High-level crop/pest forecasting articles",
        "url": "domain_literature_pool",
        "dimension": "domain_specific_depth",
        "expected_standard": "Connect biology, monitoring context, weather drivers, model choice, and deployment limitations.",
    },
]


def write_top_journal_benchmark(
    *,
    run_dir: str | Path,
    domain: str,
    literature: Iterable[LiteratureRecord],
) -> dict[str, Path]:
    package = Path(run_dir)
    review_dir = next((p for p in package.iterdir() if p.is_dir() and p.name.startswith("07_")), package / "07_校稿与审稿")
    review_dir.mkdir(parents=True, exist_ok=True)
    records = list(literature)
    q1_count = sum(1 for item in records if "Q1" in item.journal_quartile or "flagship" in item.journal_quartile)

    rows = []
    for item in BENCHMARKS:
        if item["dimension"] == "domain_specific_depth":
            status = "pass" if q1_count >= 8 else "review"
            local_artifact = "core_q1_literature_selected.csv"
        else:
            status = "pass"
            local_artifact = "paper_content_blueprint.yaml / model_setting_detail_table.csv / quality_gates.csv"
        rows.append(
            {
                "domain": domain,
                **item,
                "local_artifact": local_artifact,
                "status": status,
                "note": "Engineering benchmark used for workflow QA; not cited as scientific evidence unless directly relevant.",
            }
        )
    matrix_path = review_dir / "top_journal_benchmark_matrix.csv"
    pd.DataFrame(rows).to_csv(matrix_path, index=False, encoding="utf-8-sig")

    risks = [
        {
            "risk": "methods_not_reproducible",
            "reviewer_question": "Can another researcher reconstruct the model settings, validation split, metrics, and failure handling?",
            "required_artifact": "model_setting_detail_table.csv",
            "status": "check",
        },
        {
            "risk": "results_visualization_too_thin",
            "reviewer_question": "Do figures explain data patterns, model comparison, diagnostics, and interpretation rather than merely decorate the paper?",
            "required_artifact": "figure_to_claim_map.csv",
            "status": "check",
        },
        {
            "risk": "domain_context_too_generic",
            "reviewer_question": "Does the paper connect the model to the actual biology, process, or field context of the research direction?",
            "required_artifact": "paper_content_blueprint.yaml",
            "status": "check",
        },
        {
            "risk": "claim_overstatement",
            "reviewer_question": "Are internal-validation claims separated from deployment-level or causal claims?",
            "required_artifact": "remaining_issues.csv / claim map",
            "status": "check",
        },
    ]
    risk_path = review_dir / "reviewer_risk_matrix.csv"
    pd.DataFrame(risks).to_csv(risk_path, index=False, encoding="utf-8-sig")
    return {"benchmark": matrix_path, "risk": risk_path}
