"""Gate: model registry is complete enough to drive selection."""

from __future__ import annotations

from workflow1.model_registry.model_registry_auditor import audit_model_registry
from workflow1.quality_gates.base import QualityGate


class ModelRegistryGate(QualityGate):
    gate_name = "ModelRegistryGate"

    def run(self, context: dict[str, object]):
        audit = audit_model_registry(context.get("registry"))
        if audit["status"] != "pass":
            failed = [f"{i['task_type']}:{i['check']}" for i in audit["issues"] if i["status"] == "fail"]
            return self.fail(failed, ["update_model_registry_entry"])
        return self.pass_()
