"""Quality gate for LaTeX submission packages."""

from __future__ import annotations

import csv
from pathlib import Path

from workflow1.quality_gates.base import QualityGate


class LatexProductGate(QualityGate):
    gate_name = "LatexProductGate"

    def run(self, context: dict[str, object]):
        paper_dir = Path(str(context.get("paper_dir", "")))
        main_tex = paper_dir / "main.tex"
        references = paper_dir / "references.bib"
        pdf = paper_dir / "main.pdf"
        required = [main_tex, references, pdf]
        missing = [str(path) for path in required if not path.exists() or path.stat().st_size == 0]
        if missing:
            return self.fail(missing, ["build_latex_paper", "compile_latex", "repair_missing_latex_artifacts"])

        crossref_path = Path(str(context.get("crossref_audit", "")))
        citation_path = Path(str(context.get("citation_map", "")))
        issues: list[str] = []
        if crossref_path.exists():
            with crossref_path.open("r", encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            for row in rows:
                if row.get("status") not in {"pass", "pass_with_limits"}:
                    issues.append(f"crossref:{row}")
        if citation_path.exists():
            with citation_path.open("r", encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            unsupported = [r for r in rows if r.get("support_status") in {"missing", "metadata_only_for_strong_claim"}]
            if unsupported:
                issues.append(f"unsupported_claims:{len(unsupported)}")
        if issues:
            return self.fail(issues, ["repair_citations", "repair_crossrefs", "downgrade_unsupported_claims"])
        return self.pass_([str(path) for path in required])
