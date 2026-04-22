# P03 Project Detail

## Route

- `/projects/:id`

## Goal

Render a project hub using real project data plus related workflow and run summaries.

## Delegation Packet

- [P03-project-detail.packet.md](docs/task-packets/P03-project-detail.packet.md)

## Development Location

### Primary Docs

- [P03-project-detail.md](docs/spec-v2/pages/P03-project-detail.md)
- [project.md](docs/spec-v2/apis/project.md)
- [workflow.md](docs/spec-v2/apis/workflow.md)
- [run-execution.md](docs/spec-v2/apis/run-execution.md)
- [P03-project-detail.packet.md](docs/task-packets/P03-project-detail.packet.md)

### Frontend Code

- [ProjectDetailPage.vue](frontend/src/pages/projects/ProjectDetailPage.vue)
- [project.ts](frontend/src/api/project.ts)
- [workflow.ts](frontend/src/api/workflow.ts)
- [execution.ts](frontend/src/api/execution.ts)
- [project.ts](frontend/src/stores/project.ts)
- [workflow.ts](frontend/src/stores/workflow.ts)
- [run.ts](frontend/src/stores/run.ts)

### Tests

- [p03-project-detail-5d.spec.ts](frontend/tests/e2e/p03-project-detail-5d.spec.ts)
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

- [project.md](docs/spec-v2/entities/project.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Read First

- [project.md](docs/spec-v2/apis/project.md)
- [workflow.md](docs/spec-v2/apis/workflow.md)
- [run-execution.md](docs/spec-v2/apis/run-execution.md)
- [p03-project-detail-5d.spec.ts](frontend/tests/e2e/p03-project-detail-5d.spec.ts)
- [ProjectDetailPage.vue](frontend/src/pages/projects/ProjectDetailPage.vue)

## Allowed Write Files

- `frontend/src/pages/projects/ProjectDetailPage.vue`
- `frontend/src/api/project.ts`
- `frontend/src/api/workflow.ts`
- `frontend/src/api/execution.ts`
- `frontend/src/stores/project.ts`
- `frontend/src/stores/workflow.ts`
- `frontend/src/stores/run.ts`
- `frontend/tests/e2e/p03-project-detail-5d.spec.ts`

## Forbidden

- do not invent project-scoped backend paths that do not exist
- do not fake related resource cards when API returns empty arrays
- do not modify project list layout in this task

## API Mapping

- `project.name -> project title`
- `project.description -> summary description`
- `project.updated_at -> summary last updated display`
- `workflow.id -> recent workflow item target`
- `workflow.name -> recent workflow title`
- `run.id -> recent run item target`
- `run.status -> recent run badge`

## State Mapping

- workflow empty: show `project-detail-workflows-empty-state`
- run empty: show `project-detail-runs-empty-state`
- click recent workflow: navigate to `/workflows/{id}/editor`
- page error: preserve return path to list

## 5D Execution Targets

- D1: summary panel plus recent workflow/run regions visible
- D2: `project-recent-workflow-item` click navigates to editor
- D3: summary and related resource fields map into fixed slots
- D4: workflow and run regions may empty independently
- D5: recent item counts equal returned arrays




