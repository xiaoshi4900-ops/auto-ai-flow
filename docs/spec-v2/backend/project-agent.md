# Backend Packet: Project And Agent

## Development Location

### Spec Docs

- [project-agent.md](docs/spec-v2/backend/project-agent.md)
- [project.md](docs/spec-v2/apis/project.md)
- [agent.md](docs/spec-v2/apis/agent.md)
- [model.md](docs/spec-v2/apis/model.md)

### Backend Code

- [projects.py](backend/app/api/v1/projects.py)
- [agents.py](backend/app/api/v1/agents.py)
- [models.py](backend/app/api/v1/models.py)
- [project.py](backend/app/schemas/project.py)
- [agent.py](backend/app/schemas/agent.py)
- [model.py](backend/app/schemas/model.py)
- [project_service.py](backend/app/services/project_service.py)
- [agent_service.py](backend/app/services/agent_service.py)
- [model_service.py](backend/app/services/model_service.py)

### Tests

- [test_project_schema.py](backend/tests/contract/test_project_schema.py)
- [test_agent_schema.py](backend/tests/contract/test_agent_schema.py)
- [test_model_schema.py](backend/tests/contract/test_model_schema.py)
- [test_project_api.py](backend/tests/integration/test_project_api.py)
- [test_agent_api.py](backend/tests/integration/test_agent_api.py)
## Logic Tree

1. project CRUD and ownership
2. agent CRUD and project association
3. template-based agent creation
4. skill, tool, model, and role-template binding support
5. model config persistence for project-scoped defaults

## Test Tree

1. contract:
   - [test_project_schema.py](backend/tests/contract/test_project_schema.py)
   - [test_agent_schema.py](backend/tests/contract/test_agent_schema.py)
   - [test_agent_schema_v11.py](backend/tests/contract/test_agent_schema_v11.py)
   - [test_model_schema.py](backend/tests/contract/test_model_schema.py)
2. integration:
   - [test_project_api.py](backend/tests/integration/test_project_api.py)
   - [test_agent_api.py](backend/tests/integration/test_agent_api.py)
   - [test_agent_from_template_api.py](backend/tests/integration/test_agent_from_template_api.py)
   - [test_role_template_api.py](backend/tests/integration/test_role_template_api.py)

## API Files

- [projects.py](backend/app/api/v1/projects.py)
- [agents.py](backend/app/api/v1/agents.py)
- [models.py](backend/app/api/v1/models.py)

## Service Files

- [project_service.py](backend/app/services/project_service.py)
- [agent_service.py](backend/app/services/agent_service.py)
- [model_service.py](backend/app/services/model_service.py)

## Dependent Pages

- `P02`
- `P03`
- `P04`
- `P05`
- `P06`

