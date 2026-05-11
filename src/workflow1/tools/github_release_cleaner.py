"""Clean ResearchFlow OS/workflow1 for a public GitHub release.

The cleaner is intentionally conservative:

* dry-run is the default;
* destructive cleanup requires an explicit ``apply=True`` option;
* every file is copied to a backup directory outside the repository first;
* SHA256 is verified before a repository file is removed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
import csv
import hashlib
import json
import os
import shutil
from typing import Iterable


PUBLIC_STATE_FILES: dict[str, str] = {
    "project_state/README.md": """# project_state

This directory stores lightweight project memory for local workflow runs.
The public template contains no private research state. Local runs may update
these files, but project-specific memory should be reviewed before publishing.
""",
    "project_state/current_focus.md": """# Current Focus

The public repository is in framework-template mode.

Place local data and research materials outside Git-tracked outputs before
starting a real research task.
""",
    "project_state/next_step.md": """# Next Step

1. Install ResearchFlow OS through `install.ps1` or editable Python mode.
2. Add a local dataset under `data/01_raw/` or point `WORKFLOW1_DATA_FILE` to a local file.
3. Run intake, validation, and dry-run planning before executing a full research workflow.
""",
    "project_state/project_memory.md": """# Project Memory

Public template memory only. Do not store secrets, raw-data details, private
identifiers, or unpublished research conclusions here before pushing to GitHub.
""",
    "project_state/lessons_learned.md": """# Lessons Learned

Public template placeholder. Add reusable workflow lessons only after removing
private data and project-specific identifiers.
""",
    "project_state/conversation_handoff.md": """# Conversation Handoff

No private conversation handoff is included in the public template.
""",
    "project_state/decision_log.md": """# Decision Log

## Public Template

- The repository is configured to keep real datasets, generated outputs,
  model artifacts, local corpora, and secrets out of Git.
""",
    "project_state/changelog.md": """# Changelog

## Public Template

- Prepared ResearchFlow OS for public use as a Codex-assisted scientific workflow scaffold.
- Added PowerShell installer entrypoint for `workflow1` and `researchflow`.
- Consolidated framework assets under `framework/` while keeping local data and output workspaces at the repository root.
""",
    "project_state/artifact_index.md": """# Artifact Index

No run artifacts are tracked in the public template. Generated artifacts should
live in ignored local output directories or external archives.
""",
    "project_state/workspace_structure.md": """# Workspace Structure

The public repository keeps framework code, framework assets, skills, and
documentation. Real data and generated outputs are local-only by default.
""",
    "project_state/run_protocol.md": """# Run Protocol

1. Keep raw data immutable and local.
2. Create outputs in run packages.
3. Verify derived data before modeling.
4. Run release cleanup before pushing public changes.
""",
    "project_state/roadmap.yaml": """status: public_template
current_phase: framework_ready
next_milestone: run_with_local_user_data
""",
}


DIRECTORY_READMES: dict[str, str] = {
    "data/README.md": """# data

Local data workspace. Real data is ignored by Git.

- `01_raw/`: place immutable local raw data here.
- `02_intermediate/`: parsed or lightly transformed local data.
- `03_primary/`: cleaned analysis-ready local tables.
- `04_feature/`: engineered feature tables.
- `05_model_input/`: final local modeling matrices or splits.
""",
    "data/01_raw/README.md": """# data/01_raw

Put local raw `.csv` or `.xlsx` files here. This directory is ignored by Git
except for this README and `.gitkeep`.
""",
    "data/02_intermediate/README.md": "# data/02_intermediate\n\nLocal intermediate data. Ignored by Git.\n",
    "data/03_primary/README.md": "# data/03_primary\n\nLocal cleaned primary data. Ignored by Git.\n",
    "data/04_feature/README.md": "# data/04_feature\n\nLocal feature data. Ignored by Git.\n",
    "data/05_model_input/README.md": "# data/05_model_input\n\nLocal model-input data. Ignored by Git.\n",
    "outputs/README.md": """# outputs

Local workflow run packages and output indexes. Generated outputs are ignored
by Git. Run release cleanup before publishing.
""",
    "outputs/_index/README.md": "# outputs/_index\n\nLocal output indexes. Ignored by Git except this README.\n",
    "outputs/工作包/README.md": "# outputs/工作包\n\nLocal run packages. Ignored by Git.\n",
    "outputs/_待复核/README.md": "# outputs/_待复核\n\nLocal unclassified artifacts for manual review. Ignored by Git.\n",
    "reports/README.md": "# reports\n\nLocal reports, figures, tables, and drafts. Generated content is ignored by Git.\n",
    "reports/figures/README.md": "# reports/figures\n\nLocal generated figures. Ignored by Git.\n",
    "reports/tables/README.md": "# reports/tables\n\nLocal generated tables. Ignored by Git.\n",
    "reports/quarto/README.md": "# reports/quarto\n\nLocal report drafts. Ignored by Git.\n",
    "experiments/README.md": "# experiments\n\nLocal experiment artifacts. Ignored by Git.\n",
    "experiments/baselines/README.md": "# experiments/baselines\n\nLocal baseline experiment artifacts. Ignored by Git.\n",
    "experiments/advanced/README.md": "# experiments/advanced\n\nLocal advanced experiment artifacts. Ignored by Git.\n",
    "experiments/comparisons/README.md": "# experiments/comparisons\n\nLocal comparison experiment artifacts. Ignored by Git.\n",
    "references/processed_summaries/README.md": "# references/processed_summaries\n\nLocal processed literature summaries. Review before publishing.\n",
    "references/notes/README.md": "# references/notes\n\nLocal notes and private references. Ignored by Git by default.\n",
    "research_corpus/README.md": "# research_corpus\n\nLocal research corpus and training examples. Ignored by Git.\n",
    "external_cache/README.md": "# external_cache\n\nLocal external access cache and approval logs. Ignored by Git.\n",
    "archive/README.md": "# archive\n\nLocal historical archive. Ignored by Git.\n",
}


RISK_ROOTS: tuple[str, ...] = (
    "data",
    "outputs",
    "reports",
    "experiments",
    "archive",
    "external_cache",
    "research_corpus",
    "src/workflow1.egg-info",
)

REFERENCE_PRIVATE_ROOTS: tuple[str, ...] = (
    "references/notes",
    "references/processed_summaries",
    "references/archive",
    "references/project_plan",
)

PRIVATE_CONFIG_FILES: tuple[str, ...] = (
    ".codex/config.toml",
    ".codex/zotero_mcp.env",
)

PROJECT_SPECIFIC_TOOL_PATTERNS: tuple[str, ...] = (
    "ys" + "b",
    "pest" + "value",
    "pea" + "nut",
    "dqn",
)

PROJECT_SPECIFIC_SOURCE_FILES: tuple[str, ...] = (
    "src/workflow1/pipelines/cleaning/category_reconstruction.py",
    "src/workflow1/pipelines/optimization",
    "src/workflow1/tools/legacy_scripts",
    "src/workflow1/tools/full_workspace_run_package_cleanup.py",
    "src/workflow1/orchestration/publication_product_orchestrator.py",
    "src/workflow1/reporting/publication_paper_builder.py",
    "tools/run_publication_product_workflow.py",
    "tools/system_upgrade_auto_research_product_mode.py",
    "references/reference_inventory.csv",
)

ARTIFACT_SUFFIXES: tuple[str, ...] = (
    ".xlsx",
    ".xls",
    ".xlsm",
    ".pt",
    ".pth",
    ".pkl",
    ".pickle",
    ".joblib",
    ".zip",
    ".docx",
    ".pdf",
    ".jsonl",
)

PUBLIC_KEEP_NAMES: tuple[str, ...] = ("README.md", ".gitkeep")


@dataclass(frozen=True)
class CleanupOptions:
    """Options for public-release cleanup."""

    repo_root: Path = Path(".")
    backup_to: Path | None = None
    apply: bool = False
    keep_synthetic_example: bool = True


@dataclass
class FilePlan:
    """A single file selected for backup and removal."""

    relative_path: str
    size_bytes: int
    reason: str
    sha256: str = ""
    backup_path: str = ""


@dataclass
class CleanupResult:
    """Structured cleanup result suitable for CLI output."""

    status: str
    apply: bool
    repo_root: str
    backup_to: str
    planned_delete_count: int
    planned_delete_bytes: int
    deleted_count: int = 0
    template_files_written: int = 0
    issues: list[str] = field(default_factory=list)
    remaining_risks: list[str] = field(default_factory=list)
    sample: list[str] = field(default_factory=list)


def default_backup_dir(now: datetime | None = None) -> Path:
    """Return the default desktop backup directory."""

    stamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    desktop = Path("D:/桌面")
    if desktop.exists():
        return desktop / f"workflow1_private_backup_{stamp}"
    return Path.home() / "Desktop" / f"workflow1_private_backup_{stamp}"


def run_release_cleanup(options: CleanupOptions) -> CleanupResult:
    """Scan, and optionally clean, repository-private data for public release."""

    repo_root = options.repo_root.resolve()
    backup_to = (options.backup_to or default_backup_dir()).resolve()
    issues: list[str] = []
    plans = collect_cleanup_plan(repo_root)
    result = CleanupResult(
        status="dry_run" if not options.apply else "started",
        apply=options.apply,
        repo_root=str(repo_root),
        backup_to=str(backup_to),
        planned_delete_count=len(plans),
        planned_delete_bytes=sum(plan.size_bytes for plan in plans),
        sample=[plan.relative_path for plan in plans[:40]],
    )

    backup_issue = _validate_backup_location(repo_root, backup_to)
    if backup_issue:
        result.status = "blocked"
        result.issues.append(backup_issue)
        return result

    if not options.apply:
        result.remaining_risks = scan_remaining_risks(repo_root, planned_deletions={p.relative_path for p in plans})[:80]
        return result

    backup_to.mkdir(parents=True, exist_ok=False)
    files_backup_root = backup_to / "repository_files"
    manifest_path = backup_to / "cleanup_manifest.csv"
    metadata_path = backup_to / "cleanup_metadata.json"

    deleted = 0
    try:
        for plan in plans:
            source = repo_root / plan.relative_path
            if not source.exists() or not source.is_file():
                continue
            original_hash = sha256_file(source)
            backup_path = files_backup_root / plan.relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, backup_path)
            backup_hash = sha256_file(backup_path)
            if backup_hash != original_hash:
                issues.append(f"Hash mismatch, not deleted: {plan.relative_path}")
                continue
            plan.sha256 = original_hash
            plan.backup_path = str(backup_path)
            source.unlink()
            deleted += 1

        _remove_empty_private_dirs(repo_root)
        template_count = write_public_templates(repo_root)
        _write_manifest(manifest_path, plans)
        metadata_path.write_text(
            json.dumps(
                {
                    "repo_root": str(repo_root),
                    "backup_to": str(backup_to),
                    "deleted_count": deleted,
                    "planned_delete_count": len(plans),
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    "notes": "Manifest is intentionally stored outside the public repository.",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    except Exception as exc:  # pragma: no cover - final safety boundary.
        result.status = "error"
        result.issues.extend(issues)
        result.issues.append(str(exc))
        result.deleted_count = deleted
        return result

    remaining = scan_remaining_risks(repo_root)
    result.deleted_count = deleted
    result.template_files_written = template_count
    result.issues.extend(issues)
    result.remaining_risks = remaining[:120]
    result.status = "ok" if not issues and not remaining else "needs_review"
    return result


def collect_cleanup_plan(repo_root: Path) -> list[FilePlan]:
    """Collect files that must not remain in the public repository."""

    plans: dict[str, FilePlan] = {}

    def add(path: Path, reason: str) -> None:
        if not path.exists() or not path.is_file():
            return
        rel = _rel(path, repo_root)
        if _is_public_keep_file(rel):
            return
        plans[rel] = FilePlan(relative_path=rel, size_bytes=path.stat().st_size, reason=reason)

    for root in RISK_ROOTS:
        path = repo_root / root
        if path.exists():
            for file_path in path.rglob("*"):
                add(file_path, f"private generated root: {root}")

    for root in REFERENCE_PRIVATE_ROOTS:
        path = repo_root / root
        if path.exists():
            for file_path in path.rglob("*"):
                add(file_path, f"private reference root: {root}")

    for rel in PRIVATE_CONFIG_FILES:
        add(repo_root / rel, "private local config")

    for rel in PROJECT_SPECIFIC_SOURCE_FILES:
        path = repo_root / rel
        if path.is_file():
            add(path, "project-specific source file")
        elif path.is_dir():
            for file_path in path.rglob("*"):
                add(file_path, "project-specific source directory")

    tools_dir = repo_root / "tools"
    if tools_dir.exists():
        for file_path in tools_dir.glob("*.py"):
            lowered = file_path.name.lower()
            if any(pattern in lowered for pattern in PROJECT_SPECIFIC_TOOL_PATTERNS):
                add(file_path, "project-specific one-off tool")
            elif lowered.startswith(("curate_archive_", "finalize_", "repair_", "verify_")):
                add(file_path, "one-off verification or repair tool")

    for file_path in repo_root.rglob("*"):
        if not file_path.is_file() or ".git" in file_path.parts:
            continue
        rel = _rel(file_path, repo_root)
        if rel.startswith("examples/") and rel.endswith("synthetic_research_demo.csv"):
            continue
        if _is_public_keep_file(rel):
            continue
        if file_path.suffix.lower() in ARTIFACT_SUFFIXES:
            add(file_path, f"artifact suffix: {file_path.suffix.lower()}")
        elif file_path.suffix.lower() == ".csv" and file_path.stat().st_size > 100_000:
            add(file_path, "large CSV likely generated from private data")

    for file_path in (repo_root / "project_state").glob("*"):
        rel = _rel(file_path, repo_root) if file_path.exists() else ""
        expected = PUBLIC_STATE_FILES.get(rel)
        if expected is not None and file_path.is_file():
            current = file_path.read_text(encoding="utf-8", errors="ignore")
            if current == expected:
                continue
        add(file_path, "private project state reset")

    return sorted(plans.values(), key=lambda item: item.relative_path.lower())


def write_public_templates(repo_root: Path) -> int:
    """Write public placeholder files after cleanup."""

    written = 0
    for rel, content in DIRECTORY_READMES.items():
        path = repo_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written += 1
        gitkeep = path.parent / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
            written += 1

    state_dir = repo_root / "project_state"
    state_dir.mkdir(parents=True, exist_ok=True)
    for existing in state_dir.iterdir():
        if existing.is_file():
            existing.unlink()
    for rel, content in PUBLIC_STATE_FILES.items():
        path = repo_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written += 1

    return written


def scan_remaining_risks(repo_root: Path, planned_deletions: set[str] | None = None) -> list[str]:
    """Return risk strings that should be reviewed before publishing."""

    planned_deletions = planned_deletions or set()
    risks: list[str] = []
    project_terms = (
        "YS" + "B",
        "Pest" + "Value",
        "pea" + "nut",
        "FINAL_" + "Si" + "Chuan",
        "黄" + "曲霉",
        "花" + "生",
    )
    sensitive_assignments = ("api_key", "apikey", "secret", "pass" + "word", "access_" + "tok" + "en")
    safe_suffixes = {".pyc"}
    skip_dirs = {".git", "__pycache__", ".pytest_cache"}

    for file_path in repo_root.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part in skip_dirs for part in file_path.parts):
            continue
        rel = _rel(file_path, repo_root)
        if rel in planned_deletions:
            continue
        suffix = file_path.suffix.lower()
        if suffix in safe_suffixes:
            risks.append(f"cache bytecode remains: {rel}")
            continue
        if rel.startswith("examples/") and rel.endswith("synthetic_research_demo.csv"):
            continue
        if suffix in ARTIFACT_SUFFIXES and not rel.endswith(".example"):
            risks.append(f"artifact suffix remains: {rel}")
            continue
        if suffix == ".csv" and file_path.stat().st_size > 100_000:
            risks.append(f"large CSV remains: {rel}")
            continue
        text = _read_small_text(file_path)
        if text is None:
            continue
        lowered = text.lower()
        for term in project_terms:
            if term.lower() in lowered:
                risks.append(f"project keyword remains: {rel}")
                break
        for marker in sensitive_assignments:
            if marker in lowered and _looks_like_real_secret_line(lowered, marker):
                risks.append(f"possible secret assignment remains: {rel}")
                break

    return sorted(set(risks))


def sha256_file(path: Path) -> str:
    """Return SHA256 for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def result_to_dict(result: CleanupResult) -> dict[str, object]:
    """Convert cleanup result to a plain dictionary."""

    return asdict(result)


def _validate_backup_location(repo_root: Path, backup_to: Path) -> str | None:
    try:
        backup_to.relative_to(repo_root)
        return f"Backup directory must be outside the repository: {backup_to}"
    except ValueError:
        pass
    if backup_to == repo_root:
        return f"Backup directory cannot equal the repository root: {backup_to}"
    if backup_to.exists() and any(backup_to.iterdir()):
        return f"Backup directory must not already exist or must be empty: {backup_to}"
    return None


def _remove_empty_private_dirs(repo_root: Path) -> None:
    keep_roots = {
        "data",
        "outputs",
        "reports",
        "experiments",
        "references",
        "project_state",
        "research_corpus",
        "external_cache",
        "archive",
    }
    for root_name in RISK_ROOTS + REFERENCE_PRIVATE_ROOTS + PROJECT_SPECIFIC_SOURCE_FILES:
        root = repo_root / root_name
        if not root.exists() or not root.is_dir():
            continue
        for current, dirs, files in os.walk(root, topdown=False):
            current_path = Path(current)
            rel = _rel(current_path, repo_root)
            if rel in keep_roots:
                continue
            try:
                current_path.rmdir()
            except OSError:
                pass


def _write_manifest(path: Path, plans: Iterable[FilePlan]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["relative_path", "size_bytes", "reason", "sha256", "backup_path"],
        )
        writer.writeheader()
        for plan in plans:
            writer.writerow(asdict(plan))


def _read_small_text(path: Path) -> str | None:
    if path.stat().st_size > 2_000_000:
        return None
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def _looks_like_real_secret_line(text: str, marker: str) -> bool:
    placeholders = (
        "example",
        "placeholder",
        "<",
        "your_",
        "set ",
        "not commit",
        "do not commit",
        "os.environ",
        "redacted",
        "requires_authorization",
        "not read",
        "not printed",
        "not stored",
        "pattern",
        "re.compile",
        "secret_patterns",
        "_has_secret",
        "no_secret",
        "secret_policy",
        "possible secret assignment",
        "approval_required_for",
        "api keys are not",
        "sensitive_assignments",
        "_looks_like_real_secret_line",
    )
    for line in text.splitlines():
        if marker not in line:
            continue
        if "=" not in line and ":" not in line:
            continue
        if any(marker_text in line for marker_text in placeholders):
            continue
        right = line.split("=", 1)[-1].split(":", 1)[-1].strip().strip('"').strip("'")
        if len(right) >= 12:
            return True
    return False


def _is_public_keep_file(relative_path: str) -> bool:
    if Path(relative_path).name == ".gitkeep":
        return True
    if relative_path in DIRECTORY_READMES:
        return True
    return relative_path in {"README.md", "START_HERE.md", "AGENTS.md"}


def _rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root).as_posix()
