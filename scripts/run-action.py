from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from agent_pr_evidence.collector import collect_evidence
from agent_pr_evidence.config import load_config, resolve_config_path
from agent_pr_evidence.renderers import render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-pr-evidence-action")
    parser.add_argument("--repo", default=".", help="git repository path")
    parser.add_argument("--base", required=True, help="base git ref")
    parser.add_argument("--head", required=True, help="head git ref")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", default="agent-pr-evidence.md", help="report output path")
    parser.add_argument("--config", help="optional .agent-pr-evidence.yml config file")
    parser.add_argument("--profile", help="override config profile")
    parser.add_argument("--test-log", action="append", default=[], help="test log file; repeatable")
    parser.add_argument("--test-logs", default="", help="newline- or comma-separated test log paths")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    test_logs = [Path(path) for path in [*args.test_log, *_split_paths(args.test_logs)] if path]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    repo = Path(args.repo)
    config = load_config(resolve_config_path(repo, args.config), args.profile)
    report = collect_evidence(repo=repo, base=args.base, head=args.head, test_logs=test_logs, config=config)
    rendered = render_json(report) if args.format == "json" else render_markdown(report)
    output_path.write_text(rendered, encoding="utf-8")
    _append_step_summary(rendered)
    _write_outputs(
        {
            "report-path": str(output_path),
            "summary-json": json.dumps(
                {
                    "changed_files": report.summary.changed_files,
                    "risk_flags": report.risk_flags,
                    "schema_version": report.schema_version,
                    "test_status": report.summary.test_status,
                },
                separators=(",", ":"),
            ),
        }
    )
    print(f"Agent PR evidence written to {output_path}")
    return 0


def _split_paths(value: str) -> list[str]:
    return [part.strip() for raw in value.splitlines() for part in raw.split(",") if part.strip()]


def _append_step_summary(markdown: str) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with Path(summary_path).open("a", encoding="utf-8") as summary:
        summary.write(markdown)


def _write_outputs(outputs: dict[str, str]) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    with Path(output_path).open("a", encoding="utf-8") as output:
        for key, value in outputs.items():
            output.write(f"{key}={value}\n")


if __name__ == "__main__":
    raise SystemExit(main())
