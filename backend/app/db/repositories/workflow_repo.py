from sqlalchemy.orm import Session

from app.db.models.workflow import Workflow, WorkflowNode, WorkflowEdge


class WorkflowRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, workflow_id: int) -> Workflow | None:
        return self.db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.is_deleted == False).first()

    def list_by_project(self, project_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Workflow], int]:
        query = self.db.query(Workflow).filter(Workflow.project_id == project_id, Workflow.is_deleted == False)
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(self, project_id: int, name: str, description: str | None = None, nodes: list[dict] | None = None, edges: list[dict] | None = None) -> Workflow:
        workflow = Workflow(project_id=project_id, name=name, description=description)
        self.db.add(workflow)
        self.db.flush()
        if nodes:
            for n in nodes:
                node = WorkflowNode(workflow_id=workflow.id, **n)
                self.db.add(node)
        if edges:
            for e in edges:
                edge = WorkflowEdge(workflow_id=workflow.id, **e)
                self.db.add(edge)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def update(self, workflow: Workflow, **kwargs) -> Workflow:
        nodes_data = kwargs.pop("nodes", None)
        edges_data = kwargs.pop("edges", None)
        for key, value in kwargs.items():
            if value is not None and hasattr(workflow, key):
                setattr(workflow, key, value)
        if nodes_data is not None:
            self.db.query(WorkflowNode).filter(WorkflowNode.workflow_id == workflow.id).delete()
            for n in nodes_data:
                self.db.add(WorkflowNode(workflow_id=workflow.id, **n))
        if edges_data is not None:
            self.db.query(WorkflowEdge).filter(WorkflowEdge.workflow_id == workflow.id).delete()
            for e in edges_data:
                self.db.add(WorkflowEdge(workflow_id=workflow.id, **e))
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def soft_delete(self, workflow: Workflow) -> Workflow:
        workflow.is_deleted = True
        self.db.commit()
        return workflow
