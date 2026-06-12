from pathlib import Path

import yaml

from agent_pr_evidence.collector import collect_evidence
from test_evidence import _git, _write


def _corpus_cases() -> list[dict]:
    data = yaml.safe_load(Path("tests/fixtures/pr-corpus/v1.yml").read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    return data["cases"]


def _build_case_repo(tmp_path: Path, case: dict) -> tuple[Path, str, str]:
    repo = tmp_path / case["id"]
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.email", "agent@example.com")
    _git(repo, "config", "user.name", "Agent")
    for path, text in case["base_files"].items():
        _write(repo, path, text)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "chore: base")
    base = _git(repo, "rev-parse", "HEAD")

    for path, text in case["head_files"].items():
        _write(repo, path, text)
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feat: agent change")
    head = _git(repo, "rev-parse", "HEAD")
    return repo, base, head


def test_pr_fixture_corpus_risk_boundaries(tmp_path):
    for case in _corpus_cases():
        repo, base, head = _build_case_repo(tmp_path, case)

        report = collect_evidence(repo=repo, base=base, head=head, test_logs=[])

        assert report.risk_flags == case["expected_risk_flags"], case["id"]
        assert report.summary.sensitive_files == case["expected_sensitive_files"], case["id"]
