from __future__ import annotations

import re
from pathlib import Path

from agent_pr_evidence.config import EvidenceConfig
from agent_pr_evidence.git_adapter import changed_paths, file_at_ref, numstat
from agent_pr_evidence.model import REPORT_SCHEMA_VERSION, EvidenceReport, EvidenceSummary, FileChange, TestEvidence
from agent_pr_evidence.redaction import redact

_SECRET_CONTENT = re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*=|sk-[A-Za-z0-9_-]{8,}")


def collect_evidence(
    repo: Path,
    base: str,
    head: str,
    test_logs: list[Path],
    config: EvidenceConfig | None = None,
) -> EvidenceReport:
    config = config or EvidenceConfig()
    paths = changed_paths(repo, base, head)
    stats = numstat(repo, base, head)
    files = tuple(_file_change(repo, head, path, status, stats.get(path, (0, 0))) for path, status in paths.items())
    tests = tuple(_test_evidence(path) for path in test_logs)
    risk_flags = sorted({flag for file in files for flag in _risk_flags(file)})
    if config.require_test_evidence and not tests:
        risk_flags.append("missing-test-evidence")
    risk_flags = [flag for flag in risk_flags if flag not in config.disabled_risk_flags]
    checklist = _checklist(risk_flags, tests)
    summary = EvidenceSummary(
        changed_files=len(files),
        additions=sum(file.additions for file in files),
        deletions=sum(file.deletions for file in files),
        sensitive_files=sum(1 for file in files if file.categories),
        test_status=_combined_test_status(tests),
    )
    return EvidenceReport(
        schema_version=REPORT_SCHEMA_VERSION,
        base=base,
        head=head,
        summary=summary,
        files=files,
        test_evidence=tests,
        risk_flags=risk_flags,
        reviewer_checklist=checklist,
    )


def _file_change(repo: Path, head: str, path: str, status: str, stat: tuple[int, int]) -> FileChange:
    categories = list(_path_categories(path))
    if _has_secret_like_content(repo, head, path):
        categories.append("secret-like-content")
    return FileChange(path=path, status=status, additions=stat[0], deletions=stat[1], categories=tuple(categories))


def _path_categories(path: str) -> tuple[str, ...]:
    categories: list[str] = []
    if path.startswith(".github/workflows/") or path in {".github/dependabot.yml", ".github/actions.yml"}:
        categories.append("ci-or-workflow-change")
    if path in {"requirements.txt", "pyproject.toml", "package.json", "package-lock.json", "pnpm-lock.yaml"}:
        categories.append("dependency-change")
    if any(part in path for part in ("infra", "terraform", "kubernetes", "helm")):
        categories.append("infra-change")
    if any(part in path.lower() for part in ("auth", "permission", "policy")):
        categories.append("auth-or-policy-change")
    return tuple(categories)


def _has_secret_like_content(repo: Path, head: str, path: str) -> bool:
    try:
        content = file_at_ref(repo, head, path)
    except Exception:
        return False
    return bool(_SECRET_CONTENT.search(content))


def _test_evidence(path: Path) -> TestEvidence:
    text = path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    if "failed" in lower or "error" in lower:
        status = "failed"
    elif "passed" in lower or "success" in lower:
        status = "passed"
    else:
        status = "unknown"
    excerpt = redact("\\n".join(text.splitlines()[:20]))
    return TestEvidence(path=str(path), status=status, excerpt=excerpt)


def _combined_test_status(tests: tuple[TestEvidence, ...]) -> str:
    if not tests:
        return "not-provided"
    if any(test.status == "failed" for test in tests):
        return "failed"
    if all(test.status == "passed" for test in tests):
        return "passed"
    return "unknown"


def _risk_flags(file: FileChange) -> tuple[str, ...]:
    return file.categories


def _checklist(risk_flags: list[str], tests: tuple[TestEvidence, ...]) -> list[str]:
    items = ["Review changed files for requested scope."]
    if "ci-or-workflow-change" in risk_flags:
        items.append("Review CI or workflow changes.")
    if "dependency-change" in risk_flags:
        items.append("Review dependency changes.")
    if "secret-like-content" in risk_flags:
        items.append("Confirm secret-like content is removed or redacted.")
    if not tests:
        items.append("Add test evidence before merge.")
    return items
