from __future__ import annotations

import json

from agent_pr_evidence.model import EvidenceReport


def render_json(report: EvidenceReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def render_markdown(report: EvidenceReport) -> str:
    lines = [
        "# Agent PR Evidence",
        "",
        "## Summary",
        "",
        f"- Changed files: {report.summary.changed_files}",
        f"- Additions: {report.summary.additions}",
        f"- Deletions: {report.summary.deletions}",
        f"- Sensitive files: {report.summary.sensitive_files}",
        f"- Test status: {report.summary.test_status}",
        "",
        "## Risk Flags",
        "",
    ]
    lines.extend(f"- {flag}" for flag in report.risk_flags) if report.risk_flags else lines.append("- none")
    lines.extend(["", "## Changed Files", ""])
    for file in report.files:
        categories = ", ".join(file.categories) if file.categories else "none"
        lines.append(f"- `{file.path}` ({file.status}, +{file.additions}/-{file.deletions}) - {categories}")
    lines.extend(["", "## Test Evidence", ""])
    if report.test_evidence:
        for test in report.test_evidence:
            lines.append(f"- `{test.path}`: {test.status}")
    else:
        lines.append("- not provided")
    lines.extend(["", "## Reviewer Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in report.reviewer_checklist)
    lines.append("")
    return "\n".join(lines)
