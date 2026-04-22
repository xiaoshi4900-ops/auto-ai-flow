# AutoAiFlow Spec v2

## Purpose

This is the active knowledge base for implementation.

It is optimized for short-context AI execution and paired with `docs/task-packets/`
for external AI delegation.

## How Another AI Finds The Right Place To Work

Every page, API, and backend spec now includes `## Development Location` near the top.
That section directly lists:

1. which spec file is the source of truth
2. which code files are expected to be edited
3. which test files verify the change
4. which task packet to use for delegation

If an executor cannot identify where to work, it should start from the relevant
`## Development Location` block instead of guessing from the repository tree.

## Active Indexes

- [core/01-loading-rules.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/01-loading-rules.md)
- [core/04-contract-resolution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/04-contract-resolution.md)
- [core/05-execution-modes.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/05-execution-modes.md)
- [core/06-mapping-ownership.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/06-mapping-ownership.md)
- [entities/README.md](/C:/workspace/AutoAiFlow/docs/spec-v2/entities/README.md)
- [pages/README.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/README.md)
- [apis/README.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/README.md)
- [backend/README.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/README.md)
- [task-packets/README.md](/C:/workspace/AutoAiFlow/docs/task-packets/README.md)
