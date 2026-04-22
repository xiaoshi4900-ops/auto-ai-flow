# API Packet: Run And Execution

## Development Location

### Spec Docs

- [run-execution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/run-execution.md)
- [workflow-runtime.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/workflow-runtime.md)
- [run-query.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/run-query.md)

### Backend Code

- [executions.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/executions.py)
- [runs.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/runs.py)
- [execution.py](/C:/workspace/AutoAiFlow/backend/app/schemas/execution.py)
- [execution_service.py](/C:/workspace/AutoAiFlow/backend/app/services/execution_service.py)
- [code_runtime.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/code_runtime.py)
- [code_runtime_service.py](/C:/workspace/AutoAiFlow/backend/app/services/code_runtime_service.py)

### Frontend Code

- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/api/execution.ts)
- [run.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/run.ts)
- [execution.ts](/C:/workspace/AutoAiFlow/frontend/src/types/execution.ts)
- [RunListPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/runs/RunListPage.vue)
- [RunDetailPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/runs/RunDetailPage.vue)
- [useRunPolling.ts](/C:/workspace/AutoAiFlow/frontend/src/composables/useRunPolling.ts)

### Tests

- [test_execution_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_execution_schema.py)
- [test_run_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_run_api.py)
- [p08-workflow-editor-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p08-workflow-editor-5d.spec.ts)
- [p09-run-list-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p09-run-list-5d.spec.ts)
- [p10-run-detail-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p10-run-detail-5d.spec.ts)
## Cross-page Entity Contract

- [run.md](/C:/workspace/AutoAiFlow/docs/spec-v2/entities/run.md)
- [06-mapping-ownership.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/06-mapping-ownership.md)

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


