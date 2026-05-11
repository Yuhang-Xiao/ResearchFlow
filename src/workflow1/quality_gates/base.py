"""Base helpers for executable quality gates."""

from __future__ import annotations

from workflow1.orchestration.gate_result import QualityGateResult


class QualityGate:
    gate_name = "QualityGate"

    def fail(self, failed_items: list[str], suggestions: list[str], severity: str = "high", auto_repairable: bool = True) -> QualityGateResult:
        return QualityGateResult(
            gate_name=self.gate_name,
            status="fail",
            severity=severity,
            failed_items=failed_items,
            repair_suggestions=suggestions,
            auto_repairable=auto_repairable,
            requires_human_authorization=False,
        )

    def pass_(self, evidence_files: list[str] | None = None) -> QualityGateResult:
        return QualityGateResult(
            gate_name=self.gate_name,
            status="pass",
            severity="none",
            evidence_files=evidence_files or [],
            auto_repairable=False,
            requires_human_authorization=False,
        )
