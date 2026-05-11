"""Quality gate contracts for auto research product mode."""

from __future__ import annotations

from typing import Any

from workflow1.quality_gates.metric_completeness_gate import MetricCompletenessGate
from workflow1.quality_gates.model_comparison_gate import ModelComparisonGate
from workflow1.quality_gates.model_registry_gate import ModelRegistryGate
from workflow1.quality_gates.paper_completeness_gate import PaperCompletenessGate
from workflow1.quality_gates.latex_product_gate import LatexProductGate


GATE_CONTRACTS: tuple[dict[str, Any], ...] = (
    {
        "gate": "full_paper_product_gate",
        "required": True,
        "must_have": [
            "Title",
            "Abstract",
            "Keywords",
            "Introduction",
            "Literature Review",
            "Method",
            "Results",
            "Discussion",
            "Conclusion",
            "References",
            "Appendix",
        ],
        "failure_action": "auto_repair",
    },
    {
        "gate": "metric_completeness_gate",
        "required": True,
        "must_have": [
            "task_type_detected",
            "task_appropriate_metrics_or_not_applicable_reason",
            "same_split_metric_table",
        ],
        "failure_action": "auto_repair",
    },
    {
        "gate": "model_comparison_gate",
        "required": True,
        "must_have": ["simple_baseline", "interpretable_control", "advanced_candidate_when_applicable"],
        "failure_action": "auto_repair",
    },
    {
        "gate": "explainability_gate",
        "required": True,
        "must_have": [
            "shap_availability_check",
            "permutation_or_model_native_importance",
            "pdp_or_ale_plan",
            "local_or_extreme_case_explanation",
            "predictive_not_causal_statement",
        ],
        "failure_action": "auto_repair_or_record_unavailable_reason",
    },
    {
        "gate": "figure_table_product_gate",
        "required": True,
        "must_have": ["source_table", "nonblank_png_or_valid_table", "caption", "paper_body_reference", "explanation"],
        "failure_action": "auto_repair",
    },
    {
        "gate": "literature_evidence_gate",
        "required": True,
        "must_have": ["section_citation_map", "read_status", "reference_integrity_check"],
        "failure_action": "auto_repair_or_authorization_queue",
    },
    {
        "gate": "word_render_gate",
        "required": True,
        "must_have": ["docx_output", "render_or_fallback_audit", "placeholder_scan", "encoding_scan"],
        "failure_action": "auto_repair",
    },
    {
        "gate": "reproducibility_packaging_gate",
        "required": True,
        "must_have": ["manifest", "reproducibility_readme", "data_card", "model_card", "experiment_card", "evidence_card"],
        "failure_action": "auto_repair",
    },
    {
        "gate": "latex_submission_product_gate",
        "required": True,
        "must_have": [
            "paper/main.tex",
            "paper/references.bib",
            "paper/main.pdf",
            "latex_crossrefs",
            "citation_weaving",
            "bibtex_integrity",
        ],
        "failure_action": "auto_repair",
    },
    {
        "gate": "method_scout_gate",
        "required": True,
        "must_have": [
            "model_candidate_matrix",
            "model_method_literature_map",
            "dependency_approval_plan_for_missing_large_dependencies",
            "not_trained_reason_for_each_skipped_candidate",
        ],
        "failure_action": "auto_repair_or_authorization_queue",
    },
)


def run_quality_gate_plan(plan: Any) -> dict[str, Any]:
    """Return the default gate contract for a product-mode plan."""

    return {
        "status": "planned",
        "gates": list(GATE_CONTRACTS),
        "paper_sections": list(getattr(plan, "required_paper_sections", ())),
        "auto_repair_rounds": list(getattr(plan, "auto_repair_rounds", ())),
        "blocking_statuses": ["fail", "missing", "unable_to_verify_without_reason"],
    }


def run_executable_quality_gates(context: dict[str, Any]) -> list[dict[str, Any]]:
    """Run available gate-as-code checks and return machine-readable results."""

    gates = [
        PaperCompletenessGate(),
        MetricCompletenessGate(),
        ModelComparisonGate(),
        ModelRegistryGate(),
        LatexProductGate(),
    ]
    return [gate.run(context).to_dict() for gate in gates]
