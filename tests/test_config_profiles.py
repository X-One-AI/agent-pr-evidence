import json
from pathlib import Path

import pytest

from agent_pr_evidence.cli import main
from agent_pr_evidence.collector import collect_evidence
from agent_pr_evidence.config import EvidenceConfig, load_config
from test_evidence import _sample_repo


def test_report_includes_schema_version_by_default(tmp_path):
    repo, base, head = _sample_repo(tmp_path)

    report = collect_evidence(repo=repo, base=base, head=head, test_logs=[])

    assert report.schema_version == "agent-pr-evidence.report.v1"
    assert report.to_dict()["schema_version"] == "agent-pr-evidence.report.v1"


def test_strict_profile_flags_missing_test_evidence(tmp_path):
    repo, base, head = _sample_repo(tmp_path)

    report = collect_evidence(
        repo=repo,
        base=base,
        head=head,
        test_logs=[],
        config=EvidenceConfig(profile="strict"),
    )

    assert "missing-test-evidence" in report.risk_flags
    assert "Add test evidence before merge." in report.reviewer_checklist


def test_config_file_can_select_profile_and_disable_flags(tmp_path):
    config_path = tmp_path / ".agent-pr-evidence.yml"
    config_path.write_text(
        """
schema_version: 1
profile: strict
disabled_risk_flags:
  - dependency-change
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = load_config(config_path, profile=None)

    assert config.profile == "strict"
    assert config.disabled_risk_flags == ("dependency-change",)


def test_unknown_profile_is_rejected(tmp_path):
    config_path = tmp_path / ".agent-pr-evidence.yml"
    config_path.write_text("schema_version: 1\nprofile: noisy\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Unknown profile"):
        load_config(config_path, profile=None)


def test_cli_collect_uses_config_and_profile_override(tmp_path, capsys):
    repo, base, head = _sample_repo(tmp_path)
    config_path = tmp_path / ".agent-pr-evidence.yml"
    config_path.write_text("schema_version: 1\nprofile: default\n", encoding="utf-8")

    exit_code = main(
        [
            "collect",
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
            "--config",
            str(config_path),
            "--profile",
            "strict",
            "--format",
            "json",
        ]
    )

    data = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert data["schema_version"] == "agent-pr-evidence.report.v1"
    assert "missing-test-evidence" in data["risk_flags"]
    assert "dependency-change" in data["risk_flags"]


def test_cli_collect_discovers_repo_config_by_default(tmp_path, capsys):
    repo, base, head = _sample_repo(tmp_path)
    (repo / ".agent-pr-evidence.yml").write_text("schema_version: 1\nprofile: strict\n", encoding="utf-8")

    exit_code = main(["collect", "--repo", str(repo), "--base", base, "--head", head, "--format", "json"])

    data = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert "missing-test-evidence" in data["risk_flags"]
