# agent-pr-evidence Product Foundation

## Intake

- Priority: P1
- Status: v0.3.0 release candidate with local CLI, GitHub Action, config profiles, schema versioning, and baseline review gates
- Positioning: Generate reviewable safety evidence for AI-agent-generated pull requests.
- Primary route: Product -> Architecture -> Expert/Security -> QA -> Implementation -> Completion readiness

## PRD

### Problem

Move Safe Agent Operations from config scanning into PR review and CI evidence.

### Users

- Developers adopting AI agents or MCP tools
- Platform, DevTools, Security, and AI infrastructure teams
- Maintainers who need reviewable evidence rather than vague AI automation claims

### Goals

- scope summary
- sensitive file changes
- test evidence
- dependency and CI/auth/infra changes
- reviewer checklist

### Non-Goals

- not a generic code review bot
- not an autonomous merge gate
- not a hosted dashboard in the first version

### Acceptance Criteria

- The project can explain its place in Safe Agent Operations in one sentence.
- The first production surface is local-first or review-first, not a hosted dashboard by default.
- Reports, packets, indexes, or labs must be redaction-safe by design.
- Every risky claim links to evidence, rule logic, or an explicit limitation.
- JSON reports expose a schema version so CI consumers can check compatibility.
- Teams can start with a quiet default profile and opt into stricter review gates.
- Existing repositories can adopt baseline gates so only new risk flags fail CI.

## Architecture Brief

### Boundaries

- Keep shared workflow knowledge in OPT; keep project-specific decisions in this repository.
- Keep the main entrypoint small and explicit.
- Prefer file-based artifacts over hidden services for the first production surface.

### Data Flow

```text
input evidence -> normalize -> redact -> evaluate -> render reviewable artifact
```

### Risks

- Overclaiming safety guarantees.
- Creating generic tooling that weakens the Agentic DevSecOps signal.
- Accepting real secrets or private user data into fixtures.

## QA Plan

- Unit-test redaction and normalization before rule or report expansion.
- Add positive and negative fixtures for every behavior boundary.
- Verify generated artifacts do not include raw secrets.
- Keep bilingual README guidance aligned.

## Implementation Plan

1. Ship a local-first CLI first: `agent-pr-evidence collect --base REF --head REF`.
2. Produce Markdown and JSON evidence from deterministic git diff data.
3. Accept optional test logs and redact secret-like values before rendering.
4. Ship a read-only GitHub Action that writes PR evidence to `GITHUB_STEP_SUMMARY`.
5. Support `.agent-pr-evidence.yml` with schema versioning, profiles, and disabled risk flags.
6. Support baseline review gates for existing-risk adoption.
7. Defer GitHub App permissions and PR comment posting until the skipped inputs are resolved.
8. Use feature branches named `feat/<scope>` or `docs/<scope>`.
9. Use Conventional/Angular commits such as `feat: add packet schema` or `docs: clarify deferred scope`.
10. Never push directly to `main`; open a pull request from the feature branch.

## Skipped Inputs

- GitHub App vs Action decision
- private PR samples
- compliance wording
