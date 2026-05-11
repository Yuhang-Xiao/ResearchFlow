"""Map result claims to evidence records."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimEvidenceLink:
    claim_id: str
    claim: str
    evidence_id: str
    evidence_kind: str
    status: str
    note: str


def map_claims_to_evidence(claims: list[dict], evidence: list[dict]) -> list[ClaimEvidenceLink]:
    by_id = {str(item.get("evidence_id")): item for item in evidence}
    links: list[ClaimEvidenceLink] = []
    for idx, claim in enumerate(claims, 1):
        evidence_id = str(claim.get("evidence_id", ""))
        item = by_id.get(evidence_id)
        if not item:
            links.append(ClaimEvidenceLink(str(claim.get("claim_id", idx)), str(claim.get("claim", "")), evidence_id, "", "missing_evidence", "claim has no matching evidence"))
            continue
        links.append(ClaimEvidenceLink(str(claim.get("claim_id", idx)), str(claim.get("claim", "")), evidence_id, str(item.get("kind", "")), "mapped", "evidence found"))
    return links
