# P04 Agent List

## Route

- `/agents`

## Goal

Render agents as role cards for one project, not as raw database rows.

## Delegation Packet

- [P04-agent-list.packet.md](docs/task-packets/P04-agent-list.packet.md)

## Development Location

### Primary Docs

- [P04-agent-list.md](docs/spec-v2/pages/P04-agent-list.md)
- [agent.md](docs/spec-v2/apis/agent.md)
- [project-agent.md](docs/spec-v2/backend/project-agent.md)
- [P04-agent-list.packet.md](docs/task-packets/P04-agent-list.packet.md)

### Frontend Code

- [AgentListPage.vue](frontend/src/pages/agents/AgentListPage.vue)
- [agent.ts](frontend/src/api/agent.ts)
- [agent.ts](frontend/src/stores/agent.ts)
- [agent.ts](frontend/src/types/agent.ts)

### Tests

- [p04-agent-list-5d.spec.ts](frontend/tests/e2e/p04-agent-list-5d.spec.ts)
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

- [agent.md](docs/spec-v2/entities/agent.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Read First

- [agent.md](docs/spec-v2/apis/agent.md)
- [p04-agent-list-5d.spec.ts](frontend/tests/e2e/p04-agent-list-5d.spec.ts)
- [AgentListPage.vue](frontend/src/pages/agents/AgentListPage.vue)
- [agent.ts](frontend/src/stores/agent.ts)

## Allowed Write Files

- `frontend/src/pages/agents/AgentListPage.vue`
- `frontend/src/api/agent.ts`
- `frontend/src/stores/agent.ts`
- `frontend/src/types/agent.ts`
- `frontend/tests/e2e/p04-agent-list-5d.spec.ts`

## Forbidden

- do not invent global agent list without `project_id`
- do not assume `model_name` is returned by backend
- do not edit agent edit page in this task

## API Mapping

- `name -> agent card name`
- `role_name -> role label`
- `responsibility -> card responsibility text`
- `skill_ids.length -> skill count`
- `tool_ids.length -> tool count`
- `model_id -> resolve to display text only if model lookup exists`

## State Mapping

- empty: `agents-empty-state` visible, zero `agent-card-item`
- populated: `agent-card-item` count equals list length
- create: `agents-section-create` opens dialog

## 5D Execution Targets

- D1: card grid and filters visible
- D2: create button opens dialog
- D3: card fields map from API fields
- D4: empty state suppresses fake card/table shells
- D5: card count equals API count




