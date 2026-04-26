from __future__ import annotations

def evaluate_candidates(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for c in candidates:
        rec = c.get("recommendation", "REFERENCE_ONLY")
        rows.append({
            **c,
            "relevance_to_workflow1": "4" if rec != "REJECT" else "1",
            "documentation_quality": "3",
            "license_clarity": "unknown_check_before_copying",
            "security_risk": "high" if rec == "APPROVAL_REQUIRED_PLUGIN" else "low",
            "dependency_risk": "high" if rec == "APPROVAL_REQUIRED_PLUGIN" else "low",
            "needs_user_approval": str(rec == "APPROVAL_REQUIRED_PLUGIN").lower(),
        })
    return rows
