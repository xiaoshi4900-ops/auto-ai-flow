# P04 Agent List

## Source Of Truth

- Spec packet: [P04-agent-list.md](docs/spec-v2/pages/P04-agent-list.md)
- Rules root: [docs/spec-v2/README.md](docs/spec-v2/README.md)

## Recommended Read Order

1. spec-v2 root if needed
2. linked page packet
3. linked API/backend docs from that page packet
4. this task packet

## Primary Packet

- [P04-agent-list.md](docs/spec-v2/pages/P04-agent-list.md)

## Task Mode

- `refactor`

## First Action

1. Read the linked page packet first.
2. Read the files listed in that page packet.
3. Do not run tests before code inspection.

## Do Not Start With

- `npm exec playwright test`
- full Playwright runs
- full backend test runs
- broad repo refactors

## Test Policy

- tests are verification only unless the user explicitly asks for test alignment
- only run the page-level E2E file listed in the linked page packet
- do not run unrelated suites
## Scope

Execute exactly one page packet. Do not expand scope beyond the linked page packet.

Target dimensions: D1,D2,D3,D4,D5

## Restrictions

1. Read only the files listed in the linked page packet.
2. Change only files listed in the linked page packet.
3. Do not rename route paths, request fields, or response fields unless the page packet explicitly allows it.
4. If the linked page packet says a field is derived, keep it derived or document a backend contract change.
5. If you find a contract mismatch, stop broad refactoring and report it.

## Return Format

```json
{
  "task_id": "P04 Agent List",
  "files_read": [],
  "files_changed": [],
  "dimensions_completed": ["D1", "D2", "D3", "D4", "D5"],
  "tests_run": [],
  "contract_gaps_found": [],
  "notes": []
}
```



