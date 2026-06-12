# OPT Overlay

This project references the shared One Person Team workflow from `/Users/moquqicha/Documents/AHCode/opt`. Do not modify OPT from inside this repository.

## Local Adaptation

- Use OPT role stages for product, architecture, expert review, QA, implementation, review, and completion readiness.
- Store project-specific constraints under `ops/constraints/`.
- Store project-specific skill evolution notes under `ops/skills/`.
- Promote useful local rules into this repository only after they are proven by fixtures or real use.
- Delete or rewrite local rules that create noise, overclaim safety, or pull the project away from Safe Agent Operations.

## Branch And Commit Rules

- Work on feature branches only.
- Branch examples: `feat/opt-foundation`, `docs/product-scope`, `fix/redaction-boundary`.
- Commit examples: `feat: add product foundation`, `docs: clarify non-goals`, `fix: tighten redaction rule`.
