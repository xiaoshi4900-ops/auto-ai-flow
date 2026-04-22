from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema, HandoffPayloadSchema
from app.db.models.run import WorkflowRun
from app.db.models.workflow import WorkflowNode
from app.runtime.tool_runner import ToolRunner


class ToolNodeExecutor:
    def __init__(self):
        self.tool_runner = ToolRunner()

    def execute(self, workflow_run: WorkflowRun, workflow_node: WorkflowNode, runtime_context: RuntimeContextSchema) -> NodeExecutionResultSchema:
        config = workflow_node.config or {}
        tool_id = config.get("tool_id")
        input_mapping = config.get("input_mapping", {})
        retry_limit = config.get("retry_limit", 0)

        mapped_input = {}
        for target_key, source_path in input_mapping.items():
            parts = source_path.split(".")
            value = runtime_context.node_outputs
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    value = None
                    break
            if value is not None:
                mapped_input[target_key] = value

        last_error = None
        for attempt in range(retry_limit + 1):
            try:
                result = self.tool_runner.run(tool_id=tool_id, inputs=mapped_input)
                return NodeExecutionResultSchema(
                    node_key=workflow_node.node_key,
                    node_type=workflow_node.node_type,
                    status="success",
                    output=StructuredOutputSchema(status="success", structured_output=result),
                    handoff=HandoffPayloadSchema(handoff_summary="Tool executed successfully"),
                )
            except Exception as e:
                last_error = str(e)

        return NodeExecutionResultSchema(
            node_key=workflow_node.node_key,
            node_type=workflow_node.node_type,
            status="failed",
            output=StructuredOutputSchema(status="failed"),
            handoff=HandoffPayloadSchema(),
            error_message=last_error or "Tool execution failed",
        )
