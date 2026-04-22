from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.execution import ExecutionTriggerRequest, ExecutionTriggerResponse
from app.services.execution_service import ExecutionService

router = APIRouter()


@router.post("/trigger", response_model=ExecutionTriggerResponse)
def trigger_execution(req: ExecutionTriggerRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ExecutionService(db)
    return svc.trigger(req, user_id)
