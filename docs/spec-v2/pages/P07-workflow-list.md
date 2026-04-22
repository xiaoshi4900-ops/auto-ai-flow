# P07 Workflow List

## Route

- `/workflows`

## Goal

Render workflow assets with explicit separation between API contract and derived UI fields.

## Delegation Packet

- [P07-workflow-list.packet.md](docs/task-packets/P07-workflow-list.packet.md)

## Development Location

### Primary Docs

- [P07-workflow-list.md](docs/spec-v2/pages/P07-workflow-list.md)
- [workflow.md](docs/spec-v2/apis/workflow.md)
- [workflow-runtime.md](docs/spec-v2/backend/workflow-runtime.md)
- [P07-workflow-list.packet.md](docs/task-packets/P07-workflow-list.packet.md)

### Frontend Code

- [WorkflowListPage.vue](frontend/src/pages/workflows/WorkflowListPage.vue)
- [workflow.ts](frontend/src/api/workflow.ts)
- [workflow.ts](frontend/src/stores/workflow.ts)
- [workflow.ts](frontend/src/types/workflow.ts)

### Tests

- [p07-workflow-list-5d.spec.ts](frontend/tests/e2e/p07-workflow-list-5d.spec.ts)
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
- [p07-workflow-list-5d.spec.ts](frontend/tests/e2e/p07-workflow-list-5d.spec.ts)
- [WorkflowListPage.vue](frontend/src/pages/workflows/WorkflowListPage.vue)

## Allowed Write Files

- `frontend/src/pages/workflows/WorkflowListPage.vue`
- `frontend/src/api/workflow.ts`
- `frontend/src/stores/workflow.ts`
- `frontend/src/types/workflow.ts`
- `frontend/tests/e2e/p07-workflow-list-5d.spec.ts`

## Forbidden

- do not assume `status`, `version`, or `updated_relative` are API fields
- do not hide edit/run actions behind inaccessible menus

## API Mapping

- `name -> workflow card title`
- `nodes.length -> node count`
- `updated_at -> update text source`
- `status/version/updated_relative -> derived only if explicitly computed`

## State Mapping

- empty: `workflow-empty-state` visible
- populated: `workflow-card-item` count equals items length
- create: `workflow-col-create` opens dialog

## 5D Execution Targets

- D1: header, create, filters, card region visible
- D2: create opens dialog, card actions discoverable
- D3: card fields map from response or documented derivation
- D4: empty state suppresses fake rows
- D5: card count equals API count




