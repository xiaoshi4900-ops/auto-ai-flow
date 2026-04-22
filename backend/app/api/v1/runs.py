from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.execution import RunResponse, RunDetailResponse, RunListResponse
from app.services.execution_service import ExecutionService

router = APIRouter()


@router.get("", response_model=RunListResponse)
def list_runs(workflow_id: int = Query(...), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db_session)):
    svc = ExecutionService(db)
    return svc.list_runs(workflow_id, page, page_size)


@router.get("/{run_id}", response_model=RunDetailResponse)
def get_run(run_id: int, db: Session = Depends(get_db_session)):
    svc = ExecutionService(db)
    return svc.get_run(run_id)
