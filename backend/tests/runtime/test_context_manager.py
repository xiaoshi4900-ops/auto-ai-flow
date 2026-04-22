from app.runtime.context_manager import ContextManager
from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema, HandoffPayloadSchema


def test_init_context():
    cm = ContextManager()
    ctx = cm.init_context({"topic": "AI"})
    assert ctx.input == {"topic": "AI"}
    assert ctx.node_outputs == {}


def test_merge_node_result():
    cm = ContextManager()
    ctx = cm.init_context({"topic": "AI"})
    result = NodeExecutionResultSchema(
        node_key="agent_1",
        node_type="agent",
        status="success",
        output=StructuredOutputSchema(status="success", structured_output={"summary": "AI is great"}),
        handoff=HandoffPayloadSchema(handoff_summary="Done"),
    )
    ctx = cm.merge_node_result(ctx, "agent_1", result)
    assert "agent_1" in ctx.node_outputs
    assert ctx.node_outputs["agent_1"]["structured_output"]["summary"] == "AI is great"


def test_merge_preserves_previous_outputs():
    cm = ContextManager()
    ctx = cm.init_context({})
    result1 = NodeExecutionResultSchema(node_key="n1", node_type="start", output=StructuredOutputSchema(status="success", structured_output={"a": 1}))
    ctx = cm.merge_node_result(ctx, "n1", result1)
    result2 = NodeExecutionResultSchema(node_key="n2", node_type="agent", output=StructuredOutputSchema(status="success", structured_output={"b": 2}))
    ctx = cm.merge_node_result(ctx, "n2", result2)
    assert "n1" in ctx.node_outputs
    assert "n2" in ctx.node_outputs


def test_merge_artifact_refs():
    cm = ContextManager()
    ctx = cm.init_context({})
    result = NodeExecutionResultSchema(
        node_key="n1",
        node_type="agent",
        output=StructuredOutputSchema(status="success", artifact_refs=[{"ref": "file.txt"}]),
    )
    ctx = cm.merge_node_result(ctx, "n1", result)
    assert "n1" in ctx.artifacts
    assert ctx.artifacts["n1"][0]["ref"] == "file.txt"


def test_merge_handoff_to_messages():
    cm = ContextManager()
    ctx = cm.init_context({})
    result = NodeExecutionResultSchema(
        node_key="n1",
        node_type="agent",
        output=StructuredOutputSchema(status="success"),
        handoff=HandoffPayloadSchema(handoff_summary="Completed task"),
    )
    ctx = cm.merge_node_result(ctx, "n1", result)
    assert "n1_handoff" in ctx.shared_state
