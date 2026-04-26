"""Raw data intake pipeline."""

from workflow1.pipelines.runner import PipelineResult
from workflow1.pipelines.intake.runner import run


__all__ = ["PipelineResult", "run"]
