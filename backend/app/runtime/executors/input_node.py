from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema, HandoffPayloadSchema
from app.db.models.run import WorkflowRun
from app.db.models.workflow import WorkflowNode


class InputNodeExecutor:
    def execute(self, workflow_run: WorkflowRun, workflow_node: WorkflowNode, runtime_context: RuntimeContextSchema) -> NodeExecutionResultSchema:
        input_payload = workflow_run.input_payload or {}
        config = workflow_node.config or {}
        input_mapping = config.get("input_mapping", {})
        mapped_input = {}
        for target_key, source_key in input_mapping.items():
            if source_key in input_payload:
                mapped_input[target_key] = input_payload[source_key]
        if not mapped_input:
            mapped_input = input_payload
        return NodeExecutionResultSchema(
            node_key=workflow_node.node_key,
            node_type=workflow_node.node_type,
            status="success",
            output=StructuredOutputSchema(status="success", structured_output=mapped_input),
            handoff=HandoffPayloadSchema(handoff_summary="Input node processed"),
        )
