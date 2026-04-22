from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema, HandoffPayloadSchema
from app.db.models.run import WorkflowRun
from app.db.models.workflow import WorkflowNode


class OutputNodeExecutor:
    def execute(self, workflow_run: WorkflowRun, workflow_node: WorkflowNode, runtime_context: RuntimeContextSchema) -> NodeExecutionResultSchema:
        config = workflow_node.config or {}
        source_keys = config.get("source_keys", [])
        output_format = config.get("output_format", "raw")

        final_output = {}
        for key in source_keys:
            if key in runtime_context.node_outputs:
                final_output[key] = runtime_context.node_outputs[key]
            elif key in runtime_context.shared_state:
                final_output[key] = runtime_context.shared_state[key]

        if not source_keys:
            final_output = runtime_context.node_outputs

        return NodeExecutionResultSchema(
            node_key=workflow_node.node_key,
            node_type=workflow_node.node_type,
            status="success",
            output=StructuredOutputSchema(status="success", structured_output=final_output),
            handoff=HandoffPayloadSchema(handoff_summary="Output node aggregated results"),
        )
