# Entity Contract: Workflow

## API-native Fields

- `id`
- `project_id`
- `name`
- `description`
- `nodes`
- `edges`
- `canvas_data`
- `created_at`
- `updated_at`

## Derived Fields

### `node_count`

- source: `nodes.length`
- owner: frontend adapter or store
- fallback: `0` when `nodes` missing or empty
- consumers: `P07`

### `updated_relative`

- source: `updated_at`
- owner: frontend adapter or store
- fallback: hide relative text when unavailable
- consumers: `P07`

### `status`

- source: not present in workflow schema
- owner: only via explicit external rule or related runtime data
- fallback: hide status badge instead of inventing a value
- consumers: `P07`, `P08`

### `version`

- source: not present in workflow schema
- owner: explicit adapter only if another backend source exists
- fallback: hide version label
- consumers: `P07`

## Cross-page Consistency Rules

1. `nodes` and `edges` semantics must match between list summaries and editor load/save.
2. Save payload must preserve schema names exactly.
3. Any derived `status` or `version` must be consistently labeled as derived across pages.

## Consumer Pages

- `P07`
- `P08`
