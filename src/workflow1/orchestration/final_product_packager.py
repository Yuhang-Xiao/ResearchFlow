"""Final package contract for paper-grade research products."""

from __future__ import annotations


FINAL_PRODUCT_REQUIRED_ARTIFACTS: tuple[str, ...] = (
    "README.md",
    "manifest.csv",
    "data_lineage_manifest.csv",
    "reproducibility_README.md",
    "full_paper.md",
    "full_paper.docx",
    "paper_completeness_gate.csv",
    "quality_gate_results.csv",
    "redo_log.csv",
    "artifact_explanation_index.md",
    "artifact_to_evidence_map.csv",
    "data_card.md",
    "model_card.md",
    "experiment_card.md",
    "evidence_card.md",
)


def package_verdict(missing_artifacts: tuple[str, ...] = (), unresolved_issues: tuple[str, ...] = ()) -> dict[str, object]:
    """Return whether the product is ready for user-level micro-editing."""

    if unresolved_issues:
        status = "needs_user_authorization_or_scientific_input"
    elif missing_artifacts:
        status = "needs_auto_repair"
    else:
        status = "ready_for_user_micro_edit"
    return {
        "status": status,
        "required_artifacts": list(FINAL_PRODUCT_REQUIRED_ARTIFACTS),
        "missing_artifacts": list(missing_artifacts),
        "unresolved_issues": list(unresolved_issues),
    }
