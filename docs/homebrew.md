# Homebrew Packaging

`agent-pr-evidence` is distributed through the X-One tap.

## User Install

```bash
brew tap x-one-ai/tap
brew trust --formula x-one-ai/tap/agent-pr-evidence
brew install x-one-ai/tap/agent-pr-evidence
agent-pr-evidence --version
```

## Tap Repository

```text
X-One-AI/homebrew-tap
```

Formula path:

```text
Formula/agent-pr-evidence.rb
```

## Formula Requirements

- Install the Python CLI as `agent-pr-evidence`.
- Use the released `xone-agent-pr-evidence` source distribution.
- Vendor Python dependencies as Homebrew resources.
- Run `agent-pr-evidence --version` in the formula test.

## Current Target

```text
xone-agent-pr-evidence==0.4.1
```
