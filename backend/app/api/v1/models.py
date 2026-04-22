from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.model import ModelListResponse, ProjectModelConfigCreateRequest, ProjectModelConfigResponse
from app.services.model_service import ModelService

router = APIRouter()


@router.get("", response_model=ModelListResponse)
def list_models(db: Session = Depends(get_db_session)):
    svc = ModelService(db)
    return svc.list_models()


@router.post("/project/{project_id}/configs", response_model=ProjectModelConfigResponse)
def create_project_config(project_id: int, req: ProjectModelConfigCreateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ModelService(db)
    return svc.create_project_model_config(project_id, req)


@router.get("/project/{project_id}/configs", response_model=list[ProjectModelConfigResponse])
def list_project_configs(project_id: int, db: Session = Depends(get_db_session)):
    svc = ModelService(db)
    return svc.list_project_model_configs(project_id)
