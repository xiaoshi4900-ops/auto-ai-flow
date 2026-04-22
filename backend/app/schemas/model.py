from datetime import datetime

from pydantic import BaseModel


class ModelProviderResponse(BaseModel):
    id: int
    name: str
    provider_type: str
    api_base: str | None = None
    is_builtin: bool = False

    model_config = {"from_attributes": True}


class ModelDefinitionResponse(BaseModel):
    id: int
    provider_id: int
    name: str
    model_id: str
    description: str | None = None
    capabilities: dict | None = None
    is_builtin: bool = False

    model_config = {"from_attributes": True}


class ModelListResponse(BaseModel):
    providers: list[ModelProviderResponse]
    models: list[ModelDefinitionResponse]


class ProjectModelConfigCreateRequest(BaseModel):
    model_definition_id: int
    api_key: str | None = None
    custom_config: dict | None = None
    is_default: bool = False


class ProjectModelConfigResponse(BaseModel):
    id: int
    project_id: int
    model_definition_id: int
    is_default: bool = False
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
