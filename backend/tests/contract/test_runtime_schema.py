import pytest
from app.schemas.runtime import (
    RuntimeContextSchema,
    StructuredOutputSchema,
    HandoffPayloadSchema,
    NodeExecutionResultSchema,
)


def test_runtime_context_defaults():
    ctx = RuntimeContextSchema()
    assert ctx.input == {}
    assert ctx.shared_state == {}
    assert ctx.node_outputs == {}
    assert ctx.artifacts == {}
    assert ctx.messages == {}
    assert ctx.meta == {}


def test_structured_output_status_values():
    s = StructuredOutputSchema(status="success")
    assert s.status == "success"
    s2 = StructuredOutputSchema(status="failed")
    assert s2.status == "failed"


def test_structured_output_invalid_status():
    with pytest.raises(Exception):
        StructuredOutputSchema(status="unknown")


def test_handoff_payload_fields():
    h = HandoffPayloadSchema()
    assert h.handoff_summary == ""
    assert h.assumptions == []
    assert h.risks == []
    assert h.questions_for_next_node == []


def test_handoff_payload_with_values():
    h = HandoffPayloadSchema(
        handoff_summary="summary",
        assumptions=["a1"],
        risks=["r1"],
        questions_for_next_node=["q1"],
    )
    assert h.handoff_summary == "summary"
    assert len(h.assumptions) == 1


def test_node_execution_result_defaults():
    r = NodeExecutionResultSchema(node_key="start_1", node_type="start")
    assert r.status == "success"
    assert r.next_node_key is None
    assert r.error_message is None


def test_node_execution_result_failed():
    r = NodeExecutionResultSchema(node_key="agent_1", node_type="agent", status="failed", error_message="timeout")
    assert r.status == "failed"
    assert r.error_message == "timeout"
