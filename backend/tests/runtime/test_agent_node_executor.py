from unittest.mock import MagicMock, patch
from app.runtime.executors.agent_node import AgentNodeExecutor
from app.schemas.runtime import RuntimeContextSchema


def _make_workflow_node():
    node = MagicMock()
    node.node_key = "agent_1"
    node.node_type = "agent"
    node.config = {"agent_id": 1, "task_instruction": "Summarize", "input_mapping": {}, "retry_limit": 0}
    return node


def _make_workflow_run():
    run = MagicMock()
    run.input_payload = {"topic": "AI"}
    run.workflow = MagicMock()
    run.workflow.project_id = 1
    return run


def test_agent_node_success():
    executor = AgentNodeExecutor()
    with patch.object(executor.normal_runner, "run", return_value={"result": "Summary text"}):
        with patch.object(executor.model_resolver, "resolve", return_value={"model_id": "gpt-4"}):
            with patch.object(executor.prompt_builder, "build", return_value=MagicMock()):
                result = executor.execute(_make_workflow_run(), _make_workflow_node(), RuntimeContextSchema())
    assert result.status == "success"
    assert result.node_key == "agent_1"


def test_agent_node_failure():
    executor = AgentNodeExecutor()
    with patch.object(executor.normal_runner, "run", side_effect=Exception("LLM error")):
        with patch.object(executor.model_resolver, "resolve", return_value=None):
            with patch.object(executor.prompt_builder, "build", return_value=MagicMock()):
                result = executor.execute(_make_workflow_run(), _make_workflow_node(), RuntimeContextSchema())
    assert result.status == "failed"
    assert "LLM error" in result.error_message


def test_agent_node_retry():
    executor = AgentNodeExecutor()
    node = _make_workflow_node()
    node.config["retry_limit"] = 2
    call_count = 0

    def mock_run(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            raise Exception("Transient error")
        return {"result": "Success after retry"}

    with patch.object(executor.normal_runner, "run", side_effect=mock_run):
        with patch.object(executor.model_resolver, "resolve", return_value=None):
            with patch.object(executor.prompt_builder, "build", return_value=MagicMock()):
                result = executor.execute(_make_workflow_run(), node, RuntimeContextSchema())
    assert result.status == "success"
    assert call_count == 3
