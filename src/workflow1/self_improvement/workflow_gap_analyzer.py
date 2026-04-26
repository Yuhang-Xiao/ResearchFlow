from __future__ import annotations
from pathlib import Path

def analyze_gaps(root: Path = Path(".")) -> list[dict[str, str]]:
    checks = {
        "workflow self-improvement": root / "workflow_improvement",
        "workflow recipes": root / "workflow_recipes",
        "model registry": root / "model_registry",
        "self-improvement skills": root / "skills" / "workflow-self-improvement-scout",
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
