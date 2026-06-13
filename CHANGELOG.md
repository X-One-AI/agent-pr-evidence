# Changelog

## 0.4.1

Distribution release.

- Add package publishing workflow and distribution documentation.
- Prepare a release tag that includes the PyPI/TestPyPI publishing workflow.

## 0.4.0

PR fixture corpus and rule-boundary hardening release.

- Add a versioned PR fixture corpus for positive and negative rule-boundary cases.
- Reduce false positives for documented placeholder credentials such as `<your-api-key>`.
- Detect nested dependency manifests and lockfiles, including monorepo package paths.
- Include fixture corpus files in source distributions so rule changes remain reproducible.

## 0.3.0

Baseline review gate release.

- Add `agent-pr-evidence baseline` to create review baselines.
- Add `agent-pr-evidence gate` to fail only on risk flags not present in the baseline.
- Add baseline schema versioning with `agent-pr-evidence.baseline.v1`.
- Add GitHub Action `baseline` input plus `gate-failed` and `new-risk-flags` outputs.
- Add example baseline file.

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
