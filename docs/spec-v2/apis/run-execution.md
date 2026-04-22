# API Packet: Run And Execution

## Development Location

### Spec Docs

- [run-execution.md](docs/spec-v2/apis/run-execution.md)
- [workflow-runtime.md](docs/spec-v2/backend/workflow-runtime.md)
- [run-query.md](docs/spec-v2/backend/run-query.md)

### Backend Code

- [executions.py](backend/app/api/v1/executions.py)
- [runs.py](backend/app/api/v1/runs.py)
- [execution.py](backend/app/schemas/execution.py)
- [execution_service.py](backend/app/services/execution_service.py)
- [code_runtime.py](backend/app/api/v1/code_runtime.py)
- [code_runtime_service.py](backend/app/services/code_runtime_service.py)

### Frontend Code

- [execution.ts](frontend/src/api/execution.ts)
- [run.ts](frontend/src/stores/run.ts)
- [execution.ts](frontend/src/types/execution.ts)
- [RunListPage.vue](frontend/src/pages/runs/RunListPage.vue)
- [RunDetailPage.vue](frontend/src/pages/runs/RunDetailPage.vue)
- [useRunPolling.ts](frontend/src/composables/useRunPolling.ts)

### Tests

- [test_execution_schema.py](backend/tests/contract/test_execution_schema.py)
- [test_run_api.py](backend/tests/integration/test_run_api.py)
- [p08-workflow-editor-5d.spec.ts](frontend/tests/e2e/p08-workflow-editor-5d.spec.ts)
- [p09-run-list-5d.spec.ts](frontend/tests/e2e/p09-run-list-5d.spec.ts)
- [p10-run-detail-5d.spec.ts](frontend/tests/e2e/p10-run-detail-5d.spec.ts)
## Cross-page Entity Contract

- [run.md](docs/spec-v2/entities/run.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Actual Routes

- `POST /api/v1/executions/trigger`
- `GET /api/v1/runs?workflow_id={id}&page={n}&page_size={n}`
- `GET /api/v1/runs/{id}`
- extra runtime routes may exist under `code_runtime`

## Request Contracts

### `POST /api/v1/executions/trigger`

- `workflow_id: number`
- `input_payload?: object | null`

## Response Contracts

- `ExecutionTriggerResponse`: `run_id`, `status`, `message`
- `RunResponse`: `id`, `workflow_id`, `status`, `input_payload`, `output_payload`, `error_message`, `started_at`, `finished_at`, `created_at`
- `NodeRunResponse`: `id`, `workflow_run_id`, `node_key`, `node_type`, `status`, `input_data`, `output_data`, `error_message`, `started_at`, `finished_at`, `duration_ms`
- `RunDetailResponse`: `run`, `node_runs`

## Frontend View-Model Extensions

The frontend run types currently allow:

- `latency_ms?: number`
- `token_usage_total?: number`
- `workflow?: string`
- `trigger_user?: string`
- `structured_output?: string`
- `handoff?: { message?: string; artifacts?: string[] }`

These are not all present in backend schema. If a page depends on them, document derivation or add backend contract explicitly.

## Consumers

- `P08`
- `P09`
- `P10`


