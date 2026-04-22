from app.db.models.workflow import Workflow, WorkflowNode, WorkflowEdge
from app.db.models.project import Project
from app.db.models.user import User


def _setup(db):
    user = User(username="wfuser", email="wf@e.com", hashed_password="h")
    db.add(user)
    db.commit()
    project = Project(name="WFProject", owner_id=user.id)
    db.add(project)
    db.commit()
    return user, project


def test_workflow_create(db):
    user, project = _setup(db)
    wf = Workflow(name="TestWF", project_id=project.id)
    db.add(wf)
    db.commit()
    assert wf.id is not None


def test_workflow_with_nodes(db):
    user, project = _setup(db)
    wf = Workflow(name="NodeWF", project_id=project.id)
    db.add(wf)
    db.commit()
    n1 = WorkflowNode(workflow_id=wf.id, node_key="start_1", node_type="start")
    n2 = WorkflowNode(workflow_id=wf.id, node_key="output_1", node_type="output")
    db.add_all([n1, n2])
    db.commit()
    assert len(wf.nodes) == 2


def test_workflow_with_edges(db):
    user, project = _setup(db)
    wf = Workflow(name="EdgeWF", project_id=project.id)
    db.add(wf)
    db.commit()
    n1 = WorkflowNode(workflow_id=wf.id, node_key="start_1", node_type="start")
    n2 = WorkflowNode(workflow_id=wf.id, node_key="output_1", node_type="output")
    db.add_all([n1, n2])
    db.commit()
    edge = WorkflowEdge(workflow_id=wf.id, source_node_key="start_1", target_node_key="output_1")
    db.add(edge)
    db.commit()
    assert len(wf.edges) == 1


def test_node_key_unique_in_workflow(db):
    user, project = _setup(db)
    wf = Workflow(name="UniqueKey", project_id=project.id)
    db.add(wf)
    db.commit()
    n1 = WorkflowNode(workflow_id=wf.id, node_key="start_1", node_type="start")
    n2 = WorkflowNode(workflow_id=wf.id, node_key="start_1", node_type="start")
    db.add_all([n1, n2])
    from sqlalchemy.exc import IntegrityError
    try:
        db.commit()
        assert False, "Should have raised IntegrityError for duplicate node_key"
    except IntegrityError:
        db.rollback()
