"""Gate: Word output rendered or audited fallback exists."""

from __future__ import annotations

from pathlib import Path

from workflow1.quality_gates.base import QualityGate


class WordRenderGate(QualityGate):
    gate_name = "WordRenderGate"

    def run(self, context: dict[str, object]):
        docx = Path(str(context.get("docx_path", "")))
        audit = Path(str(context.get("render_audit_path", "")))
        if not docx.exists() or not audit.exists():
            return self.fail(["docx_or_render_audit_missing"], ["repair_docx_layout", "write_render_fallback_audit"])
        text = audit.read_text(encoding="utf-8", errors="ignore")
        if "placeholder" in text.lower() or "乱码" in text:
            return self.fail(["render_audit_contains_placeholder_or_encoding_issue"], ["repair_docx_layout"])
        return self.pass_([str(docx), str(audit)])
