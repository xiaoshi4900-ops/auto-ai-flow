# Backend Packet: Auth

## Development Location

### Spec Docs

- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/auth.md)
- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/auth.md)

### Backend Code

- [auth.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/auth.py)
- [auth.py](/C:/workspace/AutoAiFlow/backend/app/schemas/auth.py)
- [auth_service.py](/C:/workspace/AutoAiFlow/backend/app/services/auth_service.py)

### Tests

- [test_auth_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_auth_schema.py)
- [test_auth_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_auth_api.py)
## Logic Tree

1. user and refresh token model
2. auth schema contract
3. login and token issue flow
4. current user lookup
5. auth error handling

## Test Tree

1. contract:
   - [test_auth_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_auth_schema.py)
2. integration:
   - [test_auth_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_auth_api.py)

## API Files

- [auth.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/auth.py)
- [auth.py](/C:/workspace/AutoAiFlow/backend/app/schemas/auth.py)
- [auth_service.py](/C:/workspace/AutoAiFlow/backend/app/services/auth_service.py)

## Dependent Pages

- `P01`

