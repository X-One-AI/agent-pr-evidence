import json
from pathlib import Path

from agent_pr_evidence.baseline import baseline_from_report, evaluate_new_risks
from agent_pr_evidence.cli import main
from agent_pr_evidence.collector import collect_evidence
from agent_pr_evidence.config import EvidenceConfig
from test_evidence import _sample_repo


def test_baseline_from_report_records_risk_flags_and_file_categories(tmp_path):
    repo, base, head = _sample_repo(tmp_path)
    report = collect_evidence(repo=repo, base=base, head=head, test_logs=[])

    baseline = baseline_from_report(report)

    assert baseline["schema_version"] == "agent-pr-evidence.baseline.v1"
    assert baseline["risk_flags"] == ["ci-or-workflow-change", "dependency-change", "secret-like-content"]
    assert baseline["files"]["requirements.txt"] == ["dependency-change"]


def test_evaluate_new_risks_only_fails_for_risks_not_in_baseline(tmp_path):
    repo, base, head = _sample_repo(tmp_path)
    report = collect_evidence(
        repo=repo,
        base=base,
        head=head,
        test_logs=[],
        config=EvidenceConfig(profile="strict"),
    )
    baseline = {
        "schema_version": "agent-pr-evidence.baseline.v1",
        "risk_flags": ["ci-or-workflow-change", "dependency-change", "secret-like-content"],
        "files": {},
    }

    result = evaluate_new_risks(report, baseline)

    assert result.failed is True
    assert result.new_risk_flags == ["missing-test-evidence"]


def test_cli_baseline_write_and_gate_modes(tmp_path, capsys):
    repo, base, head = _sample_repo(tmp_path)
    baseline_path = tmp_path / "baseline.json"

    write_exit = main(
        [
            "baseline",
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
            "--output",
            str(baseline_path),
        ]
    )
    assert write_exit == 0
    assert json.loads(baseline_path.read_text(encoding="utf-8"))["schema_version"] == "agent-pr-evidence.baseline.v1"

    gate_exit = main(
        [
            "gate",
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
            "--baseline",
            str(baseline_path),
            "--profile",
            "strict",
            "--format",
            "json",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert gate_exit == 1
    assert output["failed"] is True
    assert output["new_risk_flags"] == ["missing-test-evidence"]
