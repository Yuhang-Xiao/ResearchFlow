from __future__ import annotations
from pathlib import Path
from .github_scout import scout_candidates
from .skill_candidate_evaluator import evaluate_candidates
from .upgrade_planner import build_action_plan
from .workflow_gap_analyzer import analyze_gaps
from .plugin_approval_queue import default_queue

def run_self_review(root: Path = Path(".")) -> dict[str, object]:
    gaps = analyze_gaps(root)
    candidates = scout_candidates()
    evaluations = evaluate_candidates(candidates)
    plan = build_action_plan(evaluations)
    return {
        "status": "ok",
        "gaps": gaps,
        "candidates": candidates,
        "evaluations": evaluations,
        "plan": plan,
        "approval_queue": default_queue(),
    }
