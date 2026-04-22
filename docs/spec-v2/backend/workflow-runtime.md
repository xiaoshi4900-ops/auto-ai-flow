# Backend Packet: Workflow And Runtime

## Development Location

### Spec Docs

- [workflow-runtime.md](docs/spec-v2/backend/workflow-runtime.md)
- [workflow.md](docs/spec-v2/apis/workflow.md)
- [run-execution.md](docs/spec-v2/apis/run-execution.md)

### Backend Code

- [workflows.py](backend/app/api/v1/workflows.py)
- [executions.py](backend/app/api/v1/executions.py)
- [code_runtime.py](backend/app/api/v1/code_runtime.py)
- [workflow.py](backend/app/schemas/workflow.py)
- [execution.py](backend/app/schemas/execution.py)
- [runtime.py](backend/app/schemas/runtime.py)
- [workflow_service.py](backend/app/services/workflow_service.py)
- [execution_service.py](backend/app/services/execution_service.py)
- [code_runtime_service.py](backend/app/services/code_runtime_service.py)

### Tests

- [test_workflow_schema.py](backend/tests/contract/test_workflow_schema.py)
- [test_execution_schema.py](backend/tests/contract/test_execution_schema.py)
- [test_runtime_schema.py](backend/tests/contract/test_runtime_schema.py)
- [test_workflow_api.py](backend/tests/integration/test_workflow_api.py)
- [test_code_runtime_api.py](backend/tests/integration/test_code_runtime_api.py)
## Logic Tree

1. workflow schema and topology validation
2. workflow CRUD
3. runtime context contract
4. node execution contract
5. workflow execution trigger
6. code-runtime and execution-mode extensions

## Test Tree

1. contract:
   - [test_workflow_schema.py](backend/tests/contract/test_workflow_schema.py)
   - [test_workflow_schema_v11.py](backend/tests/contract/test_workflow_schema_v11.py)
   - [test_execution_schema.py](backend/tests/contract/test_execution_schema.py)
   - [test_runtime_schema.py](backend/tests/contract/test_runtime_schema.py)
   - [test_code_runtime_schema.py](backend/tests/contract/test_code_runtime_schema.py)
2. integration:
   - [test_workflow_api.py](backend/tests/integration/test_workflow_api.py)
   - [test_code_runtime_api.py](backend/tests/integration/test_code_runtime_api.py)
   - [test_v11_integration.py](backend/tests/integration/test_v11_integration.py)

## API Files

- [workflows.py](backend/app/api/v1/workflows.py)
- [executions.py](backend/app/api/v1/executions.py)
- [code_runtime.py](backend/app/api/v1/code_runtime.py)

## Service Files

- [workflow_service.py](backend/app/services/workflow_service.py)
- [execution_service.py](backend/app/services/execution_service.py)
- [code_runtime_service.py](backend/app/services/code_runtime_service.py)

## Dependent Pages

- `P07`
- `P08`
- `P10`

