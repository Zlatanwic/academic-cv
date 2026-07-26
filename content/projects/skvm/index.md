---
title: "SkVM: A Skill Compilation and Runtime System for Heterogeneous LLM and Agent Harnesses"
summary: Compilation and runtime techniques for portable, parallel agent-harness execution.
tags:
  - LLM Agents
  - TypeScript
  - Bun
  - Docker
  - Compilers
---

SkVM is an SJTU-IPADS project exploring compilation and runtime support for
heterogeneous LLM and agent harnesses. The broader system is associated with
work accepted to SOSP 2026; this page describes my implementation
contributions rather than asserting a publication authorship record.

- Implemented containerized execution modes for four agent adapters:
  pi, claude-code, opencode, and hermes.
- Introduced three levels of parallelism—DLP, ILP, and TLP—into pass 3 of the
  AOT compiler and enabled parallel dispatch for ILP tool calls.
- Added multi-role agent optimization to the JIT optimization stage and
  compared it with multi-turn agent optimization.
