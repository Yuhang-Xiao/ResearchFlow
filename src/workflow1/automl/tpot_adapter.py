"""TPOT adapter placeholder with safe dependency handling."""

from workflow1.automl.automl_adapter_base import AutoMLAdapter
import importlib.util


class TPOTAdapter(AutoMLAdapter):
    adapter_name = "tpot"
    optional_dependency = "tpot"

    def is_available(self) -> bool:
        return importlib.util.find_spec("tpot") is not None
