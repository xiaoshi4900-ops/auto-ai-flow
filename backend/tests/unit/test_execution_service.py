import pytest
from unittest.mock import MagicMock, patch
from app.services.execution_service import ExecutionService
from app.schemas.execution import ExecutionTriggerRequest
from app.core.exceptions import NotFoundException


def test_trigger_run(db):
    service = ExecutionService(db)
    mock_workflow = MagicMock()
    mock_workflow.id = 1
    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.status = "pending"
    with patch.object(service.workflow_repo, "get_by_id", return_value=mock_workflow):
        with patch.object(service.run_repo, "create_run", return_value=mock_run):
            with patch("app.tasks.workflow_tasks.execute_workflow") as mock_task:
                mock_task.delay = MagicMock()
                req = ExecutionTriggerRequest(workflow_id=1)
                result = service.trigger(req, user_id=1)
    assert result.run_id == 1
    assert result.status == "pending"


def test_trigger_run_workflow_not_found(db):
    service = ExecutionService(db)
    with patch.object(service.workflow_repo, "get_by_id", return_value=None):
        with pytest.raises(NotFoundException):
            req = ExecutionTriggerRequest(workflow_id=999)
            service.trigger(req, user_id=1)


def test_get_run(db):
    service = ExecutionService(db)
    mock_run = MagicMock()
    mock_run.id = 1
    mock_run.workflow_id = 1
    mock_run.status = "success"
    mock_run.input_payload = {}
    mock_run.output_payload = None
    mock_run.error_message = None
    mock_run.started_at = None
    mock_run.finished_at = None
    mock_run.created_at = None
    with patch.object(service.run_repo, "get_run_by_id", return_value=mock_run):
        with patch.object(service.run_repo, "get_node_runs", return_value=[]):
            result = service.get_run(1)
    assert result.run.status == "success"


def test_get_run_not_found(db):
    service = ExecutionService(db)
    with patch.object(service.run_repo, "get_run_by_id", return_value=None):
        with pytest.raises(NotFoundException):
            service.get_run(999)


def test_list_runs(db):
    service = ExecutionService(db)
    with patch.object(service.run_repo, "list_runs_by_workflow", return_value=([], 0)):
        result = service.list_runs(workflow_id=1)
    assert result.total == 0
