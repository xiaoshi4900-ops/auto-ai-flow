def resolve_execution_mode(node_config: dict, skill: dict | None = None, role_template: dict | None = None) -> str:
    force = node_config.get("force_execution_mode")
    if force:
        return force

    if skill and skill.get("execution_mode"):
        return skill["execution_mode"]

    if role_template and role_template.get("execution_mode"):
        return role_template["execution_mode"]

    return "normal_llm"
