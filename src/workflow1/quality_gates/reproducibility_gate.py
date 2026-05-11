"""Gate: reproducibility package is complete."""

from __future__ import annotations

from pathlib import Path

from workflow1.quality_gates.base import QualityGate


class ReproducibilityGate(QualityGate):
    gate_name = "ReproducibilityGate"
    required = ["manifest.csv", "reproducibility_README.md"]

    def run(self, context: dict[str, object]):
        root = Path(str(context.get("package_dir", "")))
        missing = [name for name in self.required if not (root / name).exists()]
        if missing:
            return self.fail(missing, ["write_reproducibility_readme_and_manifest"])
        return self.pass_([str(root / name) for name in self.required])
