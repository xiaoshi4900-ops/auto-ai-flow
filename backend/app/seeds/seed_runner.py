import json

from sqlalchemy.orm import Session

from app.db.models.model import ModelDefinition, ModelProvider
from app.db.models.role_template import RoleTemplate
from app.db.models.skill import Skill
from app.db.models.tool import Tool
from app.db.session import SessionLocal
from app.seeds.builtin_models import BUILTIN_MODELS
from app.seeds.builtin_role_templates import get_builtin_role_templates
from app.seeds.builtin_skills import BUILTIN_SKILLS
from app.seeds.builtin_tools import BUILTIN_TOOLS


def seed_builtin_role_templates(db: Session) -> None:
    templates = get_builtin_role_templates()
    for tpl_data in templates:
        existing = db.query(RoleTemplate).filter(RoleTemplate.key == tpl_data["key"]).first()
        if existing:
            continue
        tpl = RoleTemplate(
            key=tpl_data["key"],
            name=tpl_data["name"],
            category=tpl_data.get("category"),
            description=tpl_data.get("description"),
            execution_mode=tpl_data["execution_mode"],
            default_role_name=tpl_data.get("default_role_name"),
            default_skill_ids=json.dumps(tpl_data.get("default_skill_ids", [])),
            default_tool_ids=json.dumps(tpl_data.get("default_tool_ids", [])),
            policy_config=json.dumps(tpl_data.get("policy_config", {})),
            is_builtin=True,
            enabled=True,
        )
        db.add(tpl)
    db.commit()


def seed_builtin_skills(db: Session) -> None:
    for item in BUILTIN_SKILLS:
        existing = db.query(Skill).filter(Skill.name == item["name"]).first()
        if existing:
            continue
        db.add(
            Skill(
                name=item["name"],
                description=item.get("description"),
                prompt_template=item.get("prompt_template"),
                execution_mode=item.get("execution_mode"),
                is_builtin=bool(item.get("is_builtin", True)),
            )
        )
    db.commit()


def seed_builtin_tools(db: Session) -> None:
    for item in BUILTIN_TOOLS:
        existing = db.query(Tool).filter(Tool.name == item["name"]).first()
        if existing:
            continue
        db.add(
            Tool(
                name=item["name"],
                description=item.get("description"),
                tool_type=item.get("tool_type", "function"),
                config=item.get("config"),
                is_builtin=bool(item.get("is_builtin", True)),
            )
        )
    db.commit()


def seed_builtin_models(db: Session) -> None:
    provider_by_name: dict[str, ModelProvider] = {}
    for provider in BUILTIN_MODELS.get("providers", []):
        name = provider["name"]
        existing = db.query(ModelProvider).filter(ModelProvider.name == name).first()
        if existing:
            provider_by_name[name] = existing
            continue
        created = ModelProvider(
            name=name,
            provider_type=provider["provider_type"],
            api_base=provider.get("api_base"),
            is_builtin=bool(provider.get("is_builtin", True)),
        )
        db.add(created)
        db.flush()
        provider_by_name[name] = created

    for model in BUILTIN_MODELS.get("models", []):
        provider_name = model["provider_name"]
        provider = provider_by_name.get(provider_name) or db.query(ModelProvider).filter(ModelProvider.name == provider_name).first()
        if not provider:
            continue
        existing = (
            db.query(ModelDefinition)
            .filter(
                ModelDefinition.provider_id == provider.id,
                ModelDefinition.model_id == model["model_id"],
            )
            .first()
        )
        if existing:
            continue
        db.add(
            ModelDefinition(
                provider_id=provider.id,
                name=model["name"],
                model_id=model["model_id"],
                description=model.get("description"),
                capabilities=model.get("capabilities"),
                is_builtin=True,
            )
        )
    db.commit()


def seed_all() -> None:
    db = SessionLocal()
    try:
        seed_builtin_role_templates(db)
        seed_builtin_skills(db)
        seed_builtin_tools(db)
        seed_builtin_models(db)
    finally:
        db.close()
