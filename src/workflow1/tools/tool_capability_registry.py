"""Registry of local and Codex-app tool capabilities."""

from __future__ import annotations

import importlib.util
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ToolCapability:
    tool: str
    available: bool
    capability: str
    safe_default_action: str
    requires_authorization_for: str
    codex_plugin_installed: bool = False
    callable_in_session: bool | None = None
    cli_available: bool = False
    public_api_fallback: bool = False
    notes: str = ""


TOOL_CAPABILITIES = {
    "shap": ("explainability", "run_shap_or_fallback", "installation"),
    "xgboost": ("gradient_boosting", "use_if_installed_else_fallback", "installation"),
    "lightgbm": ("gradient_boosting", "use_if_installed_else_fallback", "installation"),
    "catboost": ("gradient_boosting", "use_if_installed_else_fallback", "installation"),
    "flaml": ("automl", "use_if_installed_else_dependency_plan", "installation"),
    "autogluon": ("automl", "use_if_installed_else_dependency_plan", "installation"),
    "pycaret": ("automl", "use_if_installed_else_dependency_plan", "installation"),
    "tpot": ("automl", "use_if_installed_else_dependency_plan", "installation"),
    "docx": ("word_export", "use_python_docx", "none"),
    "openml": ("benchmark_reference", "metadata_reference_only", "installation_or_large_download"),
}

PLUGIN_SKILL_PATHS = {
    "github": Path(r"C:\Users\Administrator\.codex\plugins\cache\openai-curated\github\f9c12053\skills\github\SKILL.md"),
    "huggingface": Path(r"C:\Users\Administrator\.codex\plugins\cache\openai-curated\hugging-face\f9c12053\skills\cli\SKILL.md"),
}


def get_tool_capability_matrix() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for tool, (capability, action, auth) in TOOL_CAPABILITIES.items():
        rows.append(
            asdict(
                ToolCapability(
                    tool=tool,
                    available=importlib.util.find_spec(tool) is not None,
                    capability=capability,
                    safe_default_action=action,
                    requires_authorization_for=auth,
                    cli_available=shutil.which(tool) is not None,
                    notes="Python package availability controls local execution.",
                )
            )
        )
    for tool, cli_name, public_api in [
        ("github", "gh", True),
        ("huggingface", "hf", True),
    ]:
        plugin_installed = PLUGIN_SKILL_PATHS[tool].exists()
        cli_available = shutil.which(cli_name) is not None
        rows.append(
            asdict(
                ToolCapability(
                    tool=tool,
                    available=plugin_installed or cli_available or public_api,
                    capability="external_engineering_reference",
                    safe_default_action="prefer_codex_app_plugin_else_public_api_readonly_fallback",
                    requires_authorization_for="write_actions_private_repos_api_keys_large_downloads",
                    codex_plugin_installed=plugin_installed,
                    callable_in_session=None,
                    cli_available=cli_available,
                    public_api_fallback=public_api,
                    notes=(
                        "Codex app plugin is treated as installed when its skill bundle is present. "
                        "Missing gh/hf CLI must not be interpreted as plugin failure."
                    ),
                )
            )
        )
    return rows
