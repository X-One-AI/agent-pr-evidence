import json
import os
import subprocess
import sys
from pathlib import Path

from agent_pr_evidence.cli import main
from agent_pr_evidence.collector import collect_evidence
from agent_pr_evidence.renderers import render_markdown


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _write(repo: Path, path: str, text: str) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _sample_repo(tmp_path: Path) -> tuple[Path, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.email", "agent@example.com")
    _git(repo, "config", "user.name", "Agent")
    _write(repo, "README.md", "# demo\n")
    _write(repo, "src/app.py", "print('hello')\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "chore: initial")
    base = _git(repo, "rev-parse", "HEAD")

    _write(repo, "src/app.py", "print('hello')\nprint('agent')\n")
    _write(repo, ".github/workflows/ci.yml", "name: CI\n")
    _write(repo, "requirements.txt", "requests==2.32.0\n")
    _write(repo, "notes.txt", "token=sk-secret-value\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feat: agent change")
    head = _git(repo, "rev-parse", "HEAD")
    return repo, base, head


def test_collect_evidence_classifies_scope_and_sensitive_files(tmp_path):
    repo, base, head = _sample_repo(tmp_path)
    test_log = tmp_path / "test.log"
    test_log.write_text("12 passed\nAPI_KEY=sk-live-secret\n", encoding="utf-8")

    report = collect_evidence(repo=repo, base=base, head=head, test_logs=[test_log])

    assert report.summary.changed_files == 4
    assert report.summary.sensitive_files == 3
    assert report.summary.test_status == "passed"
    assert report.risk_flags == [
        "ci-or-workflow-change",
        "dependency-change",
        "secret-like-content",
    ]
    assert "sk-live-secret" not in report.test_evidence[0].excerpt


def test_render_markdown_outputs_reviewable_checklist(tmp_path):
    repo, base, head = _sample_repo(tmp_path)

    markdown = render_markdown(collect_evidence(repo=repo, base=base, head=head, test_logs=[]))

    assert "# Agent PR Evidence" in markdown
    assert "## Reviewer Checklist" in markdown
    assert "- [ ] Review CI or workflow changes." in markdown
    assert "- [ ] Review dependency changes." in markdown


def test_cli_collect_outputs_json(tmp_path, capsys):
    repo, base, head = _sample_repo(tmp_path)

    exit_code = main(["collect", "--repo", str(repo), "--base", base, "--head", head, "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["summary"]["changed_files"] == 4
    assert data["risk_flags"] == ["ci-or-workflow-change", "dependency-change", "secret-like-content"]


def test_package_module_entrypoint_outputs_version():
    result = subprocess.run(
        [sys.executable, "-m", "agent_pr_evidence", "--version"],
        check=True,
        env=os.environ | {"PYTHONPATH": "src"},
        text=True,
        stdout=subprocess.PIPE,
    )

    assert result.stdout.strip() == "agent-pr-evidence 0.2.0"
