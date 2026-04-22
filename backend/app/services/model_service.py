from sqlalchemy.orm import Session

from app.db.models.model import ModelProvider, ModelDefinition, ProjectModelConfig
from app.db.models.project import Project
from app.schemas.model import (
    ModelProviderResponse,
    ModelDefinitionResponse,
    ModelListResponse,
    ModelProviderCreateRequest,
    ModelDefinitionCreateRequest,
    ProjectModelConfigCreateRequest,
    ProjectModelConfigResponse,
)
from app.core.exceptions import NotFoundException, ConflictException
from app.utils.crypto import encrypt_api_key


class ModelService:
    def __init__(self, db: Session):
        self.db = db

    def list_models(self) -> ModelListResponse:
        providers = self.db.query(ModelProvider).all()
        models = self.db.query(ModelDefinition).all()
        return ModelListResponse(
            providers=[ModelProviderResponse.model_validate(p) for p in providers],
            models=[ModelDefinitionResponse.model_validate(m) for m in models],
        )

    def create_provider(self, req: ModelProviderCreateRequest) -> ModelProviderResponse:
        existing = self.db.query(ModelProvider).filter(ModelProvider.name == req.name).first()
        if existing:
            raise ConflictException("Model provider already exists")
        provider = ModelProvider(
            name=req.name,
            provider_type=req.provider_type,
            api_base=req.api_base,
            is_builtin=False,
        )
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return ModelProviderResponse.model_validate(provider)

    def create_model_definition(self, req: ModelDefinitionCreateRequest) -> ModelDefinitionResponse:
        provider = self.db.query(ModelProvider).filter(ModelProvider.id == req.provider_id).first()
        if not provider:
            raise NotFoundException("ModelProvider")
        existing = (
            self.db.query(ModelDefinition)
            .filter(ModelDefinition.provider_id == req.provider_id, ModelDefinition.model_id == req.model_id)
            .first()
        )
        if existing:
            raise ConflictException("Model definition already exists for provider")
        model = ModelDefinition(
            provider_id=req.provider_id,
            name=req.name,
            model_id=req.model_id,
            description=req.description,
            capabilities=req.capabilities,
            is_builtin=False,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return ModelDefinitionResponse.model_validate(model)

    def create_project_model_config(self, project_id: int, req: ProjectModelConfigCreateRequest) -> ProjectModelConfigResponse:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException("Project")
        encrypted_key = encrypt_api_key(req.api_key) if req.api_key else None
        config = ProjectModelConfig(
            project_id=project_id,
            model_definition_id=req.model_definition_id,
            api_key_encrypted=encrypted_key,
            custom_config=req.custom_config,
            is_default=req.is_default,
        )
        self.db.add(config)
        self.db.commit()
        self.db.refresh(config)
        return ProjectModelConfigResponse(
            id=config.id,
            project_id=config.project_id,
            model_definition_id=config.model_definition_id,
            custom_config=config.custom_config,
            has_api_key=bool(config.api_key_encrypted),
            is_default=config.is_default,
            created_at=config.created_at,
        )

    def list_project_model_configs(self, project_id: int) -> list[ProjectModelConfigResponse]:
        configs = self.db.query(ProjectModelConfig).filter(ProjectModelConfig.project_id == project_id).all()
        return [
            ProjectModelConfigResponse(
                id=c.id,
                project_id=c.project_id,
                model_definition_id=c.model_definition_id,
                custom_config=c.custom_config,
                has_api_key=bool(c.api_key_encrypted),
                is_default=c.is_default,
                created_at=c.created_at,
            )
            for c in configs
        ]
