from pathlib import Path


def test_readmes_and_opt_foundation_stay_aligned():
    english = Path("README.md").read_text(encoding="utf-8")
    chinese = Path("README.zh-CN.md").read_text(encoding="utf-8")
    foundation = Path("docs/product-foundation.md").read_text(encoding="utf-8")
    production = Path("ops/constraints/production.md").read_text(encoding="utf-8")
    skill = Path("ops/skills/evolution.md").read_text(encoding="utf-8")

    assert "agent-pr-evidence collect" in english
    assert "agent-pr-evidence collect" in chinese
    assert "local-first" in foundation
    assert "not a demo" in production
    assert "Delete Or Weaken" in skill
