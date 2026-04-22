# P09 Run List

## Route

- `/runs`

## Goal

List runs using actual run query contract plus explicit optional metrics fields.

## Delegation Packet

- [P09-run-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P09-run-list.packet.md)

## Development Location

### Primary Docs

- [P09-run-list.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P09-run-list.md)
- [run-execution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/run-execution.md)
- [run-query.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/run-query.md)
- [P09-run-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P09-run-list.packet.md)

### Frontend Code

- [RunListPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/runs/RunListPage.vue)
- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/api/execution.ts)
- [run.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/run.ts)
- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/types/execution.ts)

### Tests

- [p09-run-list-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p09-run-list-5d.spec.ts)
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
- [run-query.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/run-query.md)
- [p09-run-list-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p09-run-list-5d.spec.ts)
- [RunListPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/runs/RunListPage.vue)

## Allowed Write Files

- `frontend/src/pages/runs/RunListPage.vue`
- `frontend/src/api/execution.ts`
- `frontend/src/stores/run.ts`
- `frontend/src/types/execution.ts`
- `frontend/tests/e2e/p09-run-list-5d.spec.ts`

## Forbidden

- do not assume `latency_ms` and `token_usage_total` always exist
- do not remove filter query-state behavior

## API Mapping

- `id -> row key and detail route`
- `status -> run-status badge`
- `started_at -> start time`
- `latency_ms -> optional metric slot`
- `token_usage_total -> optional token slot`

## State Mapping

- empty: `run-empty-state` visible, zero run rows, no `No Data`
- filtered: route query reflects selected status
- detail click: navigates to `/runs/{id}`

## 5D Execution Targets

- D1: header, filters, list region visible
- D2: row detail action navigates
- D3: status/latency/token fields map to row slots
- D4: empty state suppresses fake table placeholder
- D5: row count equals API count




