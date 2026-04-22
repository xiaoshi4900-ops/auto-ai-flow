# P10 Run Detail

## Route

- `/runs/:id`

## Goal

Render one run as a debuggable execution record while clearly marking optional enriched fields.

## Delegation Packet

- [P10-run-detail.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P10-run-detail.packet.md)

## Development Location

### Primary Docs

- [P10-run-detail.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P10-run-detail.md)
- [run-execution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/run-execution.md)
- [workflow-runtime.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/workflow-runtime.md)
- [run-query.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/run-query.md)
- [P10-run-detail.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P10-run-detail.packet.md)

### Frontend Code

- [RunDetailPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/runs/RunDetailPage.vue)
- [useRunPolling.ts](/C:/workspace/AutoAiFlow/frontend/src/composables/useRunPolling.ts)
- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/api/execution.ts)
- [run.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/run.ts)
- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/types/execution.ts)

### Tests

- [p10-run-detail-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p10-run-detail-5d.spec.ts)
## Task Mode

- `refactor`

## First Action

1. Read `Development Location` in this file.
2. Open the listed code files before changing anything.
3. Confirm field mapping and state mapping before editing.

## Test Policy

- do not start by running tests
- only run the page-level test file listed in `Development Location`
- do not run full Playwright or broad backend suites unless explicitly requested

## Do Not Start With

- `npm exec playwright test`
- full backend test commands
- editing files outside `Allowed Write Files`
## Cross-page Entity Contract

- [run.md](/C:/workspace/AutoAiFlow/docs/spec-v2/entities/run.md)
- [06-mapping-ownership.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/06-mapping-ownership.md)

## Read First

- [run-execution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/run-execution.md)
- [workflow-runtime.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/workflow-runtime.md)
- [run-query.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/run-query.md)
- [p10-run-detail-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p10-run-detail-5d.spec.ts)
- [RunDetailPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/runs/RunDetailPage.vue)
- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/types/execution.ts)

## Allowed Write Files

- `frontend/src/pages/runs/RunDetailPage.vue`
- `frontend/src/composables/useRunPolling.ts`
- `frontend/src/api/execution.ts`
- `frontend/src/stores/run.ts`
- `frontend/src/types/execution.ts`
- `frontend/tests/e2e/p10-run-detail-5d.spec.ts`

## Forbidden

- do not collapse structured output and handoff into raw logs only
- do not assume `structured_output`, `handoff`, `latency_ms`, or `token_usage_total` are always present in backend response
- do not break back navigation

## API Mapping

- `run.id -> header run id`
- `run.status -> run-status-chip`
- `run.error_message -> header or error region`
- `run.started_at/finished_at -> run time summary`
- `node_runs[] -> timeline`
- `node_runs[].output_data -> per-node output region`
- `latency_ms -> run-meta-latency` only when present
- `token_usage_total -> run-meta-tokens` only when present
- `structured_output -> dedicated output viewer` only when present
- `handoff -> dedicated handoff region` only when present

## State Mapping

- loaded: page, header, timeline visible
- running: polling active
- failed: header and node regions surface error
- load error: `run-code-runtime-load-error` visible
- code runtime mode: `run-code-iterations-region` visible

## 5D Execution Targets

- D1: header, timeline, output regions visible
- D2: back action returns to run list
- D3: failed status, latency, token values map to fixed slots when present
- D4: load error and runtime mode states show dedicated regions
- D5: code iteration region uses dedicated items, not generic logs




