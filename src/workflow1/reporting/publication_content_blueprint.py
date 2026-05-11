"""Build and audit content blueprints for complete publication manuscripts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


DEFAULT_REQUIREMENTS = [
    {
        "section": "Introduction",
        "topic": "research_background_and_practical_problem",
        "keywords": ["rice", "pest", "forecast", "surveillance", "management", "risk"],
        "severity": "required",
    },
    {
        "section": "Introduction",
        "topic": "knowledge_gap_and_contribution",
        "keywords": ["gap", "objective", "contribution", "study", "aim"],
        "severity": "required",
    },
    {
        "section": "Literature Review",
        "topic": "domain_biology_or_process_context",
        "keywords": ["life cycle", "biology", "larvae", "crop stage", "development", "ecology"],
        "severity": "required",
    },
    {
        "section": "Literature Review",
        "topic": "algorithm_and_modeling_review",
        "keywords": ["machine learning", "count", "zero", "tree", "sequence", "validation"],
        "severity": "required",
    },
    {
        "section": "Materials and Methods",
        "topic": "data_and_unit_of_analysis",
        "keywords": ["data", "observation", "target", "unit", "weekly", "response"],
        "severity": "required",
    },
    {
        "section": "Materials and Methods",
        "topic": "preprocessing_and_feature_engineering",
        "keywords": ["feature", "calendar", "weather", "lag", "rolling", "preprocessing"],
        "severity": "required",
    },
    {
        "section": "Materials and Methods",
        "topic": "model_families_and_hyperparameters",
        "keywords": ["baseline", "poisson", "tweedie", "random forest", "extra trees", "hyperparameter"],
        "severity": "required",
    },
    {
        "section": "Materials and Methods",
        "topic": "validation_metrics_and_failure_handling",
        "keywords": ["time", "holdout", "mae", "rmse", "r2", "rmsle", "pathological"],
        "severity": "required",
    },
    {
        "section": "Results",
        "topic": "data_patterns_and_visual_findings",
        "keywords": ["distribution", "seasonality", "location", "trend", "figure"],
        "severity": "required",
    },
    {
        "section": "Results",
        "topic": "model_comparison_diagnostics_and_interpretation",
        "keywords": ["model", "comparison", "residual", "predicted", "importance", "error"],
        "severity": "required",
    },
    {
        "section": "Discussion",
        "topic": "scientific_interpretation_and_limitations",
        "keywords": ["interpretation", "limitation", "external validation", "future", "deployment"],
        "severity": "required",
    },
    {
        "section": "Conclusion",
        "topic": "bounded_conclusion",
        "keywords": ["conclusion", "supports", "requires", "validation", "recommendations"],
        "severity": "required",
    },
]


def _yaml_scalar(value: object) -> str:
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def _write_simple_yaml(path: Path, data: Mapping[str, object]) -> None:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, Mapping):
                    lines.append("  -")
                    for sub_key, sub_value in item.items():
                        if isinstance(sub_value, list):
                            lines.append(f"      {sub_key}:")
                            for token in sub_value:
                                lines.append(f"        - {_yaml_scalar(token)}")
                        else:
                            lines.append(f"      {sub_key}: {_yaml_scalar(sub_value)}")
                else:
                    lines.append(f"  - {_yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _extract_section(tex: str, section: str) -> str:
    pattern = re.compile(rf"\\section\{{{re.escape(section)}\}}(.*?)(?=\\section\{{|\\bibliography|\\end\{{document\}})", re.S)
    match = pattern.search(tex)
    return match.group(1) if match else ""


def audit_content_completeness(tex: str, requirements: Iterable[Mapping[str, object]] = DEFAULT_REQUIREMENTS) -> pd.DataFrame:
    rows = []
    full_lower = tex.lower()
    for item in requirements:
        section = str(item["section"])
        section_text = _extract_section(tex, section)
        haystack = section_text.lower() if section_text else full_lower
        keywords = [str(k).lower() for k in item.get("keywords", [])]
        hits = [k for k in keywords if k in haystack]
        covered = bool(section_text) and len(hits) >= max(1, min(2, len(keywords)))
        rows.append(
            {
                "section": section,
                "required_topic": item["topic"],
                "severity": item.get("severity", "required"),
                "coverage_terms": "; ".join(hits),
                "covered": covered,
                "status": "pass" if covered else "fail",
            }
        )
    return pd.DataFrame(rows)


def write_publication_content_blueprint(
    *,
    run_dir: str | Path,
    research_goal: str,
    domain: str,
    task_type: str,
    literature_count: int,
) -> dict[str, Path]:
    """Write a content blueprint and audit for a publication package."""

    package = Path(run_dir)
    paper_dir = next((p for p in package.iterdir() if p.is_dir() and p.name.startswith("05_")), package / "05_LaTeX论文")
    quality_dir = next((p for p in package.iterdir() if p.is_dir() and p.name.startswith("08_")), package / "08_质量门与返工日志")
    paper_dir.mkdir(parents=True, exist_ok=True)
    quality_dir.mkdir(parents=True, exist_ok=True)

    blueprint_path = paper_dir / "paper_content_blueprint.yaml"
    _write_simple_yaml(
        blueprint_path,
        {
            "research_goal": research_goal,
            "domain": domain,
            "task_type": task_type,
            "literature_count": literature_count,
            "principle": "Completeness is judged by scientific content coverage, not fixed word count.",
            "requirements": DEFAULT_REQUIREMENTS,
        },
    )

    tex_path = paper_dir / "main.tex"
    tex = tex_path.read_text(encoding="utf-8", errors="replace") if tex_path.exists() else ""
    audit = audit_content_completeness(tex)
    audit_path = quality_dir / "content_completeness_audit.csv"
    audit.to_csv(audit_path, index=False, encoding="utf-8-sig")
    return {"blueprint": blueprint_path, "audit": audit_path}
