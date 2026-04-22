import pytest
from app.schemas.workflow import (
    WorkflowNodeSchema,
    WorkflowEdgeSchema,
    WorkflowCreateRequest,
    AgentNodeConfigSchema,
    ConditionNodeConfigSchema,
    ConditionBranchSchema,
    OutputNodeConfigSchema,
)


def test_node_type_valid():
    for t in ["start", "input", "agent", "condition", "output", "tool"]:
        node = WorkflowNodeSchema(node_key=f"{t}_1", node_type=t)
        assert node.node_type == t


def test_agent_node_config():
    config = AgentNodeConfigSchema(agent_id=1, task_instruction="Summarize")
    assert config.agent_id == 1
    assert config.retry_limit == 0


def test_condition_node_config():
    branch = ConditionBranchSchema(left_operand="$.score", operator="greater_than", right_operand=60, target_node_key="output_1")
    config = ConditionNodeConfigSchema(branches=[branch], default_target_key="output_2")
    assert len(config.branches) == 1
    assert config.default_target_key == "output_2"


def test_output_node_config():
    config = OutputNodeConfigSchema(source_keys=["$.node_outputs.agent_1"], output_format="json")
    assert len(config.source_keys) == 1
    assert config.output_format == "json"


def test_workflow_create_request():
    req = WorkflowCreateRequest(project_id=1, name="Test", nodes=[], edges=[])
    assert req.name == "Test"


def test_workflow_create_with_nodes():
    nodes = [WorkflowNodeSchema(node_key="start_1", node_type="start")]
    edges = []
    req = WorkflowCreateRequest(project_id=1, name="Test", nodes=nodes, edges=edges)
    assert len(req.nodes) == 1


def test_condition_branch_with_values():
    branch = ConditionBranchSchema(left_operand="x", operator="equals", right_operand=1, target_node_key="y")
    assert branch.operator == "equals"
    assert branch.left_operand == "x"
    assert branch.target_node_key == "y"
