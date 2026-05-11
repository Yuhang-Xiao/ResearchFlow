"""AutoGluon adapter placeholder with safe dependency handling."""

from workflow1.automl.automl_adapter_base import AutoMLAdapter
import importlib.util


class AutoGluonAdapter(AutoMLAdapter):
    adapter_name = "autogluon"
    optional_dependency = "autogluon"

    def is_available(self) -> bool:
        return importlib.util.find_spec("autogluon") is not None
