"""Gate: references include identifiers and sidecars."""

from __future__ import annotations

from workflow1.quality_gates.base import QualityGate


class ReferenceIntegrityGate(QualityGate):
    gate_name = "ReferenceIntegrityGate"

    def run(self, context: dict[str, object]):
        refs = list(context.get("references", []))
        bad = [r for r in refs if not (r.get("citation_key") and (r.get("doi") or r.get("url")) and r.get("read_status"))]
        if bad:
            return self.fail([f"{len(bad)} references missing key/doi/url/read_status"], ["repair_reference_sidecar"])
        return self.pass_()
