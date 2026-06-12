# agent-pr-evidence

语言： [English](./README.md) | 中文

为 AI agent 生成的 PR 生成可审查的安全与交付证据。

## 状态

`P1` - early production 本地 CLI。

## 目的

把 Safe Agent Operations 从配置扫描推进到 PR 审查和 CI 证据链。

## 第一生产化表面

本地 CLI 和 GitHub Action：基于 git base/head diff 生成 Markdown/JSON PR evidence packet。GitHub App 表面等权限模型和真实 PR 样本明确后再做。

## 安装

在本仓库中运行：

```bash
python3 -m pip install -e .
agent-pr-evidence --version
```

## 使用

从 git diff 收集本地 PR evidence：

```bash
agent-pr-evidence collect --base origin/main --head HEAD --format markdown
agent-pr-evidence collect --base origin/main --head HEAD --format json --output pr-evidence.json
agent-pr-evidence collect --base origin/main --head HEAD --test-log pytest.log
```

第一生产化表面是 local-first。它不需要 GitHub App 权限，也不会上传仓库数据。

## GitHub Action

在 `actions/checkout` 之后使用，并确保 checkout 有足够历史用于 base/head diff：

```yaml
name: Agent PR Evidence

on:
  pull_request:

permissions:
  contents: read

jobs:
  evidence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - uses: X-One-AI/agent-pr-evidence@feat/local-pr-evidence-cli
        with:
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          output: agent-pr-evidence.md
```

Action 会把报告写入 `GITHUB_STEP_SUMMARY`，并暴露 `report-path` 和 `summary-json` outputs。默认不申请写权限，也不自动发布 PR comment。

## 必要证据

- 范围摘要
- 敏感文件变更
- 测试证据
- 依赖和 CI/auth/infra 变更
- reviewer checklist

## 当前限制

- 默认不发布 PR comment。
- GitHub App 权限仍等待真实 review workflow 后再定。
- 规则边界还需要真实 PR 的误报/漏报调优。

## 非目标

- 不做通用 code review bot
- 不做自动合并 gate
- 第一版不做 hosted dashboard

## OPT 运行模型

本项目通过 [ops/opt-overlay.md](./ops/opt-overlay.md) 引用共享 One Person Team 工作流。项目自己的约束放在 [ops/constraints](./ops/constraints)，可演进 skill 放在 [ops/skills](./ops/skills)。

## 暂缺输入

需要用户或真实世界数据补充的内容记录在 `../x-one-skipped-inputs.md`，不阻塞基础建设。

## 文档

- [产品基础](./docs/product-foundation.md)
- [OPT Overlay](./ops/opt-overlay.md)
- [生产约束](./ops/constraints/production.md)
- [主入口约束](./ops/constraints/main-entry.md)
- [Skill 演进](./ops/skills/evolution.md)
