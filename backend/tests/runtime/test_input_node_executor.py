from unittest.mock import MagicMock
from app.runtime.executors.input_node import InputNodeExecutor
from app.schemas.runtime import RuntimeContextSchema


def test_input_node_reads_payload():
    executor = InputNodeExecutor()
    workflow_run = MagicMock()
    workflow_run.input_payload = {"topic": "AI", "lang": "en"}
    workflow_node = MagicMock()
    workflow_node.node_key = "input_1"
    workflow_node.node_type = "input"
    workflow_node.config = {"input_mapping": {"topic": "topic"}}
    ctx = RuntimeContextSchema(input={"topic": "AI", "lang": "en"})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert result.output.structured_output["topic"] == "AI"


def test_input_node_no_mapping_passes_all():
    executor = InputNodeExecutor()
    workflow_run = MagicMock()
    workflow_run.input_payload = {"topic": "AI"}
    workflow_node = MagicMock()
    workflow_node.node_key = "input_1"
    workflow_node.node_type = "input"
    workflow_node.config = {}
    ctx = RuntimeContextSchema(input={"topic": "AI"})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert "topic" in result.output.structured_output


def test_input_node_empty_payload():
    executor = InputNodeExecutor()
    workflow_run = MagicMock()
    workflow_run.input_payload = {}
    workflow_node = MagicMock()
    workflow_node.node_key = "input_1"
    workflow_node.node_type = "input"
    workflow_node.config = {}
    ctx = RuntimeContextSchema(input={})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
