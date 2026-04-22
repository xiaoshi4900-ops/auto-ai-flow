from sqlalchemy.orm import Session

from app.db.models.model import ModelProvider, ModelDefinition, ProjectModelConfig
from app.db.models.project import Project
from app.schemas.model import ModelProviderResponse, ModelDefinitionResponse, ModelListResponse, ProjectModelConfigCreateRequest, ProjectModelConfigResponse
from app.core.exceptions import NotFoundException


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

    def create_project_model_config(self, project_id: int, req: ProjectModelConfigCreateRequest) -> ProjectModelConfigResponse:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException("Project")
        config = ProjectModelConfig(project_id=project_id, model_definition_id=req.model_definition_id, custom_config=req.custom_config, is_default=req.is_default)
        self.db.add(config)
        self.db.commit()
        self.db.refresh(config)
        return ProjectModelConfigResponse.model_validate(config)

    def list_project_model_configs(self, project_id: int) -> list[ProjectModelConfigResponse]:
        configs = self.db.query(ProjectModelConfig).filter(ProjectModelConfig.project_id == project_id).all()
        return [ProjectModelConfigResponse.model_validate(c) for c in configs]
