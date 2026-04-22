import json

from app.db.models.role_template import RoleTemplate
from app.seeds.builtin_role_templates import get_builtin_role_templates


def seed_builtin_role_templates(db):
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
