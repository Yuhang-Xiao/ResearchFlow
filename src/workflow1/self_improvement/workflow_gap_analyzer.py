from __future__ import annotations
from pathlib import Path

from workflow1.paths import framework_path

def analyze_gaps(root: Path = Path(".")) -> list[dict[str, str]]:
    checks = {
        "workflow self-improvement": framework_path("workflow_improvement"),
        "workflow recipes": framework_path("workflow_recipes"),
        "model registry": framework_path("model_registry"),
        "self-improvement skills": root / ".agents" / "skills" / "workflow-self-improvement-scout",
        "CLI self-improvement stages": root / "src" / "workflow1" / "self_improvement",
    }
    rows = []
    for cap, path in checks.items():
        exists = path.exists()
        rows.append({
            "capability": cap,
            "current_assets": str(path),
            "coverage_level": "adequate" if exists else "partial",
            "gap": "" if exists else f"Missing {path}",
            "recommended_upgrade_type": "none" if exists else "ADD_LIGHTWEIGHT_STUB",
            "auto_allowed": "true",
            "approval_required": "false",
        })
    return rows
