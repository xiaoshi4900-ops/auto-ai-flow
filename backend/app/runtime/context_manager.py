from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema


class ContextManager:
    def init_context(self, input_payload: dict) -> RuntimeContextSchema:
        return RuntimeContextSchema(input=input_payload)

    def merge_node_result(self, context: RuntimeContextSchema, node_key: str, result: NodeExecutionResultSchema) -> RuntimeContextSchema:
        context.node_outputs[node_key] = result.output.model_dump() if result.output else {}
        if result.handoff:
            context.shared_state[f"{node_key}_handoff"] = result.handoff.model_dump()
        if result.output and result.output.artifact_refs:
            context.artifacts[node_key] = result.output.artifact_refs
        context.meta[node_key] = {"status": result.status, "node_type": result.node_type}
        return context
