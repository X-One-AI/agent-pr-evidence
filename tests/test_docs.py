from pathlib import Path


def test_readmes_and_opt_foundation_stay_aligned():
    english = Path("README.md").read_text(encoding="utf-8")
    chinese = Path("README.zh-CN.md").read_text(encoding="utf-8")
    foundation = Path("docs/product-foundation.md").read_text(encoding="utf-8")
    production = Path("ops/constraints/production.md").read_text(encoding="utf-8")
    skill = Path("ops/skills/evolution.md").read_text(encoding="utf-8")
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "agent-pr-evidence collect" in english
    assert "uses: X-One-AI/agent-pr-evidence" in english
    assert "agent-pr-evidence collect" in chinese
    assert "uses: X-One-AI/agent-pr-evidence" in chinese
    assert "local-first" in foundation
    assert "GitHub Action" in foundation
    assert "not a demo" in production
    assert "read-only by default" in production
    assert "Delete Or Weaken" in skill
    assert "git fetch origin feat/opt-foundation" in ci
