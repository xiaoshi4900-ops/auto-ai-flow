from datetime import datetime

from pydantic import BaseModel


class ToolResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    tool_type: str = "function"
    config: str | None = None
    is_builtin: bool = False
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ToolListResponse(BaseModel):
    total: int
    items: list[ToolResponse]
