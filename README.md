# agent-pr-evidence

Languages: English | [中文](./README.zh-CN.md)

Generate reviewable safety evidence for AI-agent-generated pull requests.

## Status

`P1` - early production local CLI.

## Purpose

Move Safe Agent Operations from config scanning into PR review and CI evidence.

## First Production Surface

Local CLI that produces a Markdown/JSON PR evidence packet from a git base/head diff. GitHub Action and GitHub App surfaces are deferred until the required permissions and real PR samples are available.

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

## Required Evidence

- scope summary
- sensitive file changes
- test evidence
- dependency and CI/auth/infra changes
- reviewer checklist

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
