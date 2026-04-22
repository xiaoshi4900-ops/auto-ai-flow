from app.db.models.run import WorkflowRun, NodeRun
from app.db.models.workflow import Workflow
from app.db.models.project import Project
from app.db.models.user import User


def _setup(db):
    user = User(username="runuser", email="run@e.com", hashed_password="h")
    db.add(user)
    db.commit()
    project = Project(name="RunProject", owner_id=user.id)
    db.add(project)
    db.commit()
    wf = Workflow(name="RunWF", project_id=project.id)
    db.add(wf)
    db.commit()
    return user, project, wf


def test_workflow_run_create(db):
    user, project, wf = _setup(db)
    run = WorkflowRun(workflow_id=wf.id, status="pending", input_payload={"topic": "test"})
    db.add(run)
    db.commit()
    assert run.id is not None
    assert run.status == "pending"


def test_workflow_run_status_update(db):
    user, project, wf = _setup(db)
    run = WorkflowRun(workflow_id=wf.id, status="pending", input_payload={})
    db.add(run)
    db.commit()
    run.status = "running"
    db.commit()
    db.refresh(run)
    assert run.status == "running"


def test_node_run_create(db):
    user, project, wf = _setup(db)
    run = WorkflowRun(workflow_id=wf.id, status="running", input_payload={})
    db.add(run)
    db.commit()
    ne = NodeRun(workflow_run_id=run.id, node_key="start_1", node_type="start", status="success")
    db.add(ne)
    db.commit()
    assert ne.id is not None


def test_node_run_output(db):
    user, project, wf = _setup(db)
    run = WorkflowRun(workflow_id=wf.id, status="running", input_payload={})
    db.add(run)
    db.commit()
    ne = NodeRun(workflow_run_id=run.id, node_key="agent_1", node_type="agent", status="success", output_data={"structured_output": {"summary": "done"}})
    db.add(ne)
    db.commit()
    db.refresh(ne)
    assert ne.output_data["structured_output"]["summary"] == "done"


def test_run_cascade_delete(db):
    user, project, wf = _setup(db)
    run = WorkflowRun(workflow_id=wf.id, status="success", input_payload={})
    db.add(run)
    db.commit()
    ne = NodeRun(workflow_run_id=run.id, node_key="start_1", node_type="start", status="success")
    db.add(ne)
    db.commit()
    db.delete(run)
    db.commit()
    remaining = db.query(NodeRun).filter(NodeRun.workflow_run_id == run.id).first()
    assert remaining is None
