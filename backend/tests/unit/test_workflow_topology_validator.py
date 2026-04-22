import pytest
from app.services.workflow_service import WorkflowService
from app.schemas.workflow import WorkflowNodeSchema, WorkflowEdgeSchema
from app.core.exceptions import BadRequestException


def test_validate_single_start():
    nodes = [
        WorkflowNodeSchema(node_key="start_1", node_type="start"),
        WorkflowNodeSchema(node_key="output_1", node_type="output"),
    ]
    edges = [WorkflowEdgeSchema(source_node_key="start_1", target_node_key="output_1")]
    service = WorkflowService.__new__(WorkflowService)
    service._validate_workflow(nodes, edges)


def test_validate_invalid_node_type():
    nodes = [
        WorkflowNodeSchema(node_key="bad_1", node_type="invalid_type"),
    ]
    edges = []
    service = WorkflowService.__new__(WorkflowService)
    with pytest.raises(BadRequestException):
        service._validate_workflow(nodes, edges)


def test_validate_edge_source_exists():
    nodes = [
        WorkflowNodeSchema(node_key="start_1", node_type="start"),
        WorkflowNodeSchema(node_key="output_1", node_type="output"),
    ]
    edges = [WorkflowEdgeSchema(source_node_key="nonexistent", target_node_key="output_1")]
    service = WorkflowService.__new__(WorkflowService)
    with pytest.raises(BadRequestException):
        service._validate_workflow(nodes, edges)


def test_validate_edge_target_exists():
    nodes = [
        WorkflowNodeSchema(node_key="start_1", node_type="start"),
        WorkflowNodeSchema(node_key="output_1", node_type="output"),
    ]
    edges = [WorkflowEdgeSchema(source_node_key="start_1", target_node_key="nonexistent")]
    service = WorkflowService.__new__(WorkflowService)
    with pytest.raises(BadRequestException):
        service._validate_workflow(nodes, edges)


def test_validate_valid_multi_node():
    nodes = [
        WorkflowNodeSchema(node_key="start_1", node_type="start"),
        WorkflowNodeSchema(node_key="agent_1", node_type="agent"),
        WorkflowNodeSchema(node_key="output_1", node_type="output"),
    ]
    edges = [
        WorkflowEdgeSchema(source_node_key="start_1", target_node_key="agent_1"),
        WorkflowEdgeSchema(source_node_key="agent_1", target_node_key="output_1"),
    ]
    service = WorkflowService.__new__(WorkflowService)
    service._validate_workflow(nodes, edges)
