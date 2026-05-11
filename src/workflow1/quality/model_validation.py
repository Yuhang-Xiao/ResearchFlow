"""Model validation and comparison guards."""
from __future__ import annotations


def audit_model_comparison(rows: list[dict]) -> dict:
    baselines = [r for r in rows if str(r.get("model_role", "")).lower() == "baseline"]
    comparable = all(r.get("split_id") == rows[0].get("split_id") for r in rows) if rows else False
    required = ["primary_metric", "secondary_metrics", "uncertainty", "runtime", "parameter_count", "interpretability", "paper_usable"]
    missing = sorted({field for r in rows for field in required if field not in r or r.get(field) in {"", None}})
    status = "pass" if rows and baselines and comparable and not missing else "fail"
    return {"status": status, "baseline_count": len(baselines), "same_split": comparable, "missing_fields": missing}
