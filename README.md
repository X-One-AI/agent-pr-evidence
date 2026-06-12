# agent-pr-evidence

Languages: English | [中文](./README.zh-CN.md)

Generate reviewable safety evidence for AI-agent-generated pull requests.

## Status

`P1` - early production local CLI.

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
```

The first production surface is local-first. It does not need GitHub App permissions and does not upload repository data.

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
      - uses: X-One-AI/agent-pr-evidence@feat/local-pr-evidence-cli
        with:
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          output: agent-pr-evidence.md
```

The Action writes the report to `GITHUB_STEP_SUMMARY` and exposes `report-path` plus `summary-json` outputs. It does not request write permissions or post PR comments by default.

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

- [Product Foundation](./docs/product-foundation.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [Production Constraints](./ops/constraints/production.md)
- [Main Entry Constraints](./ops/constraints/main-entry.md)
- [Skill Evolution](./ops/skills/evolution.md)
