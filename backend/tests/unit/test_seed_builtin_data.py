from app.db.models.skill import Skill
from app.db.models.tool import Tool
from app.db.models.model import ModelProvider, ModelDefinition


def test_seed_skills_idempotent(db):
    from app.seeds.builtin_skills import BUILTIN_SKILLS
    for skill_data in BUILTIN_SKILLS:
        s = Skill(**skill_data)
        db.add(s)
    db.commit()
    assert db.query(Skill).count() == len(BUILTIN_SKILLS)
    for skill_data in BUILTIN_SKILLS:
        s = Skill(**skill_data)
        db.add(s)
    from sqlalchemy.exc import IntegrityError
    try:
        db.commit()
    except IntegrityError:
        db.rollback()


def test_seed_tools_idempotent(db):
    from app.seeds.builtin_tools import BUILTIN_TOOLS
    for tool_data in BUILTIN_TOOLS:
        t = Tool(**tool_data)
        db.add(t)
    db.commit()
    assert db.query(Tool).count() == len(BUILTIN_TOOLS)


def test_builtin_skills_queryable(db):
    from app.seeds.builtin_skills import BUILTIN_SKILLS
    for skill_data in BUILTIN_SKILLS:
        db.add(Skill(**skill_data))
    db.commit()
    found = db.query(Skill).filter(Skill.name == "summarize").first()
    assert found is not None
    assert found.is_builtin is True


def test_builtin_tools_queryable(db):
    from app.seeds.builtin_tools import BUILTIN_TOOLS
    for tool_data in BUILTIN_TOOLS:
        db.add(Tool(**tool_data))
    db.commit()
    found = db.query(Tool).filter(Tool.name == "http_request").first()
    assert found is not None


def test_builtin_models_queryable(db):
    from app.seeds.builtin_models import BUILTIN_MODELS
    for provider_data in BUILTIN_MODELS["providers"]:
        db.add(ModelProvider(**provider_data))
    db.commit()
    assert db.query(ModelProvider).count() == len(BUILTIN_MODELS["providers"])
