from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.agent import AgentCreateRequest, AgentUpdateRequest, AgentResponse, AgentListResponse, AgentSkillBindRequest, AgentToolBindRequest
from app.services.agent_service import AgentService

router = APIRouter()


@router.post("", response_model=AgentResponse)
def create_agent(req: AgentCreateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.create(req, user_id)


@router.get("", response_model=AgentListResponse)
def list_agents(project_id: int = Query(...), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.list_by_project(project_id, user_id, page, page_size)


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.get(agent_id, user_id)


@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: int, req: AgentUpdateRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.update(agent_id, req, user_id)


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    svc.delete(agent_id, user_id)
    return {"message": "Agent deleted"}


@router.post("/{agent_id}/skills", response_model=AgentResponse)
def bind_skills(agent_id: int, req: AgentSkillBindRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.bind_skills(agent_id, req.skill_ids, user_id)


@router.post("/{agent_id}/tools", response_model=AgentResponse)
def bind_tools(agent_id: int, req: AgentToolBindRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AgentService(db)
    return svc.bind_tools(agent_id, req.tool_ids, user_id)
