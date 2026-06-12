# agent-pr-evidence Product Foundation

## Intake

- Priority: P1
- Status: reserved production foundation
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

1. Keep this foundation branch small and reviewable.
2. Add the first executable surface only after the missing inputs are resolved or explicitly skipped.
3. Use feature branches named `feat/<scope>` or `docs/<scope>`.
4. Use Conventional/Angular commits such as `feat: add packet schema` or `docs: clarify deferred scope`.
5. Never push directly to `main`; open a pull request from the feature branch.

## Skipped Inputs

- GitHub App vs Action decision
- private PR samples
- compliance wording
