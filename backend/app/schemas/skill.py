from datetime import datetime

from pydantic import BaseModel


class SkillResponse(BaseModel):
    id: int
    name: str
    skill_key: str | None = None
    description: str | None = None
    prompt_template: str | None = None
    execution_mode: str | None = None
    is_builtin: bool = False
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class SkillListResponse(BaseModel):
    total: int
    items: list[SkillResponse]
