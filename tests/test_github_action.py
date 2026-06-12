import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

from test_evidence import _sample_repo


def test_action_contract_is_safe_for_pull_request_evidence():
    action = yaml.safe_load(Path("action.yml").read_text(encoding="utf-8"))

    assert action["name"] == "Agent PR Evidence"
    assert action["inputs"]["base"]["required"] is True
    assert action["inputs"]["head"]["required"] is True
    assert action["inputs"]["format"]["default"] == "markdown"
    assert action["inputs"]["baseline"]["required"] is False
    assert action["outputs"]["gate-failed"]["description"]
    assert action["outputs"]["report-path"]["description"]
    assert action["runs"]["using"] == "composite"
    assert "scripts/run-action.py" in action["runs"]["steps"][-1]["run"]


def test_action_runner_writes_summary_report_and_outputs(tmp_path):
    repo, base, head = _sample_repo(tmp_path)
    github_output = tmp_path / "github-output.txt"
    github_summary = tmp_path / "github-summary.md"
    report_path = tmp_path / "evidence.md"
    test_log = tmp_path / "pytest.log"
    test_log.write_text("5 passed\nTOKEN=sk-action-secret\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run-action.py",
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
            "--format",
            "markdown",
            "--output",
            str(report_path),
            "--test-log",
            str(test_log),
        ],
        check=True,
        cwd=Path.cwd(),
        env=os.environ
        | {
            "PYTHONPATH": "src",
            "GITHUB_OUTPUT": str(github_output),
            "GITHUB_STEP_SUMMARY": str(github_summary),
        },
        text=True,
        stdout=subprocess.PIPE,
    )

    assert report_path.exists()
    assert github_summary.read_text(encoding="utf-8") == report_path.read_text(encoding="utf-8")
    output = github_output.read_text(encoding="utf-8")
    assert f"report-path={report_path}" in output
    summary_line = next(line for line in output.splitlines() if line.startswith("summary-json="))
    summary = json.loads(summary_line.removeprefix("summary-json="))
    assert summary == {
        "changed_files": 4,
        "risk_flags": ["ci-or-workflow-change", "dependency-change", "secret-like-content"],
        "schema_version": "agent-pr-evidence.report.v1",
        "test_status": "passed",
    }
    assert "sk-action-secret" not in result.stdout
    assert "sk-action-secret" not in report_path.read_text(encoding="utf-8")


def test_action_runner_outputs_gate_result_when_baseline_is_provided(tmp_path):
    repo, base, head = _sample_repo(tmp_path)
    baseline_path = tmp_path / "baseline.json"
    report_path = tmp_path / "evidence.md"
    github_output = tmp_path / "github-output.txt"
    baseline_path.write_text(
        json.dumps(
            {
                "schema_version": "agent-pr-evidence.baseline.v1",
                "risk_flags": ["ci-or-workflow-change", "dependency-change", "secret-like-content"],
                "files": {},
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run-action.py",
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
            "--output",
            str(report_path),
            "--profile",
            "strict",
            "--baseline",
            str(baseline_path),
        ],
        cwd=Path.cwd(),
        env=os.environ | {"PYTHONPATH": "src", "GITHUB_OUTPUT": str(github_output)},
    )

    assert result.returncode == 1
    output = github_output.read_text(encoding="utf-8")
    assert "gate-failed=true" in output
    assert "new-risk-flags=missing-test-evidence" in output


def test_action_runner_accepts_empty_optional_config_inputs(tmp_path):
    repo, base, head = _sample_repo(tmp_path)
    report_path = tmp_path / "evidence.md"

    subprocess.run(
        [
            sys.executable,
            "scripts/run-action.py",
            "--repo",
            str(repo),
            "--base",
            base,
            "--head",
            head,
            "--output",
            str(report_path),
            "--config",
            "",
            "--profile",
            "",
        ],
        check=True,
        cwd=Path.cwd(),
        env=os.environ | {"PYTHONPATH": "src"},
    )

    assert report_path.exists()
