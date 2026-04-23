from app.runtime.prompt_builder import PromptBuildResult
from app.runtime.providers.feature_matrix import resolve_capabilities, resolve_provider_family


class OpenAICompatibleProvider:
    def complete(self, prompt_result: PromptBuildResult, model_config: dict) -> dict:
        from openai import OpenAI

        model_id = model_config["model_id"]
        provider_type = model_config.get("provider_type")
        api_key = model_config.get("api_key")
        api_base = model_config.get("api_base")

        client_kwargs = {}
        if api_key:
            client_kwargs["api_key"] = api_key
        if api_base:
            client_kwargs["base_url"] = api_base

        client = OpenAI(**client_kwargs)
        response = client.chat.completions.create(
            model=model_id,
            temperature=0.7,
            messages=[
                {"role": "system", "content": prompt_result.system_prompt},
                {"role": "user", "content": prompt_result.user_prompt},
            ],
        )

        content = ""
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            content = response.choices[0].message.content

        capabilities = resolve_capabilities(provider_type)
        return {
            "result": content,
            "model": model_id,
            "provider_family": resolve_provider_family(provider_type),
            "capabilities": capabilities.__dict__,
        }
