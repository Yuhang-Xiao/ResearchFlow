"""Gate: paper contains all required sections."""

from __future__ import annotations

from pathlib import Path

from workflow1.quality_gates.base import QualityGate


class PaperCompletenessGate(QualityGate):
    gate_name = "PaperCompletenessGate"
    required_sections = ["Title", "Abstract", "Keywords", "Introduction", "Literature Review", "Method", "Results", "Discussion", "Conclusion", "References", "Appendix"]

    def run(self, context: dict[str, object]):
        text = ""
        if context.get("paper_text"):
            text = str(context["paper_text"])
        elif context.get("paper_path") and Path(str(context["paper_path"])).exists():
            text = Path(str(context["paper_path"])).read_text(encoding="utf-8", errors="ignore")
        missing = [s for s in self.required_sections if s.lower() not in text.lower()]
        if missing:
            return self.fail(missing, ["write_missing_paper_sections"])
        return self.pass_([str(context.get("paper_path", ""))])
