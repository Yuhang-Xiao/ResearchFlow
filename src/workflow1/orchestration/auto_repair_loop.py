"""Three-round repair loop contract for product-mode workflows."""

from __future__ import annotations


AUTO_REPAIR_STOP_ONLY_FOR: tuple[str, ...] = (
    "raw data unreadable",
    "missing critical user-supplied parameter",
    "Zotero database write approval",
    "API key or paid access",
    "large dependency or external service installation",
    "scientific choice changes conclusions and needs human judgment",
)


def plan_auto_repair_loop(failed_gates: tuple[str, ...] = ()) -> dict[str, object]:
    """Plan a three-round repair loop for failed product gates."""

    return {
        "rounds": [
            {
                "round": "round_1_initial_execution",
                "purpose": "produce first complete pass with explicit assumptions",
            },
            {
                "round": "round_2_quality_gate_repair",
                "purpose": "repair missing metrics, models, explanations, figures, citations, and claims",
            },
            {
                "round": "round_3_word_and_paper_repair",
                "purpose": "repair DOCX rendering, full-paper completeness, references, and final package verdict",
            },
        ],
        "failed_gates": list(failed_gates),
        "required_logs": [
            "redo_log.csv",
            "failed_gate_summary.md",
            "repaired_items.csv",
            "remaining_issues.csv",
        ],
        "stop_only_for": list(AUTO_REPAIR_STOP_ONLY_FOR),
    }
