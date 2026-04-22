# Entity Contract: Run

## API-native Fields

### Run core

- `id`
- `workflow_id`
- `status`
- `input_payload`
- `output_payload`
- `error_message`
- `started_at`
- `finished_at`
- `created_at`

### Node run core

- `id`
- `workflow_run_id`
- `node_key`
- `node_type`
- `status`
- `input_data`
- `output_data`
- `error_message`
- `started_at`
- `finished_at`
- `duration_ms`

## Derived Or Optional Enriched Fields

### `latency_ms`

- source: optional enrichment or derived from timestamps
- owner: frontend adapter or explicit backend extension
- fallback: hide metric when absent
- consumers: `P09`, `P10`

### `token_usage_total`

- source: optional enrichment only
- owner: explicit backend extension or adapter from richer payload
- fallback: hide metric when absent
- consumers: `P09`, `P10`

### `structured_output`

- source: optional richer runtime data
- owner: backend extension or adapter from `output_payload`
- fallback: show standard output viewer using available payload only
- consumers: `P10`

### `handoff`

- source: optional richer runtime data
- owner: backend extension or adapter from structured payload
- fallback: hide handoff panel if absent
- consumers: `P10`

## Cross-page Consistency Rules

1. `status` labels and colors must match between list and detail.
2. Optional metrics must use the same hide-vs-placeholder rule in list and detail.
3. Timeline data must always come from `node_runs`, not from free-form logs.
4. `structured_output` and `handoff` must stay separate from generic logs.

## Consumer Pages

- `P08`
- `P09`
- `P10`
