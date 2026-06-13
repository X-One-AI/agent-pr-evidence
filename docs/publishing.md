# Publishing

`agent-pr-evidence` uses GitHub Actions and PyPI Trusted Publishing. Trusted Publishing uses OpenID Connect, not a long-lived package token.

Python distribution package:

```text
xone-agent-pr-evidence
```

Installed CLI:

```text
agent-pr-evidence
```

## Current Index Status

As of 2026-06-13, public API checks show:

- PyPI: `xone-agent-pr-evidence` is not published yet.
- TestPyPI: `xone-agent-pr-evidence` is not published yet.

## GitHub Environments

Create these GitHub environments:

- `testpypi`
- `pypi`

The `pypi` environment should require manual approval.

## Trusted Publisher Settings

Configure Trusted Publishers in TestPyPI and PyPI:

```text
Project: xone-agent-pr-evidence
Owner: X-One-AI
Repository: agent-pr-evidence
Workflow: publish.yml
Environment: testpypi or pypi
```

## Publish Order

1. Merge and verify a green CI run on `main`.
2. Confirm the release tag exists, for example `v0.4.1`.
3. Run `Publish Python Package` with `repository = testpypi`.
4. Verify a clean TestPyPI install.
5. Run `Publish Python Package` with `repository = pypi` from a release tag after approval.
6. Verify a clean PyPI install.

## TestPyPI Install Check

```bash
python -m venv /tmp/agent-pr-evidence-testpypi
/tmp/agent-pr-evidence-testpypi/bin/python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  xone-agent-pr-evidence
/tmp/agent-pr-evidence-testpypi/bin/agent-pr-evidence --version
```

## PyPI Install Check

```bash
python -m venv /tmp/agent-pr-evidence-pypi
/tmp/agent-pr-evidence-pypi/bin/python -m pip install xone-agent-pr-evidence
/tmp/agent-pr-evidence-pypi/bin/agent-pr-evidence --version
```

## GitHub Release Install Path

```bash
python3 -m pip install https://github.com/X-One-AI/agent-pr-evidence/releases/download/v0.4.1/xone_agent_pr_evidence-0.4.1-py3-none-any.whl
agent-pr-evidence --version
```
