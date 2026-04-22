# Task Packets

These files are the delegation layer for external AI executors.

## Guardrail Files

- [EXECUTION-CHECKLIST.md](/C:/workspace/AutoAiFlow/docs/task-packets/EXECUTION-CHECKLIST.md)
- [RESULT.schema.json](/C:/workspace/AutoAiFlow/docs/task-packets/RESULT.schema.json)
- [enforce_task_packet.ps1](/C:/workspace/AutoAiFlow/scripts/enforce_task_packet.ps1)

## Relationship To Spec

- `docs/spec-v2/` is the source of truth.
- `docs/task-packets/` is the delivery layer.
- Every task packet must point to exactly one primary page packet.
- If a task packet conflicts with a page packet, the page packet wins.

## Delegation Rule

Give the executor exactly one packet at a time.

## Recommended Delegation Order

1. open the linked page packet
2. read only the files listed there
3. execute within the write boundary
4. return using the task packet JSON format
5. run `enforce_task_packet.ps1` before accepting the result

## Page Task Index

- [P01-login.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P01-login.packet.md) <- [P01-login.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P01-login.md)
- [P02-project-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P02-project-list.packet.md) <- [P02-project-list.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P02-project-list.md)
- [P03-project-detail.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P03-project-detail.packet.md) <- [P03-project-detail.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P03-project-detail.md)
- [P04-agent-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P04-agent-list.packet.md) <- [P04-agent-list.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P04-agent-list.md)
- [P05-agent-edit.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P05-agent-edit.packet.md) <- [P05-agent-edit.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P05-agent-edit.md)
- [P06-model-config.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P06-model-config.packet.md) <- [P06-model-config.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P06-model-config.md)
- [P07-workflow-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P07-workflow-list.packet.md) <- [P07-workflow-list.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P07-workflow-list.md)
- [P08-workflow-editor.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P08-workflow-editor.packet.md) <- [P08-workflow-editor.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P08-workflow-editor.md)
- [P09-run-list.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P09-run-list.packet.md) <- [P09-run-list.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P09-run-list.md)
- [P10-run-detail.packet.md](/C:/workspace/AutoAiFlow/docs/task-packets/P10-run-detail.packet.md) <- [P10-run-detail.md](/C:/workspace/AutoAiFlow/docs/spec-v2/pages/P10-run-detail.md)
