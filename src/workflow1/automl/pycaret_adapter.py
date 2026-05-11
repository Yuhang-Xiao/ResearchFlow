"""PyCaret adapter placeholder with safe dependency handling."""

from workflow1.automl.automl_adapter_base import AutoMLAdapter
import importlib.util


class PyCaretAdapter(AutoMLAdapter):
    adapter_name = "pycaret"
    optional_dependency = "pycaret"

    def is_available(self) -> bool:
        return importlib.util.find_spec("pycaret") is not None
