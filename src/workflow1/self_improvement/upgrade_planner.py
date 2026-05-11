from __future__ import annotations

def build_action_plan(evaluations: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for e in evaluations:
        rec = e.get("recommendation", "REFERENCE_ONLY")
        action = {
            "ADAPT_AS_LOCAL_SKILL": "Adapt checklist/trigger structure into local SKILL.md.",
            "ADD_TO_RECIPE_OR_REGISTRY": "Add method to workflow recipe or registry.",
            "ADD_LIGHTWEIGHT_STUB": "Create local Python stub.",
            "APPROVAL_REQUIRED_PLUGIN": "Add to approval queue; do not install.",
            "REFERENCE_ONLY": "Keep as design reference.",
            "REJECT": "Reject and record reason.",
        }.get(rec, "Review manually.")
        rows.append({"candidate": e["name"], "recommendation": rec, "planned_action": action, "safe_only": str(rec != "APPROVAL_REQUIRED_PLUGIN").lower()})
    return rows
