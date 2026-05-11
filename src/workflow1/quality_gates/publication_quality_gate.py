"""Publication-grade package quality checks."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pandas as pd

from workflow1.quality_gates.base import QualityGate


class PublicationQualityGate(QualityGate):
    gate_name = "PublicationQualityGate"

    def run(self, context: dict[str, object]):
        package_dir = Path(str(context.get("package_dir", "")))
        issues = audit_publication_package(package_dir)
        failed = [f"{row['gate']}:{row['status']}" for row in issues if row["status"] not in {"pass", "pass_with_limits"}]
        if failed:
            return self.fail(failed, ["repair_publication_package", "rerun_latex_and_literature_gates"])
        return self.pass_([str(_quality_gate_output_path(package_dir))])


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _latex_counts(tex: str) -> dict[str, int]:
    citation_groups = re.findall(r"\\cite[tp]?\{([^}]+)\}", tex)
    citation_keys = [k.strip() for group in citation_groups for k in group.split(",") if k.strip()]
    return {
        "citations": len(set(citation_keys)),
        "figure_refs": len(re.findall(r"\\ref\{fig:", tex)),
        "table_refs": len(re.findall(r"\\ref\{tab:", tex)),
        "sections": len(re.findall(r"\\section\{", tex)),
    }


def _prefixed_dir(package: Path, prefix: str) -> Path:
    if not package.exists():
        return package / prefix.rstrip("_")
    matches = sorted([p for p in package.iterdir() if p.is_dir() and p.name.startswith(prefix)])
    return matches[0] if matches else package / prefix.rstrip("_")


def _quality_gate_output_path(package_dir: str | Path) -> Path:
    package = Path(package_dir)
    audit_dir = _prefixed_dir(package, "08_")
    if audit_dir.exists():
        return audit_dir / "quality_gates.csv"
    return package / "quality_gates.csv"


def _zotero_readback_row(package: Path) -> dict[str, object] | None:
    zotero_dir = _prefixed_dir(package, "06_")
    if not zotero_dir.exists():
        return None

    readback = zotero_dir / "zotero_readback_verification.json"
    if not readback.exists():
        return {
            "gate": "zotero_readback_gate",
            "observed": "missing zotero_readback_verification.json",
            "required": "collection metadata and membership readback pass",
            "status": "fail",
        }

    try:
        data = json.loads(readback.read_text(encoding="utf-8-sig"))
        collection = data.get("collection", {})
        if not isinstance(collection, dict):
            return {
                "gate": "zotero_readback_gate",
                "observed": f"pending_or_incomplete_readback={collection}",
                "required": "collection metadata and membership readback pass",
                "status": "fail",
            }
        duplicates = str(data.get("duplicates_by_title", ""))
        verified_items = data.get("items_verified", [])
        zotero_ok = (
            collection.get("membership_readback") == "pass"
            and duplicates in {"none_found", "none"}
            and int(collection.get("item_count", 0)) >= 1
            and all(item.get("membership") == "verified" for item in verified_items)
        )
        observed = f"{collection.get('name')}/{collection.get('key')} item_count={collection.get('item_count')} duplicates={duplicates}"
    except Exception as exc:
        zotero_ok = False
        observed = f"readback_parse_error={exc}"

    return {
        "gate": "zotero_readback_gate",
        "observed": observed,
        "required": "collection metadata and membership readback pass",
        "status": "pass" if zotero_ok else "fail",
    }


def audit_publication_package(package_dir: str | Path) -> list[dict[str, object]]:
    package = Path(package_dir)
    latex_dir = _prefixed_dir(package, "05_")
    if not latex_dir.exists():
        latex_dir = package / "paper"
    tex_path = latex_dir / "main.tex"
    log_path = latex_dir / "main.log"
    pdf_path = latex_dir / "main.pdf"
    tex = tex_path.read_text(encoding="utf-8", errors="replace") if tex_path.exists() else ""
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    counts = _latex_counts(tex)

    lit_dir = _prefixed_dir(package, "02_")
    candidate_rows = _read_csv(lit_dir / "q1_literature_candidate_pool.csv")
    core_rows = _read_csv(lit_dir / "core_q1_literature_selected.csv")
    q1_like = [r for r in core_rows if "Q1" in r.get("journal_quartile", "") or "flagship" in r.get("journal_quartile", "")]

    table_audit = _read_csv(latex_dir / "table_layout_audit.csv")
    model_dir = _prefixed_dir(package, "03_")
    model_audit = _read_csv(model_dir / "pathological_model_audit.csv")
    method_detail = _read_csv(model_dir / "model_setting_detail_table.csv")
    method_detail_audit = _read_csv(model_dir / "model_setting_detail_audit.csv")
    fig_dir = _prefixed_dir(package, "04_")
    figure_claim_map = _read_csv(fig_dir / "figure_to_claim_map.csv")
    visual_coverage = _read_csv(fig_dir / "visualization_coverage_matrix.csv")
    proofreading_dir = _prefixed_dir(package, "07_")
    top_journal_matrix = _read_csv(proofreading_dir / "top_journal_benchmark_matrix.csv")
    reviewer_risk = _read_csv(proofreading_dir / "reviewer_risk_matrix.csv")
    content_audit = _read_csv(_prefixed_dir(package, "08_") / "content_completeness_audit.csv")
    corpus_dir = _prefixed_dir(package, "09_")
    corpus_audit = _read_csv(corpus_dir / "corpus_quality_audit.csv")

    rows: list[dict[str, object]] = [
        {"gate": "chinese_run_package_structure", "observed": package.exists(), "required": True, "status": "pass" if package.exists() else "fail"},
        {"gate": "q1_literature_candidate_count", "observed": len(candidate_rows), "required": 35, "status": "pass" if len(candidate_rows) >= 35 else "fail"},
        {"gate": "core_literature_count", "observed": len(core_rows), "required": 25, "status": "pass" if len(core_rows) >= 25 else "fail"},
        {"gate": "q1_or_flagship_core_count", "observed": len(q1_like), "required": 12, "status": "pass" if len(q1_like) >= 12 else "pass_with_limits"},
        {"gate": "paper_depth_sections", "observed": counts["sections"], "required": 7, "status": "pass" if counts["sections"] >= 7 else "fail"},
        {"gate": "citation_density", "observed": counts["citations"], "required": 20, "status": "pass" if counts["citations"] >= 20 else "fail"},
        {"gate": "figure_crossrefs", "observed": counts["figure_refs"], "required": 8, "status": "pass" if counts["figure_refs"] >= 8 else "fail"},
        {"gate": "table_crossrefs", "observed": counts["table_refs"], "required": 5, "status": "pass" if counts["table_refs"] >= 5 else "fail"},
        {"gate": "latex_pdf", "observed": pdf_path.exists() and pdf_path.stat().st_size > 0 if pdf_path.exists() else False, "required": True, "status": "pass" if pdf_path.exists() and pdf_path.stat().st_size > 0 else "fail"},
        {"gate": "latex_overfull", "observed": log.count("Overfull \\hbox"), "required": 0, "status": "pass" if "Overfull \\hbox" not in log else "fail"},
        {"gate": "latex_unresolved", "observed": "undefined" in log.lower(), "required": False, "status": "pass" if "undefined references" not in log.lower() and "undefined citations" not in log.lower() else "fail"},
        {"gate": "table_layout", "observed": len(table_audit), "required": "all pass", "status": "pass" if table_audit and all(r.get("status") == "pass" for r in table_audit) else "fail"},
        {"gate": "model_pathology_audit", "observed": len(model_audit), "required": ">0 rows", "status": "pass" if model_audit else "fail"},
        {"gate": "proofreading_outputs", "observed": proofreading_dir.exists(), "required": True, "status": "pass" if proofreading_dir.exists() and any(proofreading_dir.glob("*.md")) else "fail"},
        {"gate": "content_completeness_gate", "observed": len([r for r in content_audit if r.get("status") == "fail"]), "required": "0 failed required topics", "status": "pass" if content_audit and all(r.get("status") == "pass" for r in content_audit) else "fail"},
        {"gate": "method_detail_gate", "observed": len(method_detail), "required": "model setting details and audit pass", "status": "pass" if method_detail and method_detail_audit and all(r.get("status") == "pass" for r in method_detail_audit) else "fail"},
        {"gate": "result_visual_narrative_gate", "observed": len(figure_claim_map), "required": "figure claim map and coverage audit", "status": "pass" if figure_claim_map and visual_coverage and all(r.get("status") in {"pass", "review"} for r in visual_coverage) else "fail"},
        {"gate": "top_journal_benchmark_gate", "observed": len(top_journal_matrix), "required": "benchmark matrix and reviewer risk matrix", "status": "pass" if top_journal_matrix and reviewer_risk else "fail"},
        {"gate": "corpus_safety_gate", "observed": len(corpus_audit), "required": "all corpus files pass safety and schema checks", "status": "pass" if corpus_audit and all(r.get("status") == "pass" for r in corpus_audit) else "fail"},
        {"gate": "corpus_reuse_gate", "observed": corpus_dir.exists(), "required": "RAG and optional training corpus generated", "status": "pass" if corpus_dir.exists() and (corpus_dir / "corpus_manifest.csv").exists() else "fail"},
        {"gate": "corpus_dedup_gate", "observed": len([r for r in corpus_audit if str(r.get("dedup_pass", "")).lower() in {"false", "0"}]), "required": "0 duplicate hashes within corpus files", "status": "pass" if corpus_audit and all(str(r.get("dedup_pass", "")).lower() in {"true", "1"} for r in corpus_audit) else "fail"},
    ]
    zotero_row = _zotero_readback_row(package)
    if zotero_row is not None:
        rows.append(zotero_row)

    out = _quality_gate_output_path(package)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8-sig")
    return rows
