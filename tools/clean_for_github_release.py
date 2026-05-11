"""Run workflow1 public-release cleanup from a source checkout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from workflow1.tools.github_release_cleaner import (  # noqa: E402
    CleanupOptions,
    default_backup_dir,
    result_to_dict,
    run_release_cleanup,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean workflow1 before a public GitHub release.")
    parser.add_argument("--apply", action="store_true", help="Actually back up and delete private files.")
    parser.add_argument(
        "--backup-to",
        default=None,
        help="Backup directory outside the repository. Defaults to a timestamped Desktop folder.",
    )
    parser.add_argument(
        "--keep-synthetic-example",
        action="store_true",
        default=True,
        help="Keep the public synthetic demo data file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    backup_to = Path(args.backup_to) if args.backup_to else default_backup_dir()
    result = run_release_cleanup(
        CleanupOptions(
            repo_root=REPO_ROOT,
            backup_to=backup_to,
            apply=args.apply,
            keep_synthetic_example=args.keep_synthetic_example,
        )
    )
    print(json.dumps(result_to_dict(result), ensure_ascii=False, indent=2))
    return 0 if result.status in {"ok", "dry_run"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
