from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories.run_repo import RunRepository
from app.db.repositories.workflow_repo import WorkflowRepository
from app.schemas.execution import ExecutionTriggerRequest, ExecutionTriggerResponse, RunResponse, RunDetailResponse, RunListResponse, NodeRunResponse
from app.core.exceptions import NotFoundException


class ExecutionService:
    def __init__(self, db: Session):
        self.db = db
        self.run_repo = RunRepository(db)
        self.workflow_repo = WorkflowRepository(db)

    def trigger(self, req: ExecutionTriggerRequest, user_id: int) -> ExecutionTriggerResponse:
        workflow = self.workflow_repo.get_by_id(req.workflow_id)
        if not workflow:
            raise NotFoundException("Workflow")
        run = self.run_repo.create_run(workflow_id=req.workflow_id, input_payload=req.input_payload)
        from app.tasks.workflow_tasks import execute_workflow
        execute_workflow.delay(run.id)
        return ExecutionTriggerResponse(run_id=run.id, status=run.status)

    def get_run(self, run_id: int) -> RunDetailResponse:
        run = self.run_repo.get_run_by_id(run_id)
        if not run:
            raise NotFoundException("Run")
        node_runs = self.run_repo.get_node_runs(run.id)
        return RunDetailResponse(
            run=RunResponse.model_validate(run),
            node_runs=[NodeRunResponse.model_validate(nr) for nr in node_runs],
        )

    def list_runs(self, workflow_id: int, page: int = 1, page_size: int = 20) -> RunListResponse:
        items, total = self.run_repo.list_runs_by_workflow(workflow_id, page, page_size)
        return RunListResponse(total=total, items=[RunResponse.model_validate(r) for r in items])
