# Entity Contract: Project

## API-native Fields

- `id`
- `name`
- `description`
- `owner_id`
- `default_model_id`
- `created_at`
- `updated_at`

## Derived Fields

### `updated_relative`

- source: `updated_at`
- owner: frontend store or api adapter
- fallback: if `updated_at` is null, render no relative text
- consumers: `P02`, `P03`

### `status`

- source: not present in backend project schema
- owner: only allowed if an explicit frontend rule exists
- fallback: hide status chip instead of inventing a value
- consumers: `P02`, `P03`

### `default_model_name`

- source: `default_model_id` + model lookup
- owner: frontend store or adapter
- fallback: hide model label when model cannot be resolved
- consumers: `P03`

## Cross-page Consistency Rules

1. `name` text must use the same canonical project name in list and detail.
2. `updated_relative` formatting must be shared across list and detail.
3. `status` cannot appear on one page as API-native and on another as derived.
4. Missing `default_model_id` must produce the same no-model fallback across pages.

## Consumer Pages

- `P02`
- `P03`
