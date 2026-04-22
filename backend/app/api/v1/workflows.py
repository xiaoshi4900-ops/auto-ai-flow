from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.workflow import WorkflowCreateRequest, WorkflowUpdateRequest, WorkflowResponse, WorkflowListResponse
from app.services.workflow_service import WorkflowService

router = APIRouter()


@router.post("", response_model=WorkflowResponse)
def create_workflow(req: WorkflowCreateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = WorkflowService(db)
    return svc.create(req, user_id)


@router.get("", response_model=WorkflowListResponse)
def list_workflows(project_id: int = Query(...), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = WorkflowService(db)
    return svc.list_by_project(project_id, user_id, page, page_size)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = WorkflowService(db)
    return svc.get(workflow_id, user_id)


@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(workflow_id: int, req: WorkflowUpdateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = WorkflowService(db)
    return svc.update(workflow_id, req, user_id)


@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = WorkflowService(db)
    svc.delete(workflow_id, user_id)
    return {"message": "Workflow deleted"}
