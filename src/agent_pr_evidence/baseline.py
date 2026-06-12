from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent_pr_evidence.model import EvidenceReport

BASELINE_SCHEMA_VERSION = "agent-pr-evidence.baseline.v1"


@dataclass(frozen=True)
class GateResult:
    failed: bool
    new_risk_flags: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"failed": self.failed, "new_risk_flags": self.new_risk_flags}


def baseline_from_report(report: EvidenceReport) -> dict[str, Any]:
    return {
        "schema_version": BASELINE_SCHEMA_VERSION,
        "risk_flags": list(report.risk_flags),
        "files": {file.path: list(file.categories) for file in report.files if file.categories},
    }


def evaluate_new_risks(report: EvidenceReport, baseline: dict[str, Any]) -> GateResult:
    if baseline.get("schema_version") != BASELINE_SCHEMA_VERSION:
        raise ValueError(f"Unsupported baseline schema_version: {baseline.get('schema_version')}")
    baseline_flags = set(baseline.get("risk_flags", []))
    new_flags = sorted(flag for flag in report.risk_flags if flag not in baseline_flags)
    return GateResult(failed=bool(new_flags), new_risk_flags=new_flags)
