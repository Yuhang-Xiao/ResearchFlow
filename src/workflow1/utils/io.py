"""Basic file-system helpers."""

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if needed and return it as a Path."""

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def list_files(path: str | Path, pattern: str = "*") -> list[Path]:
    """List files directly under a path using a glob pattern."""

    root = Path(path)
    if not root.exists():
        return []
    return sorted(item for item in root.glob(pattern) if item.is_file())
