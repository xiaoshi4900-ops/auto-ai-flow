# Spec Loading Rules

## Goal

Prevent context bloat and AI memory loss during implementation.

## Default Rule

Never read the full spec set for a single task.

## Minimal Load Set

For one task, load only:

1. This file
2. One page packet
3. One API packet
4. One backend packet if the task touches backend logic

## When To Load More

Load one extra file only when blocked by one of these:

1. Missing request or response fields
2. Missing state definition
3. Missing test mapping
4. Missing dependency between page and backend capability

## Frontend Task Rule

Every frontend page task must be executed in 5D order:

1. style
2. click event
3. field mapping
4. state mapping
5. quantity and constraints

Do not merge these into one vague task like "finish page".

## API Rule

Do not infer request or response shape from UI code.

Use:

1. the API packet
2. backend schema file
3. contract tests

If the three disagree, the task is blocked until the contract is reconciled.

## Backend Rule

Backend implementation is complete only when its test tree is covered:

1. contract test
2. unit test
3. integration test
4. runtime test when execution flow is involved

## Handoff Rule

When finishing a task, hand off:

1. page id
2. 5D dimensions touched
3. API packet used
4. backend packet used
5. tests added or verified
6. known gaps
