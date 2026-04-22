# P08 Workflow Editor

## Route

- `/workflows/:id/editor`

## Goal

Deliver one-screen editing and runtime observation with a stable save and run contract.

## Delegation Packet

- [P08-workflow-editor.packet.md](docs/task-packets/P08-workflow-editor.packet.md)

## Development Location

### Primary Docs

- [P08-workflow-editor.md](docs/spec-v2/pages/P08-workflow-editor.md)
- [workflow.md](docs/spec-v2/apis/workflow.md)
- [run-execution.md](docs/spec-v2/apis/run-execution.md)
- [workflow-runtime.md](docs/spec-v2/backend/workflow-runtime.md)
- [P08-workflow-editor.packet.md](docs/task-packets/P08-workflow-editor.packet.md)

### Frontend Code

- [WorkflowEditorPage.vue](frontend/src/pages/workflows/WorkflowEditorPage.vue)
- [workflow.ts](frontend/src/api/workflow.ts)
- [execution.ts](frontend/src/api/execution.ts)
- [workflow.ts](frontend/src/stores/workflow.ts)
- [workflow.ts](frontend/src/types/workflow.ts)
- [WorkflowCanvas.vue](frontend/src/components/workflows/WorkflowCanvas.vue)
- [NodeConfigPanel.vue](frontend/src/components/workflows/NodeConfigPanel.vue)
- [NodePalette.vue](frontend/src/components/workflows/NodePalette.vue)

### Tests

- [p08-workflow-editor-5d.spec.ts](frontend/tests/e2e/p08-workflow-editor-5d.spec.ts)
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

- [workflow.md](docs/spec-v2/entities/workflow.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Read First

- [workflow.md](docs/spec-v2/apis/workflow.md)
- [run-execution.md](docs/spec-v2/apis/run-execution.md)
- [workflow-runtime.md](docs/spec-v2/backend/workflow-runtime.md)
- [p08-workflow-editor-5d.spec.ts](frontend/tests/e2e/p08-workflow-editor-5d.spec.ts)
- [WorkflowEditorPage.vue](frontend/src/pages/workflows/WorkflowEditorPage.vue)
- [workflow.ts](frontend/src/stores/workflow.ts)
- [WorkflowCanvas.vue](frontend/src/components/workflows/WorkflowCanvas.vue)
- [NodeConfigPanel.vue](frontend/src/components/workflows/NodeConfigPanel.vue)

## Allowed Write Files

- `frontend/src/pages/workflows/WorkflowEditorPage.vue`
- `frontend/src/components/workflows/WorkflowCanvas.vue`
- `frontend/src/components/workflows/NodeConfigPanel.vue`
- `frontend/src/components/workflows/NodePalette.vue`
- `frontend/src/api/workflow.ts`
- `frontend/src/api/execution.ts`
- `frontend/src/stores/workflow.ts`
- `frontend/src/types/workflow.ts`
- `frontend/tests/e2e/p08-workflow-editor-5d.spec.ts`

## Forbidden

- do not modify run detail page in this task
- do not invent save payload keys outside `WorkflowUpdateRequest`
- do not remove canvas, inspector, or runtime panel

## API Mapping

- `WorkflowResponse.name -> editor-workflow-name`
- `WorkflowResponse.nodes -> canvas nodes`
- `WorkflowResponse.edges -> canvas edges`
- `WorkflowResponse.canvas_data -> viewport/layout state`
- save payload may contain only `name`, `description`, `nodes`, `edges`, `canvas_data`
- `workflow_id -> POST /api/v1/executions/trigger`
- `ExecutionTriggerResponse.run_id -> runtime notice`

## State Mapping

- loaded: toolbar, body, canvas visible
- no selection: inspector shows empty guidance or default panel
- node selected: inspector reflects selected node config
- run success: structured output and handoff regions visible
- save success: visible success toast/text

## 5D Execution Targets

- D1: toolbar, body, palette/canvas/inspector/runtime visible
- D2: run and save actions work
- D3: workflow name maps to header; run id maps to runtime notice
- D4: selection and run state update UI regions
- D5: one canvas, one inspector, one runtime panel; save payload obeys schema




