from datetime import datetime

from pydantic import BaseModel


class AgentCreateRequest(BaseModel):
    name: str
    project_id: int
    role_name: str = "assistant"
    system_prompt: str | None = None
    background_identity: str | None = None
    background_experience: str | None = None
    domain_knowledge: str | None = None
    responsibility: str | None = None
    constraints: str | None = None
    model_id: int | None = None
    allow_tool_use: bool = False
    skill_ids: list[int] | None = None
    tool_ids: list[int] | None = None
    role_template_id: int | None = None
    description: str | None = None


class AgentUpdateRequest(BaseModel):
    name: str | None = None
    role_name: str | None = None
    system_prompt: str | None = None
    background_identity: str | None = None
    background_experience: str | None = None
    domain_knowledge: str | None = None
    responsibility: str | None = None
    constraints: str | None = None
    model_id: int | None = None
    allow_tool_use: bool | None = None
    role_template_id: int | None = None


class AgentSkillBindRequest(BaseModel):
    skill_ids: list[int]


class AgentToolBindRequest(BaseModel):
    tool_ids: list[int]


class AgentResponse(BaseModel):
    id: int
    project_id: int
    name: str
    role_name: str
    system_prompt: str | None = None
    background_identity: str | None = None
    background_experience: str | None = None
    domain_knowledge: str | None = None
    responsibility: str | None = None
    constraints: str | None = None
    model_id: int | None = None
    allow_tool_use: bool = False
    skill_ids: list[int] = []
    tool_ids: list[int] = []
    role_template_id: int | None = None
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class AgentListResponse(BaseModel):
    total: int
    items: list[AgentResponse]
