from sqlalchemy.orm import Session

from app.db.models.run import WorkflowRun, NodeRun, RunArtifact


class RunRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_run_by_id(self, run_id: int) -> WorkflowRun | None:
        return self.db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()

    def list_runs_by_workflow(self, workflow_id: int, page: int = 1, page_size: int = 20) -> tuple[list[WorkflowRun], int]:
        query = self.db.query(WorkflowRun).filter(WorkflowRun.workflow_id == workflow_id)
        total = query.count()
        items = query.order_by(WorkflowRun.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create_run(self, workflow_id: int, input_payload: dict | None = None) -> WorkflowRun:
        run = WorkflowRun(workflow_id=workflow_id, status="pending", input_payload=input_payload)
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def update_run_status(self, run: WorkflowRun, status: str, error_message: str | None = None, output_payload: dict | None = None) -> WorkflowRun:
        run.status = status
        if error_message is not None:
            run.error_message = error_message
        if output_payload is not None:
            run.output_payload = output_payload
        self.db.commit()
        self.db.refresh(run)
        return run

    def create_node_run(self, workflow_run_id: int, node_key: str, node_type: str, input_data: dict | None = None) -> NodeRun:
        node_run = NodeRun(workflow_run_id=workflow_run_id, node_key=node_key, node_type=node_type, status="running", input_data=input_data)
        self.db.add(node_run)
        self.db.commit()
        self.db.refresh(node_run)
        return node_run

    def update_node_run(self, node_run: NodeRun, **kwargs) -> NodeRun:
        for key, value in kwargs.items():
            if hasattr(node_run, key):
                setattr(node_run, key, value)
        self.db.commit()
        self.db.refresh(node_run)
        return node_run

    def get_node_runs(self, workflow_run_id: int) -> list[NodeRun]:
        return self.db.query(NodeRun).filter(NodeRun.workflow_run_id == workflow_run_id).order_by(NodeRun.started_at).all()
