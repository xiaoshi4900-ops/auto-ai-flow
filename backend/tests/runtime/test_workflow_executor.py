from unittest.mock import MagicMock, patch
from app.runtime.workflow_executor import WorkflowExecutor
from app.schemas.runtime import RuntimeContextSchema, NodeExecutionResultSchema, StructuredOutputSchema
from app.db.models.workflow import Workflow, WorkflowNode, WorkflowEdge


def _make_workflow():
    wf = MagicMock(spec=Workflow)
    wf.id = 1
    wf.name = "TestWF"
    n1 = MagicMock(spec=WorkflowNode)
    n1.node_key = "start_1"
    n1.node_type = "start"
    n1.config = {}
    n2 = MagicMock(spec=WorkflowNode)
    n2.node_key = "output_1"
    n2.node_type = "output"
    n2.config = {}
    e1 = MagicMock(spec=WorkflowEdge)
    e1.source_node_key = "start_1"
    e1.target_node_key = "output_1"
    e1.condition = None
    wf.nodes = [n1, n2]
    wf.edges = [e1]
    return wf


def _make_executor(db=None):
    mock_db = db or MagicMock()
    with patch("app.runtime.workflow_executor.RunRepository") as mock_run_repo_cls, \
         patch("app.runtime.workflow_executor.WorkflowRepository") as mock_wf_repo_cls:
        mock_run_repo = MagicMock()
        mock_wf_repo = MagicMock()
        mock_run_repo_cls.return_value = mock_run_repo
        mock_wf_repo_cls.return_value = mock_wf_repo
        executor = WorkflowExecutor(mock_db)
        executor.run_repo = mock_run_repo
        executor.workflow_repo = mock_wf_repo
    return executor


def test_workflow_executor_runs_linear():
    executor = _make_executor()
    wf = _make_workflow()
    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.workflow_id = 1
    mock_run.input_payload = {"topic": "test"}
    mock_run.started_at = None

    executor.run_repo.get_run_by_id.return_value = mock_run
    executor.workflow_repo.get_by_id.return_value = wf
    executor.run_repo.create_node_run.return_value = MagicMock(started_at=None)

    call_count = 0
    def mock_get_executor(node_type):
        nonlocal call_count
        mock_executor = MagicMock()
        if call_count == 0:
            mock_executor.execute.return_value = NodeExecutionResultSchema(
                node_key="start_1", node_type="start", status="success"
            )
        else:
            mock_executor.execute.return_value = NodeExecutionResultSchema(
                node_key="output_1", node_type="output", status="success",
                output=StructuredOutputSchema(status="success")
            )
        call_count += 1
        return mock_executor

    with patch.object(executor.executor_factory, "get_executor", side_effect=mock_get_executor):
        result = executor.execute(1)
    assert result["status"] == "success"


def test_workflow_executor_condition_branch():
    executor = _make_executor()
    wf = MagicMock(spec=Workflow)
    wf.id = 1
    n1 = MagicMock()
    n1.node_key = "start_1"
    n1.node_type = "start"
    n1.config = {}
    n2 = MagicMock()
    n2.node_key = "cond_1"
    n2.node_type = "condition"
    n2.config = {"branches": [{"left_operand": "input.score", "operator": "greater_than", "right_operand": 60, "target_node_key": "output_1"}], "default_target_key": "output_2"}
    n3 = MagicMock()
    n3.node_key = "output_1"
    n3.node_type = "output"
    n3.config = {}
    n4 = MagicMock()
    n4.node_key = "output_2"
    n4.node_type = "output"
    n4.config = {}
    e1 = MagicMock()
    e1.source_node_key = "start_1"
    e1.target_node_key = "cond_1"
    e1.condition = None
    e2 = MagicMock()
    e2.source_node_key = "cond_1"
    e2.target_node_key = "output_1"
    e2.condition = "branch_0"
    e3 = MagicMock()
    e3.source_node_key = "cond_1"
    e3.target_node_key = "output_2"
    e3.condition = "default"
    wf.nodes = [n1, n2, n3, n4]
    wf.edges = [e1, e2, e3]

    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.workflow_id = 1
    mock_run.input_payload = {"score": 80}
    mock_run.started_at = None

    executor.run_repo.get_run_by_id.return_value = mock_run
    executor.workflow_repo.get_by_id.return_value = wf
    executor.run_repo.create_node_run.return_value = MagicMock(started_at=None)

    call_count = 0
    def mock_get_executor(node_type):
        nonlocal call_count
        mock_executor = MagicMock()
        if call_count == 0:
            mock_executor.execute.return_value = NodeExecutionResultSchema(
                node_key="start_1", node_type="start", status="success"
            )
        elif call_count == 1:
            mock_executor.execute.return_value = NodeExecutionResultSchema(
                node_key="cond_1", node_type="condition", status="success", next_node_key="output_1"
            )
        else:
            mock_executor.execute.return_value = NodeExecutionResultSchema(
                node_key="output_1", node_type="output", status="success",
                output=StructuredOutputSchema(status="success")
            )
        call_count += 1
        return mock_executor

    with patch.object(executor.executor_factory, "get_executor", side_effect=mock_get_executor):
        result = executor.execute(1)
    assert result["status"] == "success"


def test_workflow_executor_no_start_node():
    executor = _make_executor()
    wf = MagicMock(spec=Workflow)
    wf.id = 1
    wf.nodes = []
    wf.edges = []

    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.workflow_id = 1
    mock_run.input_payload = {}
    mock_run.started_at = None

    executor.run_repo.get_run_by_id.return_value = mock_run
    executor.workflow_repo.get_by_id.return_value = wf

    result = executor.execute(1)
    assert result["status"] == "failed"
