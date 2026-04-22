from datetime import datetime

from pydantic import BaseModel


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None
    default_model_id: int | None = None


class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    default_model_id: int | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    default_model_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    total: int
    items: list[ProjectResponse]
