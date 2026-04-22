from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.db.models.code_task import CodeTask
from app.db.models.code_iteration import CodeIteration
from app.db.models.run import WorkflowRun
from app.db.models.workflow import Workflow
from app.db.models.project import Project
from app.core.exceptions import NotFoundException, ForbiddenException

router = APIRouter()


def _check_run_access(run_id: int, user_id: int, db: Session):
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if not run:
        raise NotFoundException("Run")
    workflow = db.query(Workflow).filter(Workflow.id == run.workflow_id).first()
    if not workflow:
        raise NotFoundException("Workflow")
    project = db.query(Project).filter(Project.id == workflow.project_id).first()
    if not project or project.owner_id != user_id:
        raise ForbiddenException("Not project owner")
    return run


@router.get("/runs/{run_id}/code-iterations")
def list_code_iterations_by_run(run_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    _check_run_access(run_id, user_id, db)
    tasks = db.query(CodeTask).filter(CodeTask.workflow_run_id == run_id).all()
    items = []
    for task in tasks:
        for iteration in task.iterations:
            items.append({
                "id": iteration.id,
                "code_task_id": task.id,
                "iteration_no": iteration.iteration_no,
                "status": iteration.status,
                "plan_summary": iteration.plan_summary,
                "changed_files": iteration.changed_files,
                "validation_lint": iteration.validation_lint,
                "validation_build": iteration.validation_build,
                "validation_unit_tests": iteration.validation_unit_tests,
            })
    items.sort(key=lambda x: x["iteration_no"])
    return {"items": items}


@router.get("/code-tasks/{task_id}")
def get_code_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    task = db.query(CodeTask).filter(CodeTask.id == task_id).first()
    if not task:
        raise NotFoundException("CodeTask")
    if task.workflow_run_id:
        _check_run_access(task.workflow_run_id, user_id, db)
    return {
        "id": task.id,
        "workflow_run_id": task.workflow_run_id,
        "node_run_id": task.node_run_id,
        "agent_id": task.agent_id,
        "task_goal": task.task_goal,
        "scope": task.scope,
        "acceptance_criteria": task.acceptance_criteria,
        "status": task.status,
    }


@router.get("/code-tasks/{task_id}/iterations")
def list_code_task_iterations(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    task = db.query(CodeTask).filter(CodeTask.id == task_id).first()
    if not task:
        raise NotFoundException("CodeTask")
    if task.workflow_run_id:
        _check_run_access(task.workflow_run_id, user_id, db)
    items = []
    for iteration in task.iterations:
        items.append({
            "id": iteration.id,
            "iteration_no": iteration.iteration_no,
            "status": iteration.status,
            "plan_summary": iteration.plan_summary,
            "validation_lint": iteration.validation_lint,
            "validation_build": iteration.validation_build,
            "validation_unit_tests": iteration.validation_unit_tests,
        })
    return {"items": items}
