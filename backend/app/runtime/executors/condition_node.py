from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema, HandoffPayloadSchema
from app.db.models.run import WorkflowRun
from app.db.models.workflow import WorkflowNode
from app.runtime.condition_evaluator import ConditionEvaluator


class ConditionNodeExecutor:
    def __init__(self):
        self.evaluator = ConditionEvaluator()

    def execute(self, workflow_run: WorkflowRun, workflow_node: WorkflowNode, runtime_context: RuntimeContextSchema) -> NodeExecutionResultSchema:
        config = workflow_node.config or {}
        branches = config.get("branches", [])
        default_target = config.get("default_target_key", "")

        matched_target = default_target
        for branch in branches:
            result = self.evaluator.evaluate(branch, runtime_context)
            if result:
                matched_target = branch.get("target_node_key", default_target)
                break

        return NodeExecutionResultSchema(
            node_key=workflow_node.node_key,
            node_type=workflow_node.node_type,
            status="success",
            output=StructuredOutputSchema(status="success", structured_output={"matched_branch": matched_target}),
            handoff=HandoffPayloadSchema(handoff_summary=f"Condition evaluated, next: {matched_target}"),
            next_node_key=matched_target,
        )
