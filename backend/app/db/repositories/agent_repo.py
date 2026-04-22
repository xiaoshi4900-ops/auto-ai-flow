from sqlalchemy.orm import Session

from app.db.models.agent import Agent
from app.db.models.skill import Skill
from app.db.models.tool import Tool


class AgentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, agent_id: int) -> Agent | None:
        return self.db.query(Agent).filter(Agent.id == agent_id, Agent.is_deleted == False).first()

    def list_by_project(self, project_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Agent], int]:
        query = self.db.query(Agent).filter(Agent.project_id == project_id, Agent.is_deleted == False)
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def create(self, **kwargs) -> Agent:
        agent = Agent(**kwargs)
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        return agent

    def update(self, agent: Agent, **kwargs) -> Agent:
        for key, value in kwargs.items():
            if value is not None and hasattr(agent, key):
                setattr(agent, key, value)
        self.db.commit()
        self.db.refresh(agent)
        return agent

    def bind_skills(self, agent: Agent, skill_ids: list[int]) -> Agent:
        skills = self.db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
        agent.skills = skills
        self.db.commit()
        self.db.refresh(agent)
        return agent

    def bind_tools(self, agent: Agent, tool_ids: list[int]) -> Agent:
        tools = self.db.query(Tool).filter(Tool.id.in_(tool_ids)).all()
        agent.tools = tools
        self.db.commit()
        self.db.refresh(agent)
        return agent

    def soft_delete(self, agent: Agent) -> Agent:
        agent.is_deleted = True
        self.db.commit()
        return agent
