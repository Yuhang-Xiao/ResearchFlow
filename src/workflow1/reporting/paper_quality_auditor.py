"""Paper section quality gates."""
from __future__ import annotations


def audit_paper_section(section_map: dict) -> dict:
    claims = section_map.get("claims", [])
    citations = section_map.get("citations", [])
    findings = []
    if not claims:
        findings.append("missing_claims")
    if not citations:
        findings.append("missing_citations")
    if not section_map.get("top_journal_benchmark"):
        findings.append("missing_top_journal_benchmark")
    return {"status": "pass" if not findings else "needs_revision", "findings": findings}
