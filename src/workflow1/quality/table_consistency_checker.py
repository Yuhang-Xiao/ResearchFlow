"""Check consistency between report claims and table values."""
from __future__ import annotations


def compare_report_numbers(report_numbers: dict[str, float], table_numbers: dict[str, float], tolerance: float = 1e-9) -> list[dict]:
    findings = []
    for key, report_value in report_numbers.items():
        table_value = table_numbers.get(key)
        if table_value is None:
            findings.append({"metric": key, "status": "missing_in_table", "report_value": report_value, "table_value": ""})
        elif abs(float(report_value) - float(table_value)) > tolerance:
            findings.append({"metric": key, "status": "mismatch", "report_value": report_value, "table_value": table_value})
        else:
            findings.append({"metric": key, "status": "pass", "report_value": report_value, "table_value": table_value})
    return findings
