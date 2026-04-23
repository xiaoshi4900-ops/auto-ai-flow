# AutoAiFlow Spec v1.3

## Purpose

This version defines the execution architecture for AutoAiFlow.

It does not replace the page-level packets in `docs/spec-v2/`.
Instead, it adds one layer above them and fixes the runtime direction:

1. outer workflow orchestration remains project-owned
2. inner AI execution is pluggable
3. provider access defaults to `OpenAI-compatible`
4. feature support is capability-driven, not provider-name-driven

## Scope

This version mainly answers four questions:

1. what the platform owns
2. what an executor backend owns
3. how providers are adapted
4. how unsupported features degrade safely

## Active Files

- [execution-architecture.md](docs/spec-v1.3/execution-architecture.md)
- [provider-matrix.md](docs/spec-v1.3/provider-matrix.md)

## Relationship To Spec v2

`docs/spec-v2/` remains the active page/API/backend packet set for implementation.

`docs/spec-v1.3/` is the active runtime architecture overlay that all future
execution-related changes must follow.

If a new task touches:

- workflow orchestration
- agent execution backend
- code runtime loop
- model/provider integration

the executor must read `docs/spec-v1.3/` before editing code.
