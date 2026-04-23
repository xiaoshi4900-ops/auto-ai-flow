from app.runtime.prompt_builder import PromptBuildResult
from app.runtime.providers.openai_compatible import OpenAICompatibleProvider


class AgentRunner:
    def __init__(self):
        self.provider = OpenAICompatibleProvider()

    def run(self, prompt_result: PromptBuildResult, model_config: dict | None = None) -> dict:
        # Safe defaults when no model resolution is available.
        # Keep this aligned with current seeded baseline models.
        model_id = "gpt-5.4"
        api_base = None
        api_key = None
        provider_type = "openai"

        if model_config:
            # model_config comes from ModelResolver, possibly enriched by project custom_config.
            model_id = model_config.get("model_id", model_id)
            api_base = model_config.get("api_base")
            api_key = model_config.get("api_key")
            provider_type = model_config.get("provider_type", provider_type)

        from app.core.config import settings
        # Fallback to global key only when project-level key is not configured.
        if not api_key:
            api_key = settings.OPENAI_API_KEY or None

        try:
            return self.provider.complete(
                prompt_result=prompt_result,
                model_config={
                    "model_id": model_id,
                    "provider_type": provider_type,
                    "api_base": api_base,
                    "api_key": api_key,
                },
            )
        except ImportError:
            return {"result": "OpenAI SDK not available - executor stub response", "model": "stub"}
        except Exception as e:
            return {"result": f"Agent execution error: {str(e)}", "model": "error"}
