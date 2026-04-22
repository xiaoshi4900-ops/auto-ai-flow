# API Packet: Model

## Development Location

### Spec Docs

- [model.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/model.md)
- [project-agent.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/project-agent.md)

### Backend Code

- [models.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/models.py)
- [model.py](/C:/workspace/AutoAiFlow/backend/app/schemas/model.py)
- [model_service.py](/C:/workspace/AutoAiFlow/backend/app/services/model_service.py)

### Frontend Code

- [model.ts](/C:/workspace/AutoAiFlow/frontend/src/api/model.ts)
- [model.ts](/C:/workspace/AutoAiFlow/frontend/src/types/model.ts)

### Tests

- [test_model_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_model_schema.py)
- [p05-agent-edit-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p05-agent-edit-5d.spec.ts)
- [p06-model-config-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p06-model-config-5d.spec.ts)
## Actual Routes

- `GET /api/v1/models`
- `POST /api/v1/models/project/{project_id}/configs`
- `GET /api/v1/models/project/{project_id}/configs`

## Request Contracts

### `POST /api/v1/models/project/{project_id}/configs`

- `model_definition_id: number`
- `api_key?: string | null`
- `custom_config?: object | null`
- `is_default?: boolean`

## Response Contracts

- `ModelProviderResponse`: `id`, `name`, `provider_type`, `api_base`, `is_builtin`
- `ModelDefinitionResponse`: `id`, `provider_id`, `name`, `model_id`, `description`, `capabilities`, `is_builtin`
- `ProjectModelConfigResponse`: `id`, `project_id`, `model_definition_id`, `is_default`, `created_at`

## Contract Gap To Respect

The current frontend model types use different field names than backend schema:

- frontend provider: `api_base_url`, `is_active`
- backend provider: `api_base`, `is_builtin`
- frontend model: `model_name`, `display_name`, `model_type`, `context_window`, `is_active`
- backend model: `name`, `model_id`, `description`, `capabilities`, `is_builtin`

Do not silently remap these in implementation without updating spec, types, and tests together.

## Consumers

- `P05`
- `P06`

