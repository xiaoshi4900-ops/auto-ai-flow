from unittest.mock import MagicMock, patch

from app.runtime.executors.agent_node import AgentNodeExecutor
from app.schemas.runtime import RuntimeContextSchema


def _make_workflow_node(force_mode=None):
    node = MagicMock()
    node.node_key = "agent_1"
    node.node_type = "agent"
    node.config = {
        "agent_id": 1,
        "task_instruction": "Implement feature",
        "input_mapping": {},
        "retry_limit": 0,
    }
    if force_mode:
        node.config["force_execution_mode"] = force_mode
    return node


def _make_workflow_run():
    run = MagicMock()
    run.input_payload = {"task": "build API"}
    run.workflow = MagicMock()
    run.workflow.project_id = 1
    return run


def test_agent_node_routes_normal_mode_to_normal_runner():
    executor = AgentNodeExecutor()
    with patch("app.runtime.executors.agent_node.resolve_execution_mode", return_value="normal_llm"):
        mock_prompt = MagicMock()
        mock_model = {"model_id": "gpt-4"}
        executor.normal_runner.run = MagicMock(return_value={"result": "ok"})
        executor.prompt_builder.build = MagicMock(return_value=mock_prompt)
        executor.model_resolver.resolve = MagicMock(return_value=mock_model)

        result = executor.execute(_make_workflow_run(), _make_workflow_node(), RuntimeContextSchema())

    assert result.status == "success"
    executor.normal_runner.run.assert_called_once()


def test_agent_node_routes_code_runtime_to_code_skill_runner():
    executor = AgentNodeExecutor()
    with patch("app.runtime.executors.agent_node.resolve_execution_mode", return_value="code_runtime"):
        executor.code_runner.run = MagicMock(return_value={
            "status": "success",
            "plan_summary": "Plan",
            "iterations": [{"iteration_no": 1, "status": "completed", "changed_files": [], "artifact_refs": []}],
            "code_handoff": {"task_goal": "x", "changed_files": [], "validation_summary": {"lint": "passed"}, "open_issues": [], "next_actions": [], "artifact_refs": []},
            "recommend_human_review": False,
            "open_issues": [],
        })

        result = executor.execute(_make_workflow_run(), _make_workflow_node(force_mode="code_runtime"), RuntimeContextSchema())

    assert result.status == "success"
    executor.code_runner.run.assert_called_once()
