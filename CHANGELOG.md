# Changelog

## 0.2.0

Configuration and governance release.

- Add `.agent-pr-evidence.yml` auto-discovery from the repository root.
- Add `default` and `strict` profiles.
- Add `disabled_risk_flags` for team-specific false-positive control.
- Add report schema versioning with `agent-pr-evidence.report.v1`.
- Add Action inputs for `config` and `profile`.

## 0.1.0

Initial early-production release.

- Add local CLI: `agent-pr-evidence collect`.
- Generate Markdown and JSON PR evidence from git base/head diffs.
- Detect CI/workflow, dependency, infra, auth/policy, and secret-like changes.
- Redact secret-like values from test log evidence.
- Add read-only GitHub Action support that writes `GITHUB_STEP_SUMMARY` and outputs.
- Add English and Simplified Chinese README entry points.
