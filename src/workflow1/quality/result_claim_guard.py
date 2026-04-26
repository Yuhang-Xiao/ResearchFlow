"""Guard research result claims against overstatement."""
from __future__ import annotations

from dataclasses import asdict

from workflow1.quality.claim_to_evidence_mapper import map_claims_to_evidence
from workflow1.quality.evidence_strength_classifier import classify_evidence


FORBIDDEN_ESCALATIONS = [
    ("experimental", "formal"),
    ("prototype", "policy recommendation"),
    ("synthetic parameter", "confirmed parameter"),
    ("unconverged", "effective strategy"),
]


def audit_claims(claims: list[dict], evidence: list[dict]) -> dict:
    links = map_claims_to_evidence(claims, evidence)
    evidence_by_id = {str(item.get("evidence_id")): item for item in evidence}
    findings = []
    for link in links:
        item = evidence_by_id.get(link.evidence_id, {})
        strength = classify_evidence(item)
        claim_text = link.claim.lower()
        status = "pass"
        reason = strength.reason
        if link.status == "missing_evidence":
            status = "block"
            reason = link.note
        elif any(src in claim_text and dst in claim_text for src, dst in FORBIDDEN_ESCALATIONS):
            status = "block"
            reason = "claim contains forbidden escalation"
        elif "formal" in claim_text and not strength.can_support_formal_claim:
            status = "block"
            reason = "formal claim requires confirmed, validated, converged evidence"
        elif not strength.can_support_results:
            status = "revise"
            reason = strength.reason
        findings.append({**asdict(link), "evidence_strength": strength.level, "guard_status": status, "reason": reason})
    return {"status": "pass" if all(f["guard_status"] == "pass" for f in findings) else "needs_revision_or_blocked", "findings": findings}
