# P02 Project List

## Route

- `/projects`

## Goal

Render project cards, support create, and keep UI fully driven by project list data.

## Delegation Packet

- [P02-project-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P02-project-list.packet.md)

## Development Location

### Primary Docs

- [P02-project-list.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P02-project-list.md)
- [project.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/project.md)
- [project-agent.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/project-agent.md)
- [P02-project-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P02-project-list.packet.md)

### Frontend Code

- [ProjectListPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/projects/ProjectListPage.vue)
- [project.ts](/C:/workspace/AutoAiFlow/frontend/src/api/project.ts)
- [project.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/project.ts)
- [project.ts](/C:/workspace/AutoAiFlow/frontend/src/types/project.ts)

### Tests

- [p02-project-list-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p02-project-list-5d.spec.ts)
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

- [project.md](/C:/workspace/AutoAiFlow/docs/spec-v2/entities/project.md)
- [06-mapping-ownership.md](/C:/workspace/AutoAiFlow/docs/spec-v2/core/06-mapping-ownership.md)

## Read First

- [project.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/project.md)
- [project-agent.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/project-agent.md)
- [p02-project-list-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p02-project-list-5d.spec.ts)
- [ProjectListPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/projects/ProjectListPage.vue)
- [project.ts](/C:/workspace/AutoAiFlow/frontend/src/api/project.ts)
- [project.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/project.ts)
- [project.ts](/C:/workspace/AutoAiFlow/frontend/src/types/project.ts)

## Allowed Write Files

- `frontend/src/pages/projects/ProjectListPage.vue`
- `frontend/src/api/project.ts`
- `frontend/src/stores/project.ts`
- `frontend/src/types/project.ts`
- `frontend/tests/e2e/p02-project-list-5d.spec.ts`

## Forbidden

- do not add new backend project fields unless backend schema changes too
- do not convert card layout back into generic table layout
- do not modify project detail or workflow files in this task
- do not treat `status` and `updated_relative` as guaranteed API fields

## API Mapping

- `id -> project-card-item key`
- `name -> project-card-name`
- `description -> project card description region`
- `updated_at -> source for project-card-updated`
- `status -> derived only if frontend has a deterministic rule`
- `updated_relative -> derived display text only`
- create body: `name`, `description`, optional `default_model_id`

## State Mapping

- empty: show `project-empty-state`, zero `project-card-item`, zero hidden table header
- populated: count of `project-card-item` equals `items.length`
- create dialog open: modal visible after `projects-card-create` click
- create success: new project name visible in list
- error: error stays in list region, page shell remains mounted

## 5D Execution Targets

- D1: `projects-workspace-page`, `projects-stats-row`, `projects-card-region`
- D2: `projects-card-create` opens dialog
- D3: `name`, `status`, `updated_*` display in fixed card slots
- D4: empty state suppresses fake rows and `No Data`
- D5: created item appears after valid payload submit; card count matches API count




