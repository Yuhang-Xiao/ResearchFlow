"""Build evidence maps for paper sections."""
from __future__ import annotations


def build_section_evidence_map(section: str, claims: list[dict], citations: list[dict]) -> dict:
    return {"section": section, "claims": claims, "citations": citations, "requires_claim_guard": True, "requires_citation_verification": True}
