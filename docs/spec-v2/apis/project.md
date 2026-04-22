# API Packet: Project

## Development Location

### Spec Docs

- [project.md](docs/spec-v2/apis/project.md)
- [project-agent.md](docs/spec-v2/backend/project-agent.md)

### Backend Code

- [projects.py](backend/app/api/v1/projects.py)
- [project.py](backend/app/schemas/project.py)
- [project_service.py](backend/app/services/project_service.py)

### Frontend Code

- [project.ts](frontend/src/api/project.ts)
- [project.ts](frontend/src/stores/project.ts)
- [project.ts](frontend/src/types/project.ts)

### Tests

- [test_project_schema.py](backend/tests/contract/test_project_schema.py)
- [test_project_api.py](backend/tests/integration/test_project_api.py)
- [p02-project-list-5d.spec.ts](frontend/tests/e2e/p02-project-list-5d.spec.ts)
- [p03-project-detail-5d.spec.ts](frontend/tests/e2e/p03-project-detail-5d.spec.ts)
## Cross-page Entity Contract

- [project.md](docs/spec-v2/entities/project.md)
- [06-mapping-ownership.md](docs/spec-v2/core/06-mapping-ownership.md)

## Actual Routes

- `GET /api/v1/projects`
- `POST /api/v1/projects`
- `GET /api/v1/projects/{id}`
- `PUT /api/v1/projects/{id}`
- `DELETE /api/v1/projects/{id}`

## Request Contracts

### `POST /api/v1/projects`

- `name: string`
- `description?: string | null`
- `default_model_id?: number | null`

### `PUT /api/v1/projects/{id}`

- `name?: string`
- `description?: string | null`
- `default_model_id?: number | null`

## Response Contracts

### `ProjectResponse`

- `id: number`
- `name: string`
- `description: string | null`
- `owner_id: number`
- `default_model_id: number | null`
- `created_at: datetime | null`
- `updated_at: datetime | null`

### `ProjectListResponse`

- `total: number`
- `items: ProjectResponse[]`

## Frontend View-Model Extensions

The frontend type currently allows these derived fields, but backend schema does not expose them:

- `status?: string`
- `updated_relative?: string`
- `default_model_name?: string`

If used by UI, they must be derived locally or added through an explicit backend contract change.

## Consumers

- `P02`
- `P03`

## Contract Gaps To Respect

1. There is no actual route `GET /api/v1/projects/{project_id}/workflows` in the current backend router.
2. There is no actual route `GET /api/v1/projects/{project_id}/runs` in the current backend router.
3. Project detail pages must currently compose related data from other global resource endpoints or wait for backend extension.


