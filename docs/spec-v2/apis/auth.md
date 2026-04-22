# API Packet: Auth

## Development Location

### Spec Docs

- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/auth.md)
- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/auth.md)

### Backend Code

- [auth.py](/C:/workspace/AutoAiFlow/backend/app/api/v1/auth.py)
- [auth.py](/C:/workspace/AutoAiFlow/backend/app/schemas/auth.py)
- [auth_service.py](/C:/workspace/AutoAiFlow/backend/app/services/auth_service.py)

### Frontend Code

- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/api/auth.ts)
- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/auth.ts)
- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/types/auth.ts)

### Tests

- [test_auth_schema.py](/C:/workspace/AutoAiFlow/backend/tests/contract/test_auth_schema.py)
- [test_auth_api.py](/C:/workspace/AutoAiFlow/backend/tests/integration/test_auth_api.py)
- [p01-login-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p01-login-5d.spec.ts)
## Actual Routes

- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

## Request Contracts

### `POST /api/v1/auth/login`

- `username: string`
- `password: string`

### `POST /api/v1/auth/refresh`

- `refresh_token: string`

## Response Contracts

### `TokenPairResponse`

- `access_token`
- `refresh_token`
- `token_type`

### `CurrentUserResponse`

- `id`
- `username`
- `email`
- `display_name`
- `is_active`

## Consumers

- `P01`

