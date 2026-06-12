# agent-pr-evidence

Languages: English | [中文](./README.zh-CN.md)

Generate reviewable safety evidence for AI-agent-generated pull requests.

## Status

`P1` - reserved production foundation.

## Purpose

Move Safe Agent Operations from config scanning into PR review and CI evidence.

## First Production Surface

GitHub Action and CLI that produce a Markdown/JSON PR evidence packet.

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
