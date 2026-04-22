# P05 Agent Edit

## Route

- `/agents/:id`

## Goal

Edit agent identity, capabilities, template binding, and policy without guessing fields.

## Delegation Packet

- [P05-agent-edit.packet.md](docs/task-packets/P05-agent-edit.packet.md)

## Development Location

### Primary Docs

- [P05-agent-edit.md](docs/spec-v2/pages/P05-agent-edit.md)
- [agent.md](docs/spec-v2/apis/agent.md)
- [model.md](docs/spec-v2/apis/model.md)
- [project-agent.md](docs/spec-v2/backend/project-agent.md)
- [P05-agent-edit.packet.md](docs/task-packets/P05-agent-edit.packet.md)

### Frontend Code

- [AgentEditPage.vue](frontend/src/pages/agents/AgentEditPage.vue)
- [agent.ts](frontend/src/api/agent.ts)
- [model.ts](frontend/src/api/model.ts)
- [roleTemplate.ts](frontend/src/api/roleTemplate.ts)
- [skill.ts](frontend/src/api/skill.ts)
- [tool.ts](frontend/src/api/tool.ts)
- [agent.ts](frontend/src/stores/agent.ts)
- [agent.ts](frontend/src/types/agent.ts)

### Tests

- [p05-agent-edit-5d.spec.ts](frontend/tests/e2e/p05-agent-edit-5d.spec.ts)
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
- [model.md](docs/spec-v2/apis/model.md)
- [p05-agent-edit-5d.spec.ts](frontend/tests/e2e/p05-agent-edit-5d.spec.ts)
- [AgentEditPage.vue](frontend/src/pages/agents/AgentEditPage.vue)
- [agent.ts](frontend/src/types/agent.ts)

## Allowed Write Files

- `frontend/src/pages/agents/AgentEditPage.vue`
- `frontend/src/api/agent.ts`
- `frontend/src/api/model.ts`
- `frontend/src/api/roleTemplate.ts`
- `frontend/src/api/skill.ts`
- `frontend/src/api/tool.ts`
- `frontend/src/stores/agent.ts`
- `frontend/src/types/agent.ts`
- `frontend/tests/e2e/p05-agent-edit-5d.spec.ts`

## Forbidden

- do not invent response fields not present in backend schema
- do not assume role template default data exists unless fetched
- do not modify backend execution-mode enum names

## API Mapping

- `name -> agent-edit-name-input`
- `role_name -> role input/select`
- `system_prompt -> prompt editor`
- `background_identity -> identity textarea`
- `background_experience -> experience textarea`
- `domain_knowledge -> knowledge textarea`
- `responsibility -> responsibility textarea`
- `constraints -> constraints textarea`
- `allow_tool_use -> toggle`
- `skill_ids -> selected skills`
- `tool_ids -> selected tools`
- `role_template_id -> role template select`
- `RoleTemplateResponse.execution_mode -> agent-edit-execution-mode`
- `default_code_policy.max_iterations -> agent-edit-policy-max-iterations`

## State Mapping

- loaded: identity panel and capability panel visible
- template selected: execution mode and policy panel update
- save success: visible success message
- policy state: `agent-policy-panel` visible only when template/policy data exists

## 5D Execution Targets

- D1: grouped panels and prompt area visible
- D2: save action triggers update and shows success
- D3: template selection updates execution mode field
- D4: policy panel and max iterations control visibility match template data
- D5: selecting a different template updates bound fields only through declared rules




