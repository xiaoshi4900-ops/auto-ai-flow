# Execution Checklist

Use this checklist before and after each delegated AI run.

## Before Execution

1. Confirm one packet only for this run.
2. Open linked page packet from `## Primary Packet`.
3. Read `Development Location` in the linked page packet.
4. Confirm `Task Mode`, `First Action`, `Test Policy`, and `Do Not Start With`.
5. Confirm write scope from `Allowed Write Files`.

## During Execution

1. Do not edit files outside `Allowed Write Files`.
2. Do not start with broad tests.
3. Keep mapping ownership rules:
4. API-native fields are owned by backend schema.
5. Derived fields are owned by frontend adapter/store.
6. Save payload mapping happens once in store or dedicated mapper.

## After Execution

1. Produce result JSON using [RESULT.schema.json](docs/task-packets/RESULT.schema.json).
2. Run guard script:

```powershell
powershell -ExecutionPolicy Bypass -File C:\workspace\AutoAiFlow\scripts\enforce_task_packet.ps1 `
  -PacketPath C:\workspace\AutoAiFlow\docs\task-packets\P08-workflow-editor.packet.md `
  -ResultPath C:\workspace\AutoAiFlow\tmp\p08-result.json
```

3. If guard fails, fix scope/tests first, then rerun.
