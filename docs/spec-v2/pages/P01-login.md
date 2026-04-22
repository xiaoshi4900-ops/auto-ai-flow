# P01 Login

## Route

- `/login`

## Goal

Authenticate the user and redirect to project list.

## Delegation Packet

- [P01-login.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P01-login.packet.md)

## Development Location

### Primary Docs

- [P01-login.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P01-login.md)
- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/auth.md)
- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/auth.md)
- [P01-login.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P01-login.packet.md)

### Frontend Code

- [LoginPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/auth/LoginPage.vue)
- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/api/auth.ts)
- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/auth.ts)
- [useLogin.ts](/C:/workspace/AutoAiFlow/frontend/src/composables/useLogin.ts)

### Tests

- [p01-login-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p01-login-5d.spec.ts)
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
## Read First

- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/apis/auth.md)
- [auth.md](/C:/workspace/AutoAiFlow/docs/spec-v2/backend/auth.md)
- [p01-login-5d.spec.ts](/C:/workspace/AutoAiFlow/frontend/tests/e2e/p01-login-5d.spec.ts)
- [LoginPage.vue](/C:/workspace/AutoAiFlow/frontend/src/pages/auth/LoginPage.vue)
- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/api/auth.ts)
- [auth.ts](/C:/workspace/AutoAiFlow/frontend/src/stores/auth.ts)

## Allowed Write Files

- `frontend/src/pages/auth/LoginPage.vue`
- `frontend/src/api/auth.ts`
- `frontend/src/stores/auth.ts`
- `frontend/src/composables/useLogin.ts`
- `frontend/tests/e2e/p01-login-5d.spec.ts`

## Forbidden

- do not modify backend files
- do not change auth route paths
- do not rename `username` to `email` in request payload
- do not touch non-login page tests

## API Mapping

- `username -> login username field`
- `password -> login password field`
- `access_token -> localStorage.access_token`
- `refresh_token -> localStorage.refresh_token`
- login failure message -> `login-message`

## State Mapping

- initial: form enabled, no error message
- submitting: `login-submit` disabled
- success: route becomes `/projects`
- failed: stay on `/login`, show `login-message`, re-enable submit

## 5D Execution Targets

- D1: `login-page`, `login-submit`, username input, password input visible
- D2: clicking `login-submit` issues `POST /api/v1/auth/login`
- D3: failed response message maps to `login-message`
- D4: disabled state during submit, restored after response
- D5: exactly one primary submit path; payload only contains `username` and `password`



