# Backend Packet: Run Query

## Development Location

### Spec Docs

- [run-query.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/run-query.md)
- [run-execution.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/run-execution.md)

### Backend Code

- [runs.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/runs.py)
- [execution.py](/C:/workspace/AutoAiFlow/backend/app/schemas/execution.py)
- [execution_service.py](/C:/workspace/AutoAiFlow/backend/app/services/execution_service.py)

### Tests

- [test_execution_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_execution_schema.py)
- [test_run_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_run_api.py)
- [test_code_runtime_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_code_runtime_api.py)
## Logic Tree

1. run list query
2. run detail query
3. node run detail projection
4. metrics projection
5. runtime detail enrichment

## Test Tree

1. contract:
   - [test_execution_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_execution_schema.py)
   - [test_runtime_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_runtime_schema.py)
2. integration:
   - [test_run_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_run_api.py)
   - [test_code_runtime_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_code_runtime_api.py)

## API Files

- [runs.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/runs.py)

## Service Files

- [execution_service.py](/C:/workspace/AutoAiFlow/backend/app/services/execution_service.py)

## Dependent Pages

- `P03`
- `P09`
- `P10`

