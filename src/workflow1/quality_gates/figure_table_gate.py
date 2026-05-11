"""Gate: figures and tables exist and are reportable."""

from __future__ import annotations

from pathlib import Path

from workflow1.quality_gates.base import QualityGate


class FigureTableGate(QualityGate):
    gate_name = "FigureTableGate"

    def run(self, context: dict[str, object]):
        paths = [Path(str(p)) for p in context.get("figure_table_paths", [])]
        missing = [str(p) for p in paths if not p.exists() or p.stat().st_size == 0]
        if missing:
            return self.fail(missing, ["generate_figures_and_captions", "run_nonblank_output_check"])
        return self.pass_([str(p) for p in paths])
