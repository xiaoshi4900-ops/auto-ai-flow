def _models():
    import importlib

    workspace_mod = importlib.import_module("app.db.models.code_workspace")
    task_mod = importlib.import_module("app.db.models.code_task")
    iteration_mod = importlib.import_module("app.db.models.code_iteration")
    return workspace_mod.CodeWorkspace, task_mod.CodeTask, iteration_mod.CodeIteration


def test_code_task_can_bind_run_node_and_agent(db):
    _, CodeTask, _ = _models()
    task = CodeTask(
        workflow_run_id=101,
        node_run_id=202,
        agent_id=303,
        task_goal="Implement auth API",
        status="running",
    )
    db.add(task)
    db.commit()
    assert task.id is not None
    assert task.workflow_run_id == 101
    assert task.node_run_id == 202
    assert task.agent_id == 303


def test_code_iteration_keeps_iteration_number_and_validation_status(db):
    _, CodeTask, CodeIteration = _models()
    task = CodeTask(
        workflow_run_id=111,
        node_run_id=222,
        agent_id=333,
        task_goal="Refactor x",
        status="running",
    )
    db.add(task)
    db.commit()
    iteration = CodeIteration(
        code_task_id=task.id,
        iteration_no=1,
        status="running",
        validation_lint="passed",
        validation_build="skipped",
        validation_unit_tests="failed",
    )
    db.add(iteration)
    db.commit()
    assert iteration.id is not None
    assert iteration.iteration_no == 1
    assert iteration.validation_lint == "passed"
