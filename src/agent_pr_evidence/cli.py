from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agent_pr_evidence import __version__
from agent_pr_evidence.baseline import baseline_from_report, evaluate_new_risks
from agent_pr_evidence.collector import collect_evidence
from agent_pr_evidence.config import load_config, resolve_config_path
from agent_pr_evidence.renderers import render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-pr-evidence")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    subparsers = parser.add_subparsers(dest="command")

    collect = subparsers.add_parser("collect", help="collect local PR evidence from a git diff")
    collect.add_argument("--repo", default=".", help="git repository path")
    collect.add_argument("--base", required=True, help="base git ref")
    collect.add_argument("--head", required=True, help="head git ref")
    collect.add_argument("--test-log", action="append", default=[], help="test log file; repeatable")
    collect.add_argument("--config", help="optional .agent-pr-evidence.yml config file")
    collect.add_argument("--profile", choices=("default", "strict"), help="override config profile")
    collect.add_argument("--format", choices=("markdown", "json"), default="markdown")
    collect.add_argument("--output", help="write report to file instead of stdout")

    baseline = subparsers.add_parser("baseline", help="write a baseline from a git diff")
    _add_collection_args(baseline)
    baseline.add_argument("--output", required=True, help="baseline JSON output path")

    gate = subparsers.add_parser("gate", help="fail when new risk flags are not in a baseline")
    _add_collection_args(gate)
    gate.add_argument("--baseline", required=True, help="baseline JSON path")
    gate.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser


def _add_collection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", default=".", help="git repository path")
    parser.add_argument("--base", required=True, help="base git ref")
    parser.add_argument("--head", required=True, help="head git ref")
    parser.add_argument("--test-log", action="append", default=[], help="test log file; repeatable")
    parser.add_argument("--config", help="optional .agent-pr-evidence.yml config file")
    parser.add_argument("--profile", choices=("default", "strict"), help="override config profile")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)

    if args.version:
        print(f"agent-pr-evidence {__version__}")
        return 0
    if args.command is None:
        parser.print_help(sys.stderr)
        return 2

    if args.command == "collect":
        try:
            report = _collect_from_args(args)
        except Exception as exc:
            print(f"Failed to collect evidence: {exc}", file=sys.stderr)
            return 2
        output = render_json(report) if args.format == "json" else render_markdown(report)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
        return 0

    if args.command == "baseline":
        try:
            report = _collect_from_args(args)
            output = json.dumps(baseline_from_report(report), indent=2, sort_keys=True) + "\n"
            Path(args.output).write_text(output, encoding="utf-8")
        except Exception as exc:
            print(f"Failed to write baseline: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "gate":
        try:
            report = _collect_from_args(args)
            baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
            result = evaluate_new_risks(report, baseline)
        except Exception as exc:
            print(f"Failed to evaluate gate: {exc}", file=sys.stderr)
            return 2
        output = json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
        sys.stdout.write(output)
        return 1 if result.failed else 0

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 2


def _collect_from_args(args: argparse.Namespace):
    repo = Path(args.repo)
    config = load_config(resolve_config_path(repo, args.config), args.profile)
    return collect_evidence(
        repo=repo,
        base=args.base,
        head=args.head,
        test_logs=[Path(path) for path in args.test_log],
        config=config,
    )


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
