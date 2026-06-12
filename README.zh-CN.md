# agent-pr-evidence

语言： [English](./README.md) | 中文

为 AI agent 生成的 PR 生成可审查的安全与交付证据。

## 状态

`P1` - reserved production foundation。

## 目的

Move Safe Agent Operations from config scanning into PR review and CI evidence.

## 第一生产化表面

GitHub Action and CLI that produce a Markdown/JSON PR evidence packet.

## 必要证据

- scope summary
- sensitive file changes
- test evidence
- dependency and CI/auth/infra changes
- reviewer checklist

## 非目标

- not a generic code review bot
- not an autonomous merge gate
- not a hosted dashboard in the first version

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
