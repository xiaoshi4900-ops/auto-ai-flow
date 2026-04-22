# API Packet: Workflow

## Development Location

### Spec Docs

- [workflow.md](docs/spec-v2/apis/workflow.md)
- [workflow-runtime.md](docs/spec-v2/backend/workflow-runtime.md)

### Backend Code

- [workflows.py](backend/app/api/v1/workflows.py)
- [workflow.py](backend/app/schemas/workflow.py)
- [workflow_service.py](backend/app/services/workflow_service.py)

### Frontend Code

- [workflow.ts](frontend/src/api/workflow.ts)
- [workflow.ts](frontend/src/stores/workflow.ts)
- [workflow.ts](frontend/src/types/workflow.ts)
- [WorkflowListPage.vue](frontend/src/pages/workflows/WorkflowListPage.vue)
- [WorkflowEditorPage.vue](frontend/src/pages/workflows/WorkflowEditorPage.vue)

### Tests

- [test_workflow_schema.py](backend/tests/contract/test_workflow_schema.py)
- [test_workflow_api.py](backend/tests/integration/test_workflow_api.py)
- [p07-workflow-list-5d.spec.ts](frontend/tests/e2e/p07-workflow-list-5d.spec.ts)
- [p08-workflow-editor-5d.spec.ts](frontend/tests/e2e/p08-workflow-editor-5d.spec.ts)
## Cross-page Entity Contract

- [workflow.md](docs/spec-v2/entities/workflow.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Actual Routes

- `GET /api/v1/workflows?project_id={id}&page={n}&page_size={n}`
- `POST /api/v1/workflows`
- `GET /api/v1/workflows/{id}`
- `PUT /api/v1/workflows/{id}`
- `DELETE /api/v1/workflows/{id}`

## Request Contracts

### `POST /api/v1/workflows`

- `project_id: number`
- `name: string`
- `description?: string | null`
- `nodes?: WorkflowNodeSchema[]`
- `edges?: WorkflowEdgeSchema[]`

### `PUT /api/v1/workflows/{id}`

- `name?: string`
- `description?: string | null`
- `nodes?: WorkflowNodeSchema[]`
- `edges?: WorkflowEdgeSchema[]`
- `canvas_data?: object | null`

## Response Contracts

- `WorkflowNodeSchema`: `node_key`, `node_type`, `label`, `config`, `position_x`, `position_y`
- `WorkflowEdgeSchema`: `source_node_key`, `target_node_key`, `condition`, `label`
- `WorkflowResponse`: `id`, `project_id`, `name`, `description`, `nodes`, `edges`, `canvas_data`, `created_at`, `updated_at`

## Frontend View-Model Extensions

The frontend workflow type currently allows:

- `status?: string`
- `version?: number`
- `updated_relative?: string`

These are not in backend schema. Treat them as derived UI fields unless backend changes contract.

## Consumers

- `P07`
- `P08`


