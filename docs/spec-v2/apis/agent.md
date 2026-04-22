# API Packet: Agent

## Development Location

### Spec Docs

- [agent.md](docs/spec-v2/apis/agent.md)
- [project-agent.md](docs/spec-v2/backend/project-agent.md)

### Backend Code

- [agents.py](backend/app/api/v1/agents.py)
- [agent.py](backend/app/schemas/agent.py)
- [skills.py](backend/app/api/v1/skills.py)
- [tools.py](backend/app/api/v1/tools.py)
- [role_templates.py](backend/app/api/v1/role_templates.py)
- [agent_service.py](backend/app/services/agent_service.py)

### Frontend Code

- [agent.ts](frontend/src/api/agent.ts)
- [roleTemplate.ts](frontend/src/api/roleTemplate.ts)
- [skill.ts](frontend/src/api/skill.ts)
- [tool.ts](frontend/src/api/tool.ts)
- [agent.ts](frontend/src/stores/agent.ts)
- [agent.ts](frontend/src/types/agent.ts)

### Tests

- [test_agent_schema.py](backend/tests/contract/test_agent_schema.py)
- [test_agent_api.py](backend/tests/integration/test_agent_api.py)
- [p04-agent-list-5d.spec.ts](frontend/tests/e2e/p04-agent-list-5d.spec.ts)
- [p05-agent-edit-5d.spec.ts](frontend/tests/e2e/p05-agent-edit-5d.spec.ts)
## Cross-page Entity Contract

- [agent.md](docs/spec-v2/entities/agent.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Actual Routes

- `GET /api/v1/agents?project_id={id}&page={n}&page_size={n}`
- `POST /api/v1/agents`
- `GET /api/v1/agents/{id}`
- `PUT /api/v1/agents/{id}`
- `DELETE /api/v1/agents/{id}`
- `POST /api/v1/agents/{id}/skills`
- `POST /api/v1/agents/{id}/tools`
- `POST /api/v1/projects/{project_id}/agents/from-template`
- `GET /api/v1/skills`
- `GET /api/v1/tools`
- `GET /api/v1/role-templates`
- `GET /api/v1/role-templates/{id}`

## Request Contracts

### `POST /api/v1/agents`

- `name: string`
- `project_id: number`
- `role_name?: string`
- `system_prompt?: string | null`
- `background_identity?: string | null`
- `background_experience?: string | null`
- `domain_knowledge?: string | null`
- `responsibility?: string | null`
- `constraints?: string | null`
- `model_id?: number | null`
- `allow_tool_use?: boolean`
- `skill_ids?: number[]`
- `tool_ids?: number[]`
- `role_template_id?: number | null`
- `description?: string | null`

### `PUT /api/v1/agents/{id}`

- `name?: string`
- `role_name?: string`
- `system_prompt?: string | null`
- `background_identity?: string | null`
- `background_experience?: string | null`
- `domain_knowledge?: string | null`
- `responsibility?: string | null`
- `constraints?: string | null`
- `model_id?: number | null`
- `allow_tool_use?: boolean`
- `role_template_id?: number | null`

## Response Contracts

- `AgentResponse.id`
- `AgentResponse.project_id`
- `AgentResponse.name`
- `AgentResponse.role_name`
- `AgentResponse.system_prompt`
- `AgentResponse.background_identity`
- `AgentResponse.background_experience`
- `AgentResponse.domain_knowledge`
- `AgentResponse.responsibility`
- `AgentResponse.constraints`
- `AgentResponse.model_id`
- `AgentResponse.allow_tool_use`
- `AgentResponse.skill_ids`
- `AgentResponse.tool_ids`
- `AgentResponse.role_template_id`
- `AgentResponse.description`
- `AgentResponse.created_at`
- `AgentResponse.updated_at`

## Supporting Response Contracts

- `SkillResponse`: `id`, `name`, `skill_key`, `description`, `prompt_template`, `execution_mode`, `is_builtin`, `created_at`
- `ToolResponse`: `id`, `name`, `description`, `tool_type`, `config`, `is_builtin`, `created_at`
- `RoleTemplateListItem`: `id`, `key`, `name`, `execution_mode`
- `RoleTemplateResponse`: `id`, `key`, `name`, `category`, `description`, `execution_mode`, `default_role_name`, `default_model_id`, `default_skill_ids`, `default_tool_ids`, `default_code_policy`, `is_builtin`, `enabled`

## Frontend View-Model Extensions

The frontend agent type currently allows:

- `model_name?: string`

This is not part of backend `AgentResponse`. Resolve it from related model data or add it explicitly in backend schema.

## Consumers

- `P04`
- `P05`


