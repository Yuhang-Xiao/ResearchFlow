"""Data cleaning pipeline."""

from workflow1.pipelines.cleaning.plan import run as run_cleaning_plan
from workflow1.pipelines.runner import PipelineResult, run_placeholder_pipeline


def run() -> PipelineResult:
    """Run the cleaning pipeline placeholder."""

    return run_placeholder_pipeline("cleaning")


__all__ = ["PipelineResult", "run", "run_cleaning_plan"]
