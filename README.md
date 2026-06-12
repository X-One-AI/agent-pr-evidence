# agent-pr-evidence

Languages: English | [中文](./README.zh-CN.md)

Generate reviewable safety evidence for AI-agent-generated pull requests.

## Status

`P1` - v0.3.0 released.

## Purpose

Move Safe Agent Operations from config scanning into PR review and CI evidence.

## First Production Surface

Local CLI and GitHub Action that produce a Markdown/JSON PR evidence packet from a git base/head diff. The GitHub App surface is deferred until the required permissions and real PR samples are available.

## Install

From this repository:

```bash
python3 -m pip install -e .
agent-pr-evidence --version
```

## Usage

Collect local PR evidence from a git diff:

```bash
agent-pr-evidence collect --base origin/main --head HEAD --format markdown
agent-pr-evidence collect --base origin/main --head HEAD --format json --output pr-evidence.json
agent-pr-evidence collect --base origin/main --head HEAD --test-log pytest.log
agent-pr-evidence collect --base origin/main --head HEAD --config .agent-pr-evidence.yml --profile strict
agent-pr-evidence baseline --base origin/main --head HEAD --output agent-pr-evidence-baseline.json
agent-pr-evidence gate --base origin/main --head HEAD --baseline agent-pr-evidence-baseline.json --profile strict
```

The first production surface is local-first. It does not need GitHub App permissions and does not upload repository data.

## Configuration

`agent-pr-evidence` automatically reads `.agent-pr-evidence.yml` from the repository root. Use `--config` to point at another file, and `--profile` to override the file for a single run.

```yaml
schema_version: 1
profile: strict
disabled_risk_flags:
  - dependency-change
```

Profiles:

- `default`: lower-noise review evidence for teams adopting the tool.
- `strict`: adds `missing-test-evidence` when no test logs are provided.

Reports include `schema_version: agent-pr-evidence.report.v1` so downstream workflow steps can check compatibility before consuming JSON.

## Baseline Gate

Use a baseline when adopting the tool in an existing repository. The baseline records known risk flags, then `gate` fails only when a PR introduces new risk flags that are not already accepted.

```bash
agent-pr-evidence baseline --base origin/main --head HEAD --output agent-pr-evidence-baseline.json
agent-pr-evidence gate --base origin/main --head HEAD --baseline agent-pr-evidence-baseline.json --profile strict
```

Baseline files use `schema_version: agent-pr-evidence.baseline.v1`.

## GitHub Action

Use the Action after `actions/checkout` with enough history for the base/head diff:

```yaml
name: Agent PR Evidence

on:
  pull_request:

permissions:
  contents: read

jobs:
  evidence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - uses: X-One-AI/agent-pr-evidence@v0.3.0
        with:
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          output: agent-pr-evidence.md
          profile: strict
          baseline: agent-pr-evidence-baseline.json
```

The Action writes the report to `GITHUB_STEP_SUMMARY` and exposes `report-path`, `summary-json`, `gate-failed`, and `new-risk-flags` outputs. It does not request write permissions or post PR comments by default.

## Required Evidence

- scope summary
- sensitive file changes
- test evidence
- dependency and CI/auth/infra changes
- reviewer checklist

## Current Limits

- PR comments are intentionally not posted by default.
- GitHub App permissions are still skipped until real review workflows are available.
- Rule boundaries still need real PR false-positive and false-negative tuning.

## Non-Goals

- not a generic code review bot
- not an autonomous merge gate
- not a hosted dashboard in the first version

## OPT Operating Model

This project references the shared One Person Team workflow through [ops/opt-overlay.md](./ops/opt-overlay.md). Project-specific constraints live under [ops/constraints](./ops/constraints), and evolvable local skills live under [ops/skills](./ops/skills).

## Blocked Inputs

Inputs that require user or real-world data are recorded in `../x-one-skipped-inputs.md` and should not block foundation work.

## Docs

- [Changelog](./CHANGELOG.md)
- [Example Config](./examples/agent-pr-evidence.yml)
- [Example Baseline](./examples/baseline.json)
- [Product Foundation](./docs/product-foundation.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [Production Constraints](./ops/constraints/production.md)
- [Main Entry Constraints](./ops/constraints/main-entry.md)
- [Skill Evolution](./ops/skills/evolution.md)
