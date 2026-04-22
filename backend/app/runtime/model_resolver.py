from sqlalchemy.orm import Session

from app.db.models.model import ModelDefinition, ModelProvider, ProjectModelConfig
from app.db.models.agent import Agent
from app.utils.crypto import decrypt_api_key


class ModelResolver:
    def resolve(self, node_model_id: int | None = None, agent_id: int | None = None, project_id: int | None = None, db: Session | None = None) -> dict | None:
        if db is None:
            from app.db.session import SessionLocal
            db = SessionLocal()

        # Priority: node override -> agent-bound model -> project default model.
        model_id = node_model_id
        selected_config: ProjectModelConfig | None = None
        if not model_id and agent_id:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if agent:
                model_id = agent.model_id

        if project_id and model_id:
            selected_config = (
                db.query(ProjectModelConfig)
                .filter(ProjectModelConfig.project_id == project_id, ProjectModelConfig.model_definition_id == model_id)
                .order_by(ProjectModelConfig.is_default.desc(), ProjectModelConfig.id.desc())
                .first()
            )

        if not model_id and project_id:
            selected_config = (
                db.query(ProjectModelConfig)
                .filter(ProjectModelConfig.project_id == project_id, ProjectModelConfig.is_default == True)
                .first()
            )
            if selected_config:
                model_id = selected_config.model_definition_id

        if not model_id:
            return None

        model_def = db.query(ModelDefinition).filter(ModelDefinition.id == model_id).first()
        if not model_def:
            return None

        provider = db.query(ModelProvider).filter(ModelProvider.id == model_def.provider_id).first()
        # Project model config may carry runtime overrides for vendor compatibility.
        custom = selected_config.custom_config if selected_config and isinstance(selected_config.custom_config, dict) else {}
        api_base_override = custom.get("api_base_url") or custom.get("api_base")
        model_id_override = custom.get("model_id")
        provider_type_override = custom.get("provider_type")
        api_key = None
        if selected_config and selected_config.api_key_encrypted:
            api_key = decrypt_api_key(selected_config.api_key_encrypted) or None

        return {
            "model_definition_id": model_def.id,
            "model_id": model_id_override or model_def.model_id,
            "provider_type": provider_type_override or (provider.provider_type if provider else "openai"),
            "api_base": api_base_override or (provider.api_base if provider else None),
            "api_key": api_key,
        }
