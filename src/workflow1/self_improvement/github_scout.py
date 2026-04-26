from __future__ import annotations
from pathlib import Path

DEFAULT_CANDIDATES = [
    ("openai/skills", "https://github.com/openai/skills", "Codex skills", "REFERENCE_ONLY"),
    ("ComposioHQ/awesome-codex-skills", "https://github.com/ComposioHQ/awesome-codex-skills", "skill registry", "ADAPT_AS_LOCAL_SKILL"),
    ("ComposioHQ/awesome-claude-skills", "https://github.com/ComposioHQ/awesome-claude-skills", "skill registry", "REFERENCE_ONLY"),
    ("karpathy/autoresearch", "https://github.com/karpathy/autoresearch", "experiment loop", "ADD_TO_RECIPE_OR_REGISTRY"),
    ("SamuelSchmidgall/AgentLaboratory", "https://github.com/SamuelSchmidgall/AgentLaboratory", "research agent", "REFERENCE_ONLY"),
    ("ruc-datalab/DeepAnalyze", "https://github.com/ruc-datalab/DeepAnalyze", "data science agent", "REFERENCE_ONLY"),
    ("kujenga/zotero-mcp", "https://github.com/kujenga/zotero-mcp", "Zotero MCP", "APPROVAL_REQUIRED_PLUGIN"),
]

def generate_queries(root: Path = Path(".")) -> list[str]:
    watch = root / "workflow_improvement" / "source_watchlist.yaml"
    base = ["Codex skills GitHub", "Zotero MCP GitHub", "scientific research agent GitHub", "AutoML agent GitHub"]
    return base + ([f"watchlist:{watch}"] if watch.exists() else [])

def scout_candidates() -> list[dict[str, str]]:
    return [
        {"name": n, "url": u, "category": c, "recommendation": r, "rationale": "Seed candidate from self-improvement watchlist."}
        for n, u, c, r in DEFAULT_CANDIDATES
    ]
