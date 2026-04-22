# Mapping Ownership Rule

## Purpose

Freeze where request mapping, response mapping, derived-field mapping, and save-payload mapping are allowed to live.

## Rule Summary

1. Backend schema defines API-native fields.
2. Frontend API or store layer may build a view-model adapter.
3. Page components consume view-model fields and emit UI events.
4. Save payload mapping must happen once in a store or dedicated mapper, not ad hoc in multiple components.

## Allowed Ownership

### API-native Field Definition

Owner:

- backend schema
- backend router response contract

Examples:

- `ProjectResponse.updated_at`
- `AgentResponse.role_template_id`
- `WorkflowResponse.nodes`
- `RunDetailResponse.node_runs`

### Derived View-model Field

Owner:

- frontend `api/` adapter layer, or
- frontend `stores/` layer, or
- dedicated mapper module if introduced later

Not allowed in:

- page template
- scattered component computed fields across multiple files

Examples:

- `updated_relative`
- `model_name`
- optional `latency_ms` display fallback

### Save Payload Mapping

Owner:

- one store action, or
- one dedicated mapper

Not allowed in:

- multiple page sections
- child component plus page plus store at the same time

Examples:

- `WorkflowUpdateRequest`
- `AgentUpdateRequest`
- `ProjectCreateRequest`

## Forbidden Patterns

1. Page component remaps backend fields directly into multiple UI-specific aliases.
2. The same derived field is computed in more than one page.
3. Save payload is assembled separately in page, child component, and store.
4. Tests rely on a derived field that is not declared in entity contracts.

## Required Documentation

When a page uses a derived field, the page or entity contract must state:

1. field name
2. source field(s)
3. mapping owner
4. fallback rule
5. consumer pages
