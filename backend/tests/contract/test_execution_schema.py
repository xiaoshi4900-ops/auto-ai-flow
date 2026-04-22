import pytest
from app.schemas.execution import RunResponse, NodeRunResponse, ExecutionTriggerRequest


def test_run_response_fields():
    resp = RunResponse(id=1, workflow_id=1, status="success")
    dumped = resp.model_dump()
    assert "id" in dumped
    assert "workflow_id" in dumped
    assert "status" in dumped
    assert "input_payload" in dumped
    assert "output_payload" in dumped


def test_node_run_response_fields():
    resp = NodeRunResponse(id=1, workflow_run_id=1, node_key="start_1", node_type="start", status="success")
    dumped = resp.model_dump()
    assert "node_key" in dumped
    assert "node_type" in dumped
    assert "status" in dumped
    assert "output_data" in dumped


def test_execution_trigger_request_defaults():
    req = ExecutionTriggerRequest(workflow_id=1)
    assert req.input_payload is None


def test_execution_trigger_request_with_payload():
    req = ExecutionTriggerRequest(workflow_id=1, input_payload={"topic": "test"})
    assert req.input_payload == {"topic": "test"}
