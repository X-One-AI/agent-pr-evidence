from pathlib import Path


def test_readmes_and_opt_foundation_stay_aligned():
    english = Path("README.md").read_text(encoding="utf-8")
    chinese = Path("README.zh-CN.md").read_text(encoding="utf-8")
    foundation = Path("docs/product-foundation.md").read_text(encoding="utf-8")
    production = Path("ops/constraints/production.md").read_text(encoding="utf-8")
    skill = Path("ops/skills/evolution.md").read_text(encoding="utf-8")
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    example_config = Path("examples/agent-pr-evidence.yml").read_text(encoding="utf-8")
    example_baseline = Path("examples/baseline.json").read_text(encoding="utf-8")
    manifest = Path("MANIFEST.in").read_text(encoding="utf-8")

    assert "agent-pr-evidence collect" in english
    assert "v0.3.0 released" in english
    assert "uses: X-One-AI/agent-pr-evidence@v0.3.0" in english
    assert "agent-pr-evidence gate" in english
    assert ".agent-pr-evidence.yml" in english
    assert "profile: strict" in english
    assert "agent-pr-evidence collect" in chinese
    assert "v0.3.0 已发布" in chinese
    assert "uses: X-One-AI/agent-pr-evidence@v0.3.0" in chinese
    assert "agent-pr-evidence gate" in chinese
    assert ".agent-pr-evidence.yml" in chinese
    assert "local-first" in foundation
    assert "v0.3.0 released" in foundation
    assert "GitHub Action" in foundation
    assert "schema version" in foundation
    assert "baseline" in foundation
    assert "not a demo" in production
    assert "read-only by default" in production
    assert "Profiles must be quiet by default" in production
    assert "Baseline gates must fail only on newly introduced risk flags" in production
    assert "Delete Or Weaken" in skill
    assert "fetch-depth: 0" in ci
    assert "base_ref=\"$(git rev-parse HEAD^)\"" in ci
    assert 'version = "0.3.0"' in pyproject
    assert "## 0.3.0" in changelog
    assert "GitHub Action" in changelog
    assert "schema_version: 1" in example_config
    assert "profile: strict" in example_config
    assert "agent-pr-evidence.baseline.v1" in example_baseline
    assert "include action.yml" in manifest
    assert "include README.zh-CN.md" in manifest
    assert "recursive-include examples *.yml" in manifest
    assert "recursive-include examples *.json" in manifest
