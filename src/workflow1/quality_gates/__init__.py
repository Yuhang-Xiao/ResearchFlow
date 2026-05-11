"""Executable quality gates for workflow1 Research OS."""

from workflow1.quality_gates.paper_completeness_gate import PaperCompletenessGate
from workflow1.quality_gates.metric_completeness_gate import MetricCompletenessGate
from workflow1.quality_gates.model_comparison_gate import ModelComparisonGate
from workflow1.quality_gates.model_registry_gate import ModelRegistryGate
from workflow1.quality_gates.latex_product_gate import LatexProductGate
from workflow1.quality_gates.publication_quality_gate import PublicationQualityGate

__all__ = [
    "PaperCompletenessGate",
    "MetricCompletenessGate",
    "ModelComparisonGate",
    "ModelRegistryGate",
    "LatexProductGate",
    "PublicationQualityGate",
]
