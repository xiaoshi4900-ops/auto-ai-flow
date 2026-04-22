from unittest.mock import MagicMock
from app.runtime.executors.start_node import StartNodeExecutor
from app.schemas.runtime import RuntimeContextSchema


def test_start_node_returns_success():
    executor = StartNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "start_1"
    workflow_node.node_type = "start"
    ctx = RuntimeContextSchema(input={"topic": "test"})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert result.node_key == "start_1"
    assert result.node_type == "start"


def test_start_node_does_not_modify_input():
    executor = StartNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "start_1"
    workflow_node.node_type = "start"
    ctx = RuntimeContextSchema(input={"topic": "test"})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert ctx.input == {"topic": "test"}
