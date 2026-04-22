# Contract Resolution Rules

## Purpose

Freeze how external AI must handle mismatches between backend schema, frontend types,
and page-level tests.

## Priority Order

1. backend route path
2. backend schema field set
3. frontend page test selector and visible behavior
4. frontend view-model extension field

## Allowed View-Model Extension

A frontend page may compute derived fields such as:

- `updated_relative`
- `status` derived from another resource or fallback rule
- `model_name` resolved from related model data
- `token_usage_total` or `latency_ms` displayed only when present

These are view-model fields, not API contract fields, unless backend schema exposes them.

## Forbidden Behavior

1. Do not add backend response fields just because a page test uses them.
2. Do not rename backend fields to match a frontend preference without changing schema and tests together.
3. Do not hide a contract mismatch inside mock data.
4. Do not invent project-scoped paths when the router uses global resource paths.

## Required Documentation When A Gap Exists

Every page or API packet that depends on a view-model extension must explicitly say:

1. source API field
2. derived UI field
3. fallback behavior when source field is absent
