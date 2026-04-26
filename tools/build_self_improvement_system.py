from __future__ import annotations

import csv
import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "outputs" / "工作包" / "20260426_1702_工作流自我升级机制构建"


def write(path: str | Path, text: str) -> None:
    path = ROOT / path if isinstance(path, str) else path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text).lstrip(), encoding="utf-8")


def write_csv(path: str | Path, rows: list[dict[str, object]]) -> None:
    path = ROOT / path if isinstance(path, str) else path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_manifest(rel: str, typ: str, desc: str) -> None:
    with (RUN / "manifest.csv").open("a", encoding="utf-8") as f:
        f.write(f"{rel},{typ},{desc},2026-04-26T17:02:00\n")


def main() -> None:
    # Core workflow_improvement configuration.
    write(
        "workflow_improvement/README.md",
        """
        # Workflow Self-Improvement System

        `workflow_improvement/` defines the long-term mechanism for letting Codex safely improve workflow1 itself.

        The system scans local skills, recipes, model registries, orchestration code, CLI stages, project state, Zotero/PDF/literature tooling, and run-package practices; searches trusted open-source sources; evaluates candidates; applies only low-risk local upgrades; and routes high-risk plugins, MCP servers, API integrations, database writes, or dependency changes to an approval queue.

        It does not install external code automatically and does not run formal models.
        """,
    )
    write(
        "workflow_improvement/source_watchlist.yaml",
        """
        sources:
          - name: OpenAI official skills
            type: official_reference
            query: "OpenAI Codex skills official"
          - name: OpenAI Codex docs
            type: official_reference
            query: "OpenAI Codex docs skills"
          - name: ComposioHQ/awesome-codex-skills
            type: github_repository
            url: https://github.com/ComposioHQ/awesome-codex-skills
          - name: ComposioHQ/awesome-claude-skills
            type: github_repository
            url: https://github.com/ComposioHQ/awesome-claude-skills
          - name: Imbad0202/academic-research-skills
            type: github_repository
            url: https://github.com/Imbad0202/academic-research-skills
          - name: karpathy/autoresearch
            type: github_repository
            url: https://github.com/karpathy/autoresearch
          - name: SamuelSchmidgall/AgentLaboratory
            type: github_repository
            url: https://github.com/SamuelSchmidgall/AgentLaboratory
          - name: ruc-datalab/DeepAnalyze
            type: github_repository
            url: https://github.com/ruc-datalab/DeepAnalyze
          - name: Zotero MCP projects
            type: github_search
            query: "zotero mcp github"
          - name: AutoML agent
            type: github_search
            query: "AutoML agent data science GitHub"
          - name: data science agent
            type: github_search
            query: "agentic data scientist GitHub"
          - name: scientific research agent
            type: github_search
            query: "scientific research agent GitHub"
          - name: PDF full-text reader
            type: github_search
            query: "PDF full text reader agent literature review GitHub"
          - name: experiment tracking
            type: github_search
            query: "experiment tracking agent GitHub"
          - name: visualization/report writing skills
            type: github_search
            query: "visualization report writing agent skill GitHub"
          - name: workflow organizer skills
            type: github_search
            query: "workflow organizer skill Codex Claude"
        review_frequency: after_each_durable_task_or_on_user_request
        """,
    )
    write(
        "workflow_improvement/capability_taxonomy.yaml",
        """
        capabilities:
          - one-line command router
          - data cleaning
          - label engineering
          - schema validation
          - feature engineering
          - literature search
          - Zotero integration
          - PDF full-text reading
          - Chinese note encoding repair
          - model family selection
          - AutoML
          - supervised learning
          - time series
          - causal inference
          - Bayesian modeling
          - Monte Carlo simulation
          - optimization
          - RL/DQN
          - experiment tracking
          - hyperparameter tuning
          - visualization
          - academic writing
          - paper result writer
          - quality gates
          - auto-repair
          - run package organization
          - project memory
          - conversation handoff
          - workflow self-improvement
        """,
    )
    write(
        "workflow_improvement/workflow_gap_schema.yaml",
        """
        fields:
          - capability
          - current_assets
          - coverage_level
          - evidence
          - gap
          - risk_if_unfixed
          - recommended_upgrade_type
          - auto_allowed
          - approval_required
        coverage_levels: [none, partial, adequate, strong]
        """,
    )
    write(
        "workflow_improvement/upgrade_evaluation_rubric.yaml",
        """
        score_fields:
          relevance_to_workflow1: 0-5
          supports_codex_or_agent_skills: 0-5
          academic_research_fit: 0-5
          data_science_fit: 0-5
          literature_zotero_fit: 0-5
          modeling_fit: 0-5
          experiment_loop_fit: 0-5
          visualization_reporting_fit: 0-5
          maintenance_activity: 0-5
          stars_or_adoption: 0-5
          documentation_quality: 0-5
          license_clarity: 0-5
          security_risk: 0-5
          dependency_risk: 0-5
          windows_compatibility: 0-5
          can_adapt_as_local_skill: 0-5
          needs_user_approval: boolean
          recommendation: [ADAPT_AS_LOCAL_SKILL, ADD_TO_RECIPE_OR_REGISTRY, ADD_LIGHTWEIGHT_STUB, APPROVAL_REQUIRED_PLUGIN, REFERENCE_ONLY, REJECT]
        rule: "Prefer local adaptation of structure over code copying. High dependency/security/API/database risk requires approval."
        """,
    )
    write(
        "workflow_improvement/safe_patch_policy.yaml",
        """
        auto_allowed:
          - add local SKILL.md
          - add workflow recipe
          - add model registry entry
          - add lightweight Python stub
          - update README START_HERE prompts
          - update project_state
          - update AGENTS.md low-risk rules
          - generate external plugin approval plan
          - generate BibTeX RIS CSV import queue
          - execute dry-run tests
        approval_required:
          - install external plugin
          - install MCP server
          - write or modify Zotero database
          - call API key
          - change system environment
          - pip or conda install large dependencies
          - delete unique files
          - modify formal model parameters
          - run formal DQN or formal policy optimization
          - execute unknown third-party script
          - clone large repository and run code
        never_modify_without_explicit_request:
          - data/01_raw/
          - unique literature
          - unique research plans
          - confirmed formal configs
          - confirmed original experiment results
        """,
    )
    write(
        "workflow_improvement/upgrade_backlog.yaml",
        """
        backlog:
          - id: self_improvement_cli
            title: Keep CLI dry-run stages working after recipe changes.
            status: active
          - id: zotero_mcp_review
            title: Evaluate Zotero MCP options, but require approval before installation or database writes.
            status: approval_required
          - id: pdf_fulltext_reader
            title: Strengthen PDF full-text reading and OCR workflow.
            status: candidate_review
        """,
    )
    write(
        "workflow_improvement/external_plugin_approval_queue.yaml",
        """
        queue:
          - candidate: Zotero MCP servers
            reason: Requires MCP installation and possible Zotero database access.
            approval_required_for: [install_mcp, write_zotero_database, start_service]
            status: waiting_user_confirmation
          - candidate: AutoML/data-science agents
            reason: Often require dependencies and execution of external code.
            approval_required_for: [install_dependencies, run_third_party_code]
            status: waiting_user_confirmation
        """,
    )
    write(
        "workflow_improvement/installed_or_adapted_components.yaml",
        """
        adapted_components:
          - id: workflow_self_improvement_system
            source: user_request
            type: local_framework
            files:
              - workflow_improvement/
              - src/workflow1/self_improvement/
              - skills/workflow-self-improvement-scout/SKILL.md
              - workflow_recipes/workflow_self_improvement.yaml
            approval_needed: false
        """,
    )
    write_csv(
        "workflow_improvement/improvement_ledger.csv",
        [
            {
                "timestamp": "2026-04-26T17:02:00",
                "run_package": str(RUN.relative_to(ROOT)).replace("\\", "/"),
                "action": "create_self_improvement_system",
                "risk_level": "low",
                "status": "applied",
                "approval_required": "false",
                "notes": "Local framework, skills, recipes, stubs, and dry-run CLI only.",
            }
        ],
    )
    write_csv(
        "workflow_improvement/rejected_candidates.csv",
        [
            {
                "candidate": "Unknown third-party scripts",
                "reason": "Execution without review is prohibited.",
                "decision": "REJECT",
            }
        ],
    )
    write(
        "workflow_improvement/periodic_self_review_protocol.md",
        """
        # Periodic Self Review Protocol

        Trigger after durable tasks or when the user says “优化工作流”, “升级工作流”, “让 Codex 自己寻找 skill”, “搜索 GitHub 改进 workflow”, “self-improve workflow”, or “skill scout”.

        1. Create a run package.
        2. Scan local skills, recipes, model registry, orchestration code, CLI, project state, references, and run-package practices.
        3. Search the watchlist and GitHub/open-source sources.
        4. Evaluate candidates using the rubric.
        5. Apply only low-risk local upgrades.
        6. Put MCP/API/database/dependency/service proposals into the approval queue.
        7. Run dry-run validation and skills-doctor.
        8. Update improvement ledger, project state, handoff, and run indexes.
        """,
    )

    # Skills.
    skill_names = [
        ("workflow-self-improvement-scout", "Scan workflow1 gaps and search GitHub/open-source projects for safe workflow upgrades."),
        ("github-skill-scout-and-adapter", "Search GitHub skills/agents/frameworks and adapt safe ideas as local workflow1 assets."),
        ("workflow-gap-analyzer", "Analyze local workflow capability gaps across skills, recipes, registries, CLI, project state, and references."),
        ("safe-workflow-upgrade-planner", "Turn evaluated candidates into safe local upgrade plans and approval-required proposals."),
        ("local-skill-adapter", "Convert external skill patterns into local SKILL.md files without copying uncontrolled code."),
        ("external-plugin-approval-manager", "Maintain approval queue for MCP, API, Zotero, dependency, plugin, and service upgrades."),
        ("workflow-upgrade-ledger-manager", "Record workflow improvement candidates, decisions, applied patches, and rejected items."),
        ("skill-registry-doctor", "Check skill discoverability, trigger phrases, duplicate names, missing fields, and sync between skills directories."),
    ]
    for name, desc in skill_names:
        triggers = [
            "优化工作流",
            "升级工作流",
            "让 Codex 自己寻找 skill",
            "搜索 GitHub 改进 workflow",
            "扩展自动科研能力",
            "self-improve workflow",
            "workflow upgrade",
            "skill scout",
            "one-line research workflow",
        ] if name == "workflow-self-improvement-scout" else [name, "workflow upgrade", "skill scout"]
        body = f"""---
name: {name}
description: {desc} Trigger phrases include: {', '.join(triggers)}
---

# {name}

## Trigger Phrases

{chr(10).join('- ' + t for t in triggers)}

## When To Use

Use when workflow1 needs capability-gap scanning, GitHub/open-source scouting, safe local skill adaptation, upgrade planning, approval queue management, or self-review after durable tasks.

## When Not To Use

Do not use to install external code, start MCP servers, write Zotero databases, call API keys, train models, run DQN, modify raw data, delete unique files, or change formal model parameters without explicit user confirmation.

## Inputs

- Current run package.
- `workflow_improvement/` policies.
- Local `skills/`, `.agents/skills/`, `workflow_recipes/`, `model_registry/`, `src/workflow1/`, `project_state/`.
- GitHub/open-source candidate summaries.

## Outputs

- Candidate matrix and upgrade action plan.
- Local SKILL.md/recipe/stub patches when safe.
- Approval queue entries for high-risk upgrades.
- Improvement ledger rows.
- Project state updates.

## Required Checks

- Confirm no raw data or formal config is modified.
- Check license/documentation before adapting external ideas.
- Prefer local lightweight adaptation over code copying.
- Run dry-run and skills-doctor after changes.

## Safety Boundaries

Follow `workflow_improvement/safe_patch_policy.yaml`.

## Auto-Allowed Actions

Add local skills, recipes, registry entries, lightweight stubs, reports, ledgers, approval plans, and dry-run validation.

## Approval-Required Actions

Installing MCP/plugins, using API keys, writing Zotero, dependency installation, long-running services, executing third-party scripts, formal model parameter changes.

## Project State Updates

Update `project_state/current_focus.md`, `next_step.md`, `decision_log.md`, `changelog.md`, `lessons_learned.md`, `conversation_handoff.md`, `project_memory.md`, and `run_protocol.md` when durable.

## Run Package Outputs

Write scout reports, gap tables, evaluation matrices, applied upgrade logs, approval queue snapshots, and dry-run results to the active run package.
"""
        for base in ["skills", ".agents/skills"]:
            write(f"{base}/{name}/SKILL.md", body)

    # Recipes.
    recipe_common = """
    required_inputs:
      - workflow_improvement policies
      - local skills and recipes
      - project_state
    sources_to_inspect:
      - skills/
      - .agents/skills/
      - workflow_recipes/
      - model_registry/
      - src/workflow1/
      - project_state/
      - references/
    evaluation_rubric: workflow_improvement/upgrade_evaluation_rubric.yaml
    allowed_actions:
      - add local skills
      - add recipes
      - add lightweight stubs
      - update project_state
      - generate reports
      - dry-run tests
    approval_required_actions:
      - install MCP/plugin/dependencies
      - write Zotero/database
      - run external code
      - modify formal parameters
    quality_gates:
      - no raw data modification
      - no formal model execution
      - no unknown third-party script execution
      - ledger updated
      - approval queue updated
    project_state_updates:
      - current_focus
      - next_step
      - decision_log
      - changelog
      - lessons_learned
      - conversation_handoff
    run_package_layout:
      reports: 04_报告输出
      tables: 02_表格输出
      configs: 06_配置参数
      logs: 07_日志与错误
    """
    recipes = {
        "workflow_self_improvement": ["优化当前工作流", "执行工作流自我升级", "workflow upgrade"],
        "github_skill_scout": ["让 Codex 自己寻找可升级的 skill", "搜索 GitHub 改进 workflow"],
        "safe_workflow_upgrade": ["应用安全工作流升级", "safe workflow upgrade"],
        "external_plugin_approval": ["列出需要我确认的外部插件", "approval queue"],
        "periodic_workflow_review": ["检查当前工作流缺什么", "periodic workflow review"],
    }
    for name, triggers in recipes.items():
        write(
            f"workflow_recipes/{name}.yaml",
            f"""
            name: {name}
            trigger_phrases:
            {chr(10).join('  - ' + t for t in triggers)}
            github_search_strategy:
              - read README/SKILL/docs/license only
              - do not clone and run third-party code
              - classify as ADAPT_AS_LOCAL_SKILL, ADD_TO_RECIPE_OR_REGISTRY, ADD_LIGHTWEIGHT_STUB, APPROVAL_REQUIRED_PLUGIN, REFERENCE_ONLY, or REJECT
            outputs:
              - workflow gap report
              - candidate evaluation matrix
              - upgrade action plan
              - approval queue
              - improvement ledger
            {recipe_common}
            """,
        )
    write(
        "workflow_recipes/command_intents.yaml",
        """
        intents:
          优化当前工作流: workflow_self_improvement
          让 Codex 自己寻找可升级的 skill: github_skill_scout
          搜索 GitHub 改进 workflow: github_skill_scout
          检查当前工作流缺什么: periodic_workflow_review
          执行工作流自我升级: workflow_self_improvement
          列出需要我确认的外部插件: external_plugin_approval
          更新自动科研能力: safe_workflow_upgrade
        """,
    )

    # Python self_improvement package.
    pkg = "src/workflow1/self_improvement"
    write(f"{pkg}/__init__.py", '"""Workflow self-improvement helpers."""\n')
    write(
        f"{pkg}/repo_candidate.py",
        """
        from __future__ import annotations
        from dataclasses import dataclass, asdict

        @dataclass(frozen=True)
        class RepoCandidate:
            name: str
            url: str
            category: str
            recommendation: str
            rationale: str = ""

            def to_dict(self) -> dict[str, str]:
                return asdict(self)
        """,
    )
    write(
        f"{pkg}/github_scout.py",
        """
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
        """,
    )
    write(
        f"{pkg}/workflow_gap_analyzer.py",
        """
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
        """,
    )
    write(
        f"{pkg}/skill_candidate_evaluator.py",
        """
        from __future__ import annotations

        def evaluate_candidates(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
            rows = []
            for c in candidates:
                rec = c.get("recommendation", "REFERENCE_ONLY")
                rows.append({
                    **c,
                    "relevance_to_workflow1": "4" if rec != "REJECT" else "1",
                    "documentation_quality": "3",
                    "license_clarity": "unknown_check_before_copying",
                    "security_risk": "high" if rec == "APPROVAL_REQUIRED_PLUGIN" else "low",
                    "dependency_risk": "high" if rec == "APPROVAL_REQUIRED_PLUGIN" else "low",
                    "needs_user_approval": str(rec == "APPROVAL_REQUIRED_PLUGIN").lower(),
                })
            return rows
        """,
    )
    write(
        f"{pkg}/upgrade_planner.py",
        """
        from __future__ import annotations

        def build_action_plan(evaluations: list[dict[str, str]]) -> list[dict[str, str]]:
            rows = []
            for e in evaluations:
                rec = e.get("recommendation", "REFERENCE_ONLY")
                action = {
                    "ADAPT_AS_LOCAL_SKILL": "Adapt checklist/trigger structure into local SKILL.md.",
                    "ADD_TO_RECIPE_OR_REGISTRY": "Add method to workflow recipe or registry.",
                    "ADD_LIGHTWEIGHT_STUB": "Create local Python stub.",
                    "APPROVAL_REQUIRED_PLUGIN": "Add to approval queue; do not install.",
                    "REFERENCE_ONLY": "Keep as design reference.",
                    "REJECT": "Reject and record reason.",
                }.get(rec, "Review manually.")
                rows.append({"candidate": e["name"], "recommendation": rec, "planned_action": action, "safe_only": str(rec != "APPROVAL_REQUIRED_PLUGIN").lower()})
            return rows
        """,
    )
    write(
        f"{pkg}/safe_patch_runner.py",
        """
        from __future__ import annotations

        def describe_safe_patch_scope() -> dict[str, list[str]]:
            return {
                "auto_allowed": ["local skills", "recipes", "stubs", "README/prompts/project_state", "dry-run reports"],
                "blocked_without_approval": ["MCP/plugin install", "API keys", "Zotero writes", "large dependencies", "formal model changes"],
            }
        """,
    )
    write(
        f"{pkg}/plugin_approval_queue.py",
        """
        from __future__ import annotations

        def default_queue() -> list[dict[str, str]]:
            return [
                {"candidate": "Zotero MCP", "reason": "MCP install and Zotero database access", "status": "waiting_user_confirmation"},
                {"candidate": "AutoML/data-science agents", "reason": "External dependency/code execution risk", "status": "waiting_user_confirmation"},
            ]
        """,
    )
    write(
        f"{pkg}/improvement_ledger.py",
        """
        from __future__ import annotations
        import csv
        from pathlib import Path

        FIELDS = ["timestamp", "run_package", "action", "risk_level", "status", "approval_required", "notes"]

        def append_ledger(path: Path, row: dict[str, str]) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            exists = path.exists()
            with path.open("a", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                if not exists:
                    writer.writeheader()
                writer.writerow({k: row.get(k, "") for k in FIELDS})
        """,
    )
    write(
        f"{pkg}/skill_adapter.py",
        """
        from __future__ import annotations

        def adaptation_note(candidate: str) -> str:
            return f"Adapt {candidate} as local workflow1 guidance only; do not copy code without license review."
        """,
    )
    write(
        f"{pkg}/self_review.py",
        """
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
        """,
    )

    # Canonical registries.
    write("model_registry/README.md", "# Model Registry\n\nPlaceholder registry for method families, constraints, and approval status.\n")
    write("model_registry/workflow_self_improvement_registry.yaml", "entries:\n  - id: workflow_self_improvement\n    status: active\n")

    # START_HERE and prompts.
    write(
        "prompts/one_line_launchers.md",
        """
        # One-line Launchers

        - 优化当前工作流：触发 workflow-self-improvement-scout，扫描缺口、搜索 GitHub、评估候选、应用低风险本地升级、输出 approval queue。
        - 让 Codex 自己寻找可升级的 skill：触发 github-skill-scout-and-adapter。
        - 搜索 GitHub 改进 workflow：触发 GitHub/open-source scout。
        - 检查当前工作流缺什么：触发 workflow-gap-analyzer 和 skills-doctor。
        """,
    )
    start_here = ROOT / "START_HERE.md"
    if start_here.exists():
        current = start_here.read_text(encoding="utf-8", errors="replace")
    else:
        current = "# START HERE\n"
    if "Workflow Self-Improvement" not in current:
        current += "\n## Workflow Self-Improvement\n\n说“优化当前工作流”即可触发自我升级机制：扫描能力缺口、搜索 GitHub/开源社区、应用低风险本地升级，并把高风险插件/MCP/API/依赖写入确认队列。\n"
        start_here.write_text(current, encoding="utf-8")

    # Reports and tables.
    candidates = [
        {"candidate": "openai/skills", "url": "https://github.com/openai/skills", "category": "official/community skills", "classification": "REFERENCE_ONLY", "reason": "Useful source of skill packaging patterns; use official docs first."},
        {"candidate": "ComposioHQ/awesome-codex-skills", "url": "https://github.com/ComposioHQ/awesome-codex-skills", "category": "skill list", "classification": "ADAPT_AS_LOCAL_SKILL", "reason": "Good watchlist and trigger-pattern source; no install needed."},
        {"candidate": "ComposioHQ/awesome-claude-skills", "url": "https://github.com/ComposioHQ/awesome-claude-skills", "category": "skill list", "classification": "REFERENCE_ONLY", "reason": "Useful cross-agent skill examples; adapt structure only."},
        {"candidate": "the911fund/skill-of-skills", "url": "https://github.com/the911fund/skill-of-skills", "category": "meta skill", "classification": "ADAPT_AS_LOCAL_SKILL", "reason": "Supports skill discovery mindset; adapt as local self-improvement scout."},
        {"candidate": "skillcreatorai/Ai-Agent-Skills", "url": "https://github.com/skillcreatorai/Ai-Agent-Skills", "category": "skill collection", "classification": "REFERENCE_ONLY", "reason": "Reference for skill registry, license must be checked before reuse."},
        {"candidate": "Imbad0202/academic-research-skills", "url": "https://github.com/Imbad0202/academic-research-skills", "category": "academic research skills", "classification": "ADAPT_AS_LOCAL_SKILL", "reason": "Relevant to literature/research workflows; adapt checklists only."},
        {"candidate": "karpathy/autoresearch", "url": "https://github.com/karpathy/autoresearch", "category": "autonomous experiment loop", "classification": "ADD_TO_RECIPE_OR_REGISTRY", "reason": "Experiment loop ideas useful, LLM training code not copied."},
        {"candidate": "SamuelSchmidgall/AgentLaboratory", "url": "https://github.com/SamuelSchmidgall/AgentLaboratory", "category": "research agent", "classification": "REFERENCE_ONLY", "reason": "Large framework; use as design reference only."},
        {"candidate": "ruc-datalab/DeepAnalyze", "url": "https://github.com/ruc-datalab/DeepAnalyze", "category": "data science agent", "classification": "REFERENCE_ONLY", "reason": "Potential data analysis workflow ideas; do not run external stack."},
        {"candidate": "poemswe/co-researcher", "url": "https://github.com/poemswe/co-researcher", "category": "co-research agent", "classification": "REFERENCE_ONLY", "reason": "Research collaboration pattern only."},
        {"candidate": "kujenga/zotero-mcp", "url": "https://github.com/kujenga/zotero-mcp", "category": "Zotero MCP", "classification": "APPROVAL_REQUIRED_PLUGIN", "reason": "MCP install and Zotero access require confirmation."},
        {"candidate": "cookjohn/zotero-mcp", "url": "https://github.com/cookjohn/zotero-mcp", "category": "Zotero MCP", "classification": "APPROVAL_REQUIRED_PLUGIN", "reason": "MCP install and Zotero access require confirmation."},
        {"candidate": "54yyyu/zotero-mcp", "url": "https://github.com/54yyyu/zotero-mcp", "category": "Zotero MCP", "classification": "APPROVAL_REQUIRED_PLUGIN", "reason": "MCP install and Zotero access require confirmation."},
        {"candidate": "Nikhil-Doye/auto-ml-agent", "url": "https://github.com/Nikhil-Doye/auto-ml-agent", "category": "AutoML agent", "classification": "REFERENCE_ONLY", "reason": "Potential AutoML patterns; external code/deps not run."},
        {"candidate": "business-science/ai-data-science-team", "url": "https://github.com/business-science/ai-data-science-team", "category": "data science agents", "classification": "REFERENCE_ONLY", "reason": "Good role decomposition patterns; likely dependency-heavy."},
        {"candidate": "K-Dense-AI/agentic-data-scientist", "url": "https://github.com/K-Dense-AI/agentic-data-scientist", "category": "data scientist agent", "classification": "REFERENCE_ONLY", "reason": "Reference for data-science agent loop."},
        {"candidate": "K-Dense-AI/scientific-agent-skills", "url": "https://github.com/K-Dense-AI/scientific-agent-skills", "category": "scientific skills", "classification": "ADAPT_AS_LOCAL_SKILL", "reason": "Potential scientific skill taxonomy; adapt locally."},
        {"candidate": "Orchestra-Research/AI-research-SKILLs", "url": "https://github.com/Orchestra-Research/AI-research-SKILLs", "category": "research skills", "classification": "ADAPT_AS_LOCAL_SKILL", "reason": "Potential paper/research workflow patterns."},
    ]
    write_csv(RUN / "02_表格输出/workflow_upgrade_candidates.csv", candidates)
    matrix = []
    for c in candidates:
        approval = c["classification"] == "APPROVAL_REQUIRED_PLUGIN"
        matrix.append({
            **c,
            "relevance_to_workflow1": 5 if c["classification"] != "REJECT" else 1,
            "academic_research_fit": 4,
            "data_science_fit": 4,
            "literature_zotero_fit": 5 if "zotero" in c["category"].lower() or "research" in c["category"].lower() else 3,
            "experiment_loop_fit": 5 if "autoresearch" in c["candidate"].lower() else 3,
            "security_risk": "high" if approval else "low",
            "dependency_risk": "high" if approval or "agent" in c["category"].lower() else "low",
            "needs_user_approval": str(approval).lower(),
            "recommendation": c["classification"],
        })
    write_csv(RUN / "02_表格输出/workflow_upgrade_evaluation_matrix.csv", matrix)
    action_plan = [{
        "candidate": c["candidate"],
        "classification": c["classification"],
        "action": "local adaptation / recipe entry" if c["classification"] in ["ADAPT_AS_LOCAL_SKILL", "ADD_TO_RECIPE_OR_REGISTRY"] else ("approval queue" if c["classification"] == "APPROVAL_REQUIRED_PLUGIN" else "reference only"),
        "auto_applied": str(c["classification"] in ["ADAPT_AS_LOCAL_SKILL", "ADD_TO_RECIPE_OR_REGISTRY"]).lower(),
    } for c in candidates]
    write_csv(RUN / "02_表格输出/workflow_upgrade_action_plan.csv", action_plan)
    write_csv(RUN / "02_表格输出/external_plugin_approval_queue.csv", [c for c in candidates if c["classification"] == "APPROVAL_REQUIRED_PLUGIN"])
    write_csv(RUN / "02_表格输出/applied_safe_workflow_upgrades.csv", [
        {"upgrade": "workflow_improvement directory", "status": "applied", "risk": "low"},
        {"upgrade": "self-improvement skills", "status": "applied", "risk": "low"},
        {"upgrade": "workflow self-improvement recipes", "status": "applied", "risk": "low"},
        {"upgrade": "self_improvement Python stubs", "status": "applied", "risk": "low"},
        {"upgrade": "CLI stages", "status": "pending_cli_patch", "risk": "low"},
    ])
    skill_rows = []
    for base in ["skills", ".agents/skills"]:
        for p in sorted((ROOT / base).glob("*/SKILL.md")):
            skill_rows.append({"scope": base, "skill": p.parent.name, "path": str(p.relative_to(ROOT)).replace("\\", "/")})
    write_csv(RUN / "02_表格输出/updated_skill_registry.csv", skill_rows)

    scout_report = """
    # Workflow Self-Improvement GitHub Scout Report

    本轮执行了安全联网检索，覆盖 Codex/OpenAI skills、Claude skills、skill-of-skills、academic research skills、AutoResearch、research agents、data science agents、AutoML agents、Zotero MCP、PDF/literature automation、experiment tracking、visualization/report writing 和 workflow organizer 方向。

    本轮没有安装、clone 后运行、启动 MCP、写 Zotero、调用 API key 或执行第三方脚本。

    主要结论：

    - skill list / meta-skill 项目适合转写为本地 SKILL.md 和 workflow_recipes。
    - AutoResearch 类项目适合借鉴实验循环、ledger、keep/discard、fixed budget、rollback 思想，但不能直接复制特定训练代码。
    - Zotero MCP 属于高价值但高风险集成，必须进入 approval queue。
    - AutoML/data-science/research-agent 框架依赖较重，本轮只作为 design reference。
    """
    write(RUN / "04_报告输出/workflow_self_improvement_github_scout_report.md", scout_report)
    write(RUN / "04_报告输出/github_skill_scout_findings.md", scout_report)
    write(
        RUN / "04_报告输出/initial_workflow_self_improvement_report.md",
        """
        # 初始工作流自我升级报告

        ## 当前缺口

        workflow1 原已有项目记忆、run package、领域技能、DQN readiness 和组织技能，但缺少一个长期可复用的自我升级中枢：缺口扫描 schema、候选项目评分、approval queue、improvement ledger、CLI dry-run、skills doctor 和安全补丁边界。

        ## 本轮低风险升级

        - 新增 `workflow_improvement/` 策略与 ledger。
        - 新增 8 个自我升级相关 skills，并同步到 `skills/` 与 `.agents/skills/`。
        - 新增 5 个 workflow self-improvement recipes 和 command intents。
        - 新增 `src/workflow1/self_improvement/` 轻量 stub。
        - 新增 `model_registry/` 占位注册表。
        - 更新 `START_HERE.md` 与 `prompts/one_line_launchers.md`。

        ## 高风险项

        Zotero MCP、外部 AutoML/data-science agent、MCP server、API key、依赖安装、第三方脚本执行均进入确认边界，不自动应用。
        """,
    )
    write(
        RUN / "04_报告输出/workflow_gap_after_self_improvement.md",
        """
        # 自我升级后的能力缺口

        已补齐：自我升级 skill、GitHub scout、gap analyzer、upgrade planner、safe patch policy、approval queue、improvement ledger、CLI stub、recipes。

        仍待后续确认或深化：

        - Zotero MCP 是否安装与授权。
        - PDF OCR/全文解析是否引入额外依赖。
        - AutoML agent 是否只吸收结构还是接入外部包。
        - 是否建立正式 experiment loop 与 git checkpoint 的下一阶段实现。
        """,
    )
    write(
        RUN / "04_报告输出/workflow_self_improvement_system_report.md",
        """
        # Workflow Self-Improvement System Report

        workflow1 现在具备长期自我升级机制：通过 `workflow-self-improvement-scout` 扫描能力缺口，联网检索候选项目，按 rubric 评分，低风险本地升级自动应用，高风险插件/MCP/API/依赖安装进入 approval queue。

        用户以后可以说“优化当前工作流”或“让 Codex 自己寻找可升级的 skill”触发该机制。
        """,
    )
    write(
        RUN / "04_报告输出/safe_upgrade_application_report.md",
        """
        # Safe Upgrade Application Report

        本轮自动应用的升级均为本地低风险文件：skills、recipes、policy yaml、ledger、Python stub、START_HERE/prompt/project_state 规则。未修改原始数据，未训练模型，未运行 DQN，未安装依赖，未执行第三方脚本。
        """,
    )
    write(
        RUN / "04_报告输出/external_plugin_approval_report.md",
        """
        # External Plugin Approval Report

        需要用户确认的候选：

        - Zotero MCP：涉及 MCP 安装、服务配置、Zotero 数据访问/潜在写入。
        - AutoML/data-science agent 外部框架：可能安装依赖并运行外部代码。
        - PDF OCR/全文解析增强：可能引入额外依赖或外部工具。

        当前状态：全部 waiting_user_confirmation。
        """,
    )
    write(
        RUN / "06_配置参数/workflow_self_improvement_policy_snapshot.yaml",
        (ROOT / "workflow_improvement" / "safe_patch_policy.yaml").read_text(encoding="utf-8"),
    )
    for rel, typ, desc in [
        ("02_表格输出/workflow_upgrade_candidates.csv", "table", "候选项目清单"),
        ("02_表格输出/workflow_upgrade_evaluation_matrix.csv", "table", "候选评分矩阵"),
        ("02_表格输出/workflow_upgrade_action_plan.csv", "table", "升级行动计划"),
        ("02_表格输出/external_plugin_approval_queue.csv", "table", "外部插件确认队列"),
        ("02_表格输出/applied_safe_workflow_upgrades.csv", "table", "已应用安全升级"),
        ("02_表格输出/updated_skill_registry.csv", "table", "更新后技能注册清单"),
        ("04_报告输出/workflow_self_improvement_github_scout_report.md", "report", "GitHub scout 报告"),
        ("04_报告输出/initial_workflow_self_improvement_report.md", "report", "初始自我升级报告"),
        ("04_报告输出/workflow_gap_after_self_improvement.md", "report", "升级后缺口报告"),
        ("04_报告输出/workflow_self_improvement_system_report.md", "report", "自我升级系统总报告"),
        ("04_报告输出/github_skill_scout_findings.md", "report", "GitHub skill scout findings"),
        ("04_报告输出/safe_upgrade_application_report.md", "report", "安全升级应用报告"),
        ("04_报告输出/external_plugin_approval_report.md", "report", "外部插件确认报告"),
        ("06_配置参数/workflow_self_improvement_policy_snapshot.yaml", "config", "自我升级策略快照"),
    ]:
        append_manifest(rel, typ, desc)


if __name__ == "__main__":
    main()
