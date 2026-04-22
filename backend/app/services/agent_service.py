import json

from sqlalchemy.orm import Session

from app.db.repositories.agent_repo import AgentRepository
from app.db.repositories.project_repo import ProjectRepository
from app.db.models.role_template import RoleTemplate
from app.schemas.agent import AgentCreateRequest, AgentUpdateRequest, AgentResponse, AgentListResponse
from app.core.exceptions import NotFoundException, ForbiddenException


class AgentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AgentRepository(db)
        self.project_repo = ProjectRepository(db)

    def _check_project_owner(self, project_id: int, user_id: int):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundException("Project")
        if project.owner_id != user_id:
            raise ForbiddenException("Not project owner")

    def create(self, req: AgentCreateRequest, user_id: int) -> AgentResponse:
        self._check_project_owner(req.project_id, user_id)
        data = req.model_dump(exclude={"skill_ids", "tool_ids"})
        agent = self.repo.create(**data)
        if req.skill_ids:
            self.repo.bind_skills(agent, req.skill_ids)
        if req.tool_ids:
            self.repo.bind_tools(agent, req.tool_ids)
        return self._to_response(agent)

    def get(self, agent_id: int, user_id: int) -> AgentResponse:
        agent = self.repo.get_by_id(agent_id)
        if not agent:
            raise NotFoundException("Agent")
        self._check_project_owner(agent.project_id, user_id)
        return self._to_response(agent)

    def list_by_project(self, project_id: int, user_id: int, page: int = 1, page_size: int = 20) -> AgentListResponse:
        self._check_project_owner(project_id, user_id)
        items, total = self.repo.list_by_project(project_id, page, page_size)
        return AgentListResponse(total=total, items=[self._to_response(a) for a in items])

    def update(self, agent_id: int, req: AgentUpdateRequest, user_id: int) -> AgentResponse:
        agent = self.repo.get_by_id(agent_id)
        if not agent:
            raise NotFoundException("Agent")
        self._check_project_owner(agent.project_id, user_id)
        updated = self.repo.update(agent, **req.model_dump(exclude_unset=True))
        return self._to_response(updated)

    def delete(self, agent_id: int, user_id: int) -> None:
        agent = self.repo.get_by_id(agent_id)
        if not agent:
            raise NotFoundException("Agent")
        self._check_project_owner(agent.project_id, user_id)
        self.repo.soft_delete(agent)

    def bind_skills(self, agent_id: int, skill_ids: list[int], user_id: int) -> AgentResponse:
        agent = self.repo.get_by_id(agent_id)
        if not agent:
            raise NotFoundException("Agent")
        self._check_project_owner(agent.project_id, user_id)
        agent = self.repo.bind_skills(agent, skill_ids)
        return self._to_response(agent)

    def bind_tools(self, agent_id: int, tool_ids: list[int], user_id: int) -> AgentResponse:
        agent = self.repo.get_by_id(agent_id)
        if not agent:
            raise NotFoundException("Agent")
        self._check_project_owner(agent.project_id, user_id)
        agent = self.repo.bind_tools(agent, tool_ids)
        return self._to_response(agent)

    def create_from_template(self, project_id: int, role_template_id: int, user_id: int, name: str | None = None, description: str | None = None, model_id: int | None = None) -> AgentResponse:
        self._check_project_owner(project_id, user_id)
        tpl = self.db.query(RoleTemplate).filter(RoleTemplate.id == role_template_id).first()
        if not tpl:
            raise NotFoundException("RoleTemplate", error_code="ROLE_TEMPLATE_NOT_FOUND")

        agent_name = name or tpl.name
        agent_description = description or tpl.description
        agent_model_id = model_id or tpl.default_model_id

        agent = self.repo.create(
            name=agent_name,
            project_id=project_id,
            role_name=tpl.default_role_name or tpl.key,
            description=agent_description,
            model_id=agent_model_id,
            role_template_id=tpl.id,
        )

        default_skill_ids = json.loads(tpl.default_skill_ids) if tpl.default_skill_ids else []
        default_tool_ids = json.loads(tpl.default_tool_ids) if tpl.default_tool_ids else []
        if default_skill_ids:
            self.repo.bind_skills(agent, default_skill_ids)
        if default_tool_ids:
            self.repo.bind_tools(agent, default_tool_ids)

        return self._to_response(agent)

    def _to_response(self, agent) -> AgentResponse:
        return AgentResponse(
            id=agent.id,
            project_id=agent.project_id,
            name=agent.name,
            role_name=agent.role_name,
            system_prompt=agent.system_prompt,
            background_identity=agent.background_identity,
            background_experience=agent.background_experience,
            domain_knowledge=agent.domain_knowledge,
            responsibility=agent.responsibility,
            constraints=agent.constraints,
            model_id=agent.model_id,
            allow_tool_use=agent.allow_tool_use,
            skill_ids=[s.id for s in agent.skills] if agent.skills else [],
            tool_ids=[t.id for t in agent.tools] if agent.tools else [],
            role_template_id=agent.role_template_id,
            description=agent.description,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
        )
