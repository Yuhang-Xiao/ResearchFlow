"""Orchestrate safe paper section generation QA."""
from __future__ import annotations

from workflow1.reporting.paper_quality_auditor import audit_paper_section
from workflow1.reporting.section_evidence_mapper import build_section_evidence_map


def plan_paper_section(section: str, claims: list[dict], citations: list[dict], benchmark: str | None = None) -> dict:
    evidence_map = build_section_evidence_map(section, claims, citations)
    evidence_map["top_journal_benchmark"] = benchmark
    audit = audit_paper_section(evidence_map)
    return {"section": section, "outline_required": True, "evidence_map": evidence_map, "quality_audit": audit, "docx_export_required": True}
