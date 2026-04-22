from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema, HandoffPayloadSchema
from app.db.models.run import WorkflowRun
from app.db.models.workflow import WorkflowNode
from app.runtime.agent_runner import AgentRunner
from app.runtime.normal_agent_runner import NormalAgentRunner
from app.runtime.code_skill_runner import CodeSkillRunner
from app.runtime.prompt_builder import PromptBuilder
from app.runtime.model_resolver import ModelResolver
from app.runtime.handoff_builder import HandoffBuilder
from app.runtime.execution_mode_resolver import resolve_execution_mode


class AgentNodeExecutor:
    def __init__(self):
        self.normal_runner = NormalAgentRunner()
        self.code_runner = CodeSkillRunner()
        self.prompt_builder = PromptBuilder()
        self.model_resolver = ModelResolver()
        self.handoff_builder = HandoffBuilder()

    def execute(self, workflow_run: WorkflowRun, workflow_node: WorkflowNode, runtime_context: RuntimeContextSchema) -> NodeExecutionResultSchema:
        config = workflow_node.config or {}
        agent_id = config.get("agent_id")
        task_instruction = config.get("task_instruction", "")
        input_mapping = config.get("input_mapping", {})
        model_override_id = config.get("model_override_id")
        retry_limit = config.get("retry_limit", 0)

        execution_mode = resolve_execution_mode(
            node_config=config,
            skill=None,
            role_template=None,
        )

        if execution_mode == "code_runtime":
            return self._execute_code_runtime(workflow_run, workflow_node, runtime_context, config)

        return self._execute_normal(workflow_run, workflow_node, runtime_context, config, agent_id, task_instruction, input_mapping, model_override_id, retry_limit)

    def _execute_normal(self, workflow_run, workflow_node, runtime_context, config, agent_id, task_instruction, input_mapping, model_override_id, retry_limit):
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

        prompt_result = self.prompt_builder.build(
            agent_id=agent_id,
            task_instruction=task_instruction,
            runtime_context=runtime_context,
            extra_input=mapped_input,
        )

        model_config = self.model_resolver.resolve(
            node_model_id=model_override_id,
            agent_id=agent_id,
            project_id=workflow_run.workflow.project_id if workflow_run.workflow else None,
        )

        last_error = None
        for attempt in range(retry_limit + 1):
            try:
                raw_output = self.normal_runner.run(prompt_result, model_config)
                structured_output = StructuredOutputSchema(status="success", structured_output=raw_output)
                handoff = self.handoff_builder.build(node_type="agent", raw_output=raw_output, structured_output=raw_output)
                return NodeExecutionResultSchema(
                    node_key=workflow_node.node_key,
                    node_type=workflow_node.node_type,
                    status="success",
                    output=structured_output,
                    handoff=handoff,
                )
            except Exception as e:
                last_error = str(e)

        return NodeExecutionResultSchema(
            node_key=workflow_node.node_key,
            node_type=workflow_node.node_type,
            status="failed",
            output=StructuredOutputSchema(status="failed"),
            handoff=HandoffPayloadSchema(),
            error_message=last_error or "Agent execution failed",
        )

    def _execute_code_runtime(self, workflow_run, workflow_node, runtime_context, config):
        max_iterations = 3
        code_policy = config.get("code_policy_override", {})
        if code_policy and isinstance(code_policy, dict):
            max_iterations = code_policy.get("max_iterations", 3)

        context_dict = {}
        if runtime_context and hasattr(runtime_context, "model_dump"):
            context_dict = runtime_context.model_dump()
        elif runtime_context and hasattr(runtime_context, "__dict__"):
            context_dict = {k: v for k, v in runtime_context.__dict__.items() if not k.startswith("_")}

        result = self.code_runner.run(
            workflow_run=workflow_run,
            workflow_node=workflow_node,
            runtime_context=context_dict,
            max_iterations=max_iterations,
        )

        code_handoff = result.get("code_handoff", {})
        structured_output = StructuredOutputSchema(
            status=result.get("status", "success"),
            structured_output=result,
        )
        handoff = self.handoff_builder.build(
            node_type="agent",
            raw_output=result,
            structured_output=result,
        )

        return NodeExecutionResultSchema(
            node_key=workflow_node.node_key,
            node_type=workflow_node.node_type,
            status=result.get("status", "success"),
            output=structured_output,
            handoff=handoff,
        )
