"""Classify evidence strength for research claims."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceStrength:
    level: str
    can_support_results: bool
    can_support_formal_claim: bool
    reason: str


def classify_evidence(evidence: dict) -> EvidenceStrength:
    kind = str(evidence.get("kind", "")).lower()
    verified = bool(evidence.get("verified", False))
    formal = bool(evidence.get("formal_parameters_confirmed", False))
    converged = evidence.get("converged", True)
    if kind in {"validated_data", "verified_table", "verified_model"} and verified and formal and converged:
        return EvidenceStrength("formal_ready", True, True, "validated and confirmed evidence")
    if kind in {"validated_data", "verified_table", "verified_model", "peer_reviewed_literature"} and verified:
        return EvidenceStrength("evidence_supported", True, False, "usable evidence, but not formal-policy ready")
    if kind in {"prototype_model", "synthetic_parameter", "abstract_only_literature"}:
        return EvidenceStrength("prototype_only", False, False, "prototype or limited evidence")
    return EvidenceStrength("insufficient", False, False, "missing or unverified evidence")
