from unittest.mock import MagicMock
from app.runtime.executors.condition_node import ConditionNodeExecutor
from app.schemas.runtime import RuntimeContextSchema


def test_condition_true_branch():
    executor = ConditionNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "cond_1"
    workflow_node.node_type = "condition"
    workflow_node.config = {
        "branches": [
            {"left_operand": "input.score", "operator": "greater_than", "right_operand": 60, "target_node_key": "output_1"},
        ],
        "default_target_key": "output_2",
    }
    ctx = RuntimeContextSchema(input={"score": 80})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.status == "success"
    assert result.next_node_key == "output_1"


def test_condition_false_branch():
    executor = ConditionNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "cond_1"
    workflow_node.node_type = "condition"
    workflow_node.config = {
        "branches": [
            {"left_operand": "input.score", "operator": "greater_than", "right_operand": 60, "target_node_key": "output_1"},
        ],
        "default_target_key": "output_2",
    }
    ctx = RuntimeContextSchema(input={"score": 30})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.next_node_key == "output_2"


def test_condition_default_branch():
    executor = ConditionNodeExecutor()
    workflow_run = MagicMock()
    workflow_node = MagicMock()
    workflow_node.node_key = "cond_1"
    workflow_node.node_type = "condition"
    workflow_node.config = {
        "branches": [],
        "default_target_key": "output_default",
    }
    ctx = RuntimeContextSchema(input={})
    result = executor.execute(workflow_run, workflow_node, ctx)
    assert result.next_node_key == "output_default"
