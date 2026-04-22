import importlib


def test_builtin_role_templates_contains_required_keys():
    mod = importlib.import_module("app.seeds.builtin_role_templates")
    templates = mod.get_builtin_role_templates()
    keys = {item["key"] for item in templates}
    assert {"generic_assistant", "product_manager", "backend_engineer", "frontend_engineer", "fullstack_engineer", "research_analyst"}.issubset(keys)


def test_backend_engineer_default_mode_is_code_runtime():
    mod = importlib.import_module("app.seeds.builtin_role_templates")
    templates = mod.get_builtin_role_templates()
    backend = next(item for item in templates if item["key"] == "backend_engineer")
    assert backend["execution_mode"] == "code_runtime"


def test_seed_role_templates_is_idempotent(db):
    seed_mod = importlib.import_module("app.seeds.seed_runner")
    role_tpl_mod = importlib.import_module("app.db.models.role_template")
    seed_mod.seed_builtin_role_templates(db)
    seed_mod.seed_builtin_role_templates(db)
    rows = db.query(role_tpl_mod.RoleTemplate).all()
    keys = [item.key for item in rows]
    assert len(keys) == len(set(keys))
