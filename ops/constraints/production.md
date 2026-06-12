# Production Constraints

- This is not a demo repository. Every shipped behavior must be usable in a real review workflow.
- Do not claim runtime protection, sandboxing, or complete security coverage unless the implementation truly provides it.
- Redaction is mandatory before sharing evidence, packets, reports, or examples.
- Prefer deterministic local behavior before introducing hosted services.
- GitHub Action behavior must stay read-only by default: write `GITHUB_STEP_SUMMARY` and outputs, but do not post PR comments or request write permissions until real workflows justify it.
- Profiles must be quiet by default and explicit when strict; teams should opt into additional noise such as missing test evidence.
- Baseline gates must fail only on newly introduced risk flags, not on already accepted repository state.
- Rule changes must add or update fixture corpus cases for both the intended signal and the closest false-positive boundary.
- Keep failure modes explicit and documented.
- Every rule, score, label, or scenario must have evidence or a limitation note.
