from sqlalchemy.orm import Session

from app.db.models.model import ModelDefinition, ModelProvider, ProjectModelConfig
from app.db.models.agent import Agent


class ModelResolver:
    def resolve(self, node_model_id: int | None = None, agent_id: int | None = None, project_id: int | None = None, db: Session | None = None) -> dict | None:
        if db is None:
            from app.db.session import SessionLocal
            db = SessionLocal()

        model_id = node_model_id
        if not model_id and agent_id:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if agent:
                model_id = agent.model_id

        if not model_id and project_id:
            default_config = db.query(ProjectModelConfig).filter(ProjectModelConfig.project_id == project_id, ProjectModelConfig.is_default == True).first()
            if default_config:
                model_id = default_config.model_definition_id

        if not model_id:
            return None

        model_def = db.query(ModelDefinition).filter(ModelDefinition.id == model_id).first()
        if not model_def:
            return None

        provider = db.query(ModelProvider).filter(ModelProvider.id == model_def.provider_id).first()

        return {
            "model_definition_id": model_def.id,
            "model_id": model_def.model_id,
            "provider_type": provider.provider_type if provider else "openai",
            "api_base": provider.api_base if provider else None,
        }
