# Entity Contract: Agent

## API-native Fields

- `id`
- `project_id`
- `name`
- `role_name`
- `system_prompt`
- `background_identity`
- `background_experience`
- `domain_knowledge`
- `responsibility`
- `constraints`
- `model_id`
- `allow_tool_use`
- `skill_ids`
- `tool_ids`
- `role_template_id`
- `description`
- `created_at`
- `updated_at`

## Derived Fields

### `model_name`

- source: `model_id` + model lookup
- owner: frontend store or adapter
- fallback: hide model name when not resolvable
- consumers: `P04`, `P05`

### `execution_mode`

- source: role template detail, not `AgentResponse`
- owner: frontend adapter from role-template query
- fallback: show no execution-mode control until template data loads
- consumers: `P05`

### `policy defaults`

- source: `RoleTemplateResponse.default_code_policy`
- owner: frontend adapter/store
- fallback: policy panel hidden when absent
- consumers: `P05`

## Cross-page Consistency Rules

1. `name` and `role_name` must not drift between list card and edit form initial values.
2. `model_name` must always be treated as derived, never assumed from agent API.
3. Template-driven fields must update from role-template data, not from hardcoded page logic.

## Consumer Pages

- `P04`
- `P05`
