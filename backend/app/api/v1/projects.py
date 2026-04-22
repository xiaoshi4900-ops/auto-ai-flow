from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse, ProjectListResponse
from app.schemas.agent import AgentResponse
from app.services.project_service import ProjectService
from app.services.agent_service import AgentService

router = APIRouter()


class AgentFromTemplateRequest(BaseModel):
    role_template_id: int
    name: str | None = None
    description: str | None = None
    model_id: int | None = None


@router.post("", response_model=ProjectResponse)
def create_project(req: ProjectCreateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ProjectService(db)
    return svc.create(req, user_id)


@router.get("", response_model=ProjectListResponse)
def list_projects(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ProjectService(db)
    return svc.list_projects(user_id, page, page_size)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ProjectService(db)
    return svc.get(project_id, user_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, req: ProjectUpdateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ProjectService(db)
    return svc.update(project_id, req, user_id)


@router.delete("/{project_id}")
def delete_project(project_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = ProjectService(db)
    svc.delete(project_id, user_id)
    return {"message": "Project deleted"}


@router.post("/{project_id}/agents/from-template", response_model=AgentResponse)
def create_agent_from_template(project_id: int, req: AgentFromTemplateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.create_from_template(project_id, req.role_template_id, user_id, name=req.name, description=req.description, model_id=req.model_id)
