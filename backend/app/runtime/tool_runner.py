class ToolRunner:
    def run(self, tool_id: int | None = None, inputs: dict | None = None) -> dict:
        return {"tool_id": tool_id, "result": "Tool execution stub", "inputs": inputs or {}}
