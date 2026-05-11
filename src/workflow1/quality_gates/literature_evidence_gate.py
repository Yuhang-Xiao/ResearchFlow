"""Gate: paper sections have literature/result evidence."""

from __future__ import annotations

from workflow1.quality_gates.base import QualityGate


class LiteratureEvidenceGate(QualityGate):
    gate_name = "LiteratureEvidenceGate"

    def run(self, context: dict[str, object]):
        section_map = list(context.get("section_evidence_map", []))
        supported = [row for row in section_map if row.get("read_status") in {"full-text", "abstract-only"} or row.get("evidence_type") in {"result", "figure", "table"}]
        if len(supported) < 4:
            return self.fail(["insufficient_section_evidence"], ["expand_literature_search", "build_section_citation_map"])
        return self.pass_()
