"""FLAML adapter placeholder with safe dependency handling."""

from workflow1.automl.automl_adapter_base import AutoMLAdapter
import importlib.util


class FLAMLAdapter(AutoMLAdapter):
    adapter_name = "flaml"
    optional_dependency = "flaml"

    def is_available(self) -> bool:
        return importlib.util.find_spec("flaml") is not None
