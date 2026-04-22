from unittest.mock import MagicMock
from app.runtime.executors.output_node import OutputNodeExecutor
from app.schemas.runtime import RuntimeContextSchema


def test_output_node_aggregates_sources():
    executor = OutputNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "output_1"
    workflow_node.node_type = "output"
    workflow_node.config = {
        "source_keys": ["agent_1"],
        "output_format": "json",
    }
    ctx = RuntimeContextSchema(
        node_outputs={"agent_1": {"structured_output": {"summary": "test"}}},
    )
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert "agent_1" in result.output.structured_output
    assert result.output.structured_output["agent_1"]["structured_output"]["summary"] == "test"


def test_output_node_no_sources():
    executor = OutputNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "output_1"
    workflow_node.node_type = "output"
    workflow_node.config = {}
    ctx = RuntimeContextSchema(
        node_outputs={"agent_1": {"structured_output": {"summary": "test"}}},
    )
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert "agent_1" in result.output.structured_output


def test_output_node_missing_source_key():
    executor = OutputNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "output_1"
    workflow_node.node_type = "output"
    workflow_node.config = {
        "source_keys": ["nonexistent"],
    }
    ctx = RuntimeContextSchema(node_outputs={})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert result.output.structured_output == {}
