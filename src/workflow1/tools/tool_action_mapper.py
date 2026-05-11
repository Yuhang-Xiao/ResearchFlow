"""Map tool capability to Research OS actions."""

from __future__ import annotations


ACTION_TOOL_MAP = {
    "run_shap_or_fallback": ["shap", "sklearn_permutation_importance", "pdp_or_ale_fallback"],
    "train_models": ["sklearn", "xgboost_optional", "lightgbm_optional", "catboost_optional"],
    "run_automl_candidate": ["flaml_optional", "autogluon_optional", "pycaret_optional", "tpot_optional"],
    "build_zotero_evidence_chain": ["sidecar_bibtex_ris_csv", "zotero_write_requires_authorization"],
    "word_render_audit": ["python_docx", "libreoffice_optional"],
    "search_literature": ["local_references", "openalex_or_crossref_if_available", "web_metadata_if_allowed"],
}


def map_action_to_tools(action_name: str) -> list[str]:
    return ACTION_TOOL_MAP.get(action_name, [])
