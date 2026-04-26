"""Allow `python -m workflow1` to run the lightweight entry point."""

from workflow1.cli import main


if __name__ == "__main__":
    raise SystemExit(main())

