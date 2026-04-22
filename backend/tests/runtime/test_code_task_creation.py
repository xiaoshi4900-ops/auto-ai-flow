from unittest.mock import MagicMock


def _runtime_service():
    import importlib

    mod = importlib.import_module("app.services.code_runtime_service")
    return mod.CodeRuntimeService()


def test_create_code_task_on_first_code_runtime_entry(db):
    service = _runtime_service()
    workflow_run = MagicMock(id=11)
    node_run = MagicMock(id=22)
    agent = MagicMock(id=33)

    created = service.create_code_task_if_absent(
        db_session=db,
        workflow_run=workflow_run,
        node_run=node_run,
        agent=agent,
        task_goal="Implement endpoint",
    )
    assert created is not None
    assert created.workflow_run_id == 11
    assert created.node_run_id == 22
    assert created.agent_id == 33
