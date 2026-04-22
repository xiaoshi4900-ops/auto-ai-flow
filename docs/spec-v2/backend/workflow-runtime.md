# Backend Packet: Workflow And Runtime

## Development Location

### Spec Docs

- [workflow-runtime.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/workflow-runtime.md)
- [workflow.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/workflow.md)
- [run-execution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/run-execution.md)

### Backend Code

- [workflows.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/workflows.py)
- [executions.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/executions.py)
- [code_runtime.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/code_runtime.py)
- [workflow.py](/C:/workspace/AutoAiFlow/backend/app/schemas/workflow.py)
- [execution.py](/C:/workspace/AutoAiFlow/backend/app/schemas/execution.py)
- [runtime.py](/C:/workspace/AutoAiFlow/backend/app/schemas/runtime.py)
- [workflow_service.py](/C:/workspace/AutoAiFlow/backend/app/services/workflow_service.py)
- [execution_service.py](/C:/workspace/AutoAiFlow/backend/app/services/execution_service.py)
- [code_runtime_service.py](/C:/workspace/AutoAiFlow/backend/app/services/code_runtime_service.py)

### Tests

- [test_workflow_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_workflow_schema.py)
- [test_execution_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_execution_schema.py)
- [test_runtime_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_runtime_schema.py)
- [test_workflow_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_workflow_api.py)
- [test_code_runtime_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_code_runtime_api.py)
## Logic Tree

1. workflow schema and topology validation
2. workflow CRUD
3. runtime context contract
4. node execution contract
5. workflow execution trigger
6. code-runtime and execution-mode extensions

## Test Tree

1. contract:
   - [test_workflow_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_workflow_schema.py)
   - [test_workflow_schema_v11.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_workflow_schema_v11.py)
   - [test_execution_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_execution_schema.py)
   - [test_runtime_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_runtime_schema.py)
   - [test_code_runtime_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_code_runtime_schema.py)
2. integration:
   - [test_workflow_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_workflow_api.py)
   - [test_code_runtime_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_code_runtime_api.py)
   - [test_v11_integration.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_v11_integration.py)

## API Files

- [workflows.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/workflows.py)
- [executions.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/executions.py)
- [code_runtime.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/code_runtime.py)

## Service Files

- [workflow_service.py](/C:/workspace/AutoAiFlow/backend/app/services/workflow_service.py)
- [execution_service.py](/C:/workspace/AutoAiFlow/backend/app/services/execution_service.py)
- [code_runtime_service.py](/C:/workspace/AutoAiFlow/backend/app/services/code_runtime_service.py)

## Dependent Pages

- `P07`
- `P08`
- `P10`

