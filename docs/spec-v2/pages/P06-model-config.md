# P06 Model Config

## Route

- `/models`

## Goal

Manage model configuration while respecting backend/frontend field mismatches explicitly.

## Delegation Packet

- [P06-model-config.packet.md](docs/task-packets/P06-model-config.packet.md)

## Development Location

### Primary Docs

- [P06-model-config.md](docs/spec-v2/pages/P06-model-config.md)
- [model.md](docs/spec-v2/apis/model.md)
- [project-agent.md](docs/spec-v2/backend/project-agent.md)
- [P06-model-config.packet.md](docs/task-packets/P06-model-config.packet.md)

### Frontend Code

- [ModelConfigPage.vue](frontend/src/pages/models/ModelConfigPage.vue)
- [model.ts](frontend/src/api/model.ts)
- [model.ts](frontend/src/types/model.ts)

### Tests

- [p06-model-config-5d.spec.ts](frontend/tests/e2e/p06-model-config-5d.spec.ts)
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
## Read First

- [model.md](docs/spec-v2/apis/model.md)
- [p06-model-config-5d.spec.ts](frontend/tests/e2e/p06-model-config-5d.spec.ts)
- [ModelConfigPage.vue](frontend/src/pages/models/ModelConfigPage.vue)
- [model.ts](frontend/src/types/model.ts)

## Allowed Write Files

- `frontend/src/pages/models/ModelConfigPage.vue`
- `frontend/src/api/model.ts`
- `frontend/src/types/model.ts`
- `frontend/tests/e2e/p06-model-config-5d.spec.ts`

## Forbidden

- do not silently rename backend fields without adapter code and docs
- do not print secrets
- do not modify agent edit or project pages in this task

## API Mapping

- backend `provider.name -> provider display`
- backend `provider.provider_type -> provider type badge`
- backend `provider.api_base -> optional host display`
- backend `model.name/model_id -> frontend display strategy must be explicit`
- `model_definition_id -> config binding`
- `is_default -> default badge`

## State Mapping

- empty: `model-empty-state` visible, zero `model-row-*`
- add dialog open: visible after `model-add-config-btn` click
- create success: selected model visible in config list

## 5D Execution Targets

- D1: list region, default indicator, add action visible
- D2: add action opens dialog and confirm submits
- D3: provider/model/default fields map from actual response or explicit adapter
- D4: empty state suppresses fake table shell
- D5: row count equals visible configs; secret values never render



