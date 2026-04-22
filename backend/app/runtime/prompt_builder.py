from pydantic import BaseModel


class PromptBuildResult(BaseModel):
    system_prompt: str
    user_prompt: str
    metadata: dict = {}


class PromptBuilder:
    def build(self, agent_id: int | None = None, task_instruction: str = "", runtime_context=None, extra_input: dict | None = None, agent_config: dict | None = None) -> PromptBuildResult:
        config = agent_config or {}
        system_parts = []
        if config.get("role_name"):
            system_parts.append(f"Role: {config['role_name']}")
        if config.get("background_identity"):
            system_parts.append(f"Identity: {config['background_identity']}")
        if config.get("background_experience"):
            system_parts.append(f"Experience: {config['background_experience']}")
        if config.get("domain_knowledge"):
            system_parts.append(f"Domain Knowledge: {config['domain_knowledge']}")
        if config.get("responsibility"):
            system_parts.append(f"Responsibility: {config['responsibility']}")
        if config.get("constraints"):
            system_parts.append(f"Constraints: {config['constraints']}")
        if config.get("system_prompt"):
            system_parts.append(config["system_prompt"])

        system_prompt = "\n\n".join(system_parts) if system_parts else "You are a helpful AI assistant."

        user_parts = []
        if task_instruction:
            user_parts.append(f"Task: {task_instruction}")
        if extra_input:
            user_parts.append(f"Input Data: {extra_input}")
        if runtime_context and runtime_context.shared_state:
            relevant_state = {k: v for k, v in runtime_context.shared_state.items() if not k.endswith("_handoff")}
            if relevant_state:
                user_parts.append(f"Context: {relevant_state}")

        user_prompt = "\n\n".join(user_parts) if user_parts else "Please process the task."

        return PromptBuildResult(system_prompt=system_prompt, user_prompt=user_prompt, metadata={"agent_id": agent_id})
