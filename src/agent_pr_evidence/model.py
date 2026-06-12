from __future__ import annotations

from dataclasses import asdict, dataclass


REPORT_SCHEMA_VERSION = "agent-pr-evidence.report.v1"


@dataclass(frozen=True)
class FileChange:
    path: str
    status: str
    additions: int
    deletions: int
    categories: tuple[str, ...]


@dataclass(frozen=True)
class TestEvidence:
    path: str
    status: str
    excerpt: str


@dataclass(frozen=True)
class EvidenceSummary:
    changed_files: int
    additions: int
    deletions: int
    sensitive_files: int
    test_status: str


@dataclass(frozen=True)
class EvidenceReport:
    schema_version: str
    base: str
    head: str
    summary: EvidenceSummary
    files: tuple[FileChange, ...]
    test_evidence: tuple[TestEvidence, ...]
    risk_flags: list[str]
    reviewer_checklist: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
