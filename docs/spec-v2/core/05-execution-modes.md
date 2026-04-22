# Execution Modes

## Purpose

Tell external AI what to do first and what not to do first.

## Global Rule

Do not start from tests unless the packet explicitly says the task is test-driven.

## Modes

### `refactor`

Use when the request is to restructure code, clean up logic, reduce duplication,
or improve maintainability without intentionally changing visible behavior.

#### First Action

1. Read the page packet or backend packet.
2. Read the listed code files.
3. Understand current behavior and file boundaries.

#### Do Not Start With

- running Playwright
- running the full backend test suite
- changing unrelated files

#### Test Policy

- tests are for post-change verification
- only run the tests listed in the current packet
- do not run full-suite regression unless explicitly requested

### `feature`

Use when the request adds new visible behavior or new backend capability.

#### First Action

1. Read the packet.
2. Freeze request and response contracts.
3. Identify target files.

#### Test Policy

- may write tests early
- do not start by running unrelated suites

### `bugfix`

Use when the request is to correct a broken behavior.

#### First Action

1. Read the packet.
2. Identify the smallest failing scope.
3. Reproduce using the narrowest relevant test or page path.

#### Test Policy

- only run the minimal related tests first
- do not start with full-suite execution

### `test-alignment`

Use when the request is explicitly to repair or align tests.

#### First Action

1. Read the packet.
2. Read the failing test file.
3. Compare test contract with implementation and schema.

#### Test Policy

- running the listed test first is allowed
- do not broaden scope unless contract mismatch is proven

## Default

If a packet does not explicitly say otherwise, treat the task as `refactor`.
