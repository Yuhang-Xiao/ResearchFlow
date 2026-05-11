from __future__ import annotations

def describe_safe_patch_scope() -> dict[str, list[str]]:
    return {
        "auto_allowed": ["local skills", "recipes", "stubs", "README, framework prompts, project_state", "dry-run reports"],
        "blocked_without_approval": ["MCP/plugin install", "API keys", "Zotero writes", "large dependencies", "formal model changes"],
    }
