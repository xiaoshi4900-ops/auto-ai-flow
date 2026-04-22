from app.runtime.prompt_builder import PromptBuildResult


class AgentRunner:
    def run(self, prompt_result: PromptBuildResult, model_config: dict | None = None) -> dict:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage

            # Safe defaults when no model resolution is available.
            # Keep this aligned with current seeded baseline models.
            model_id = "gpt-5.4"
            api_base = None
            api_key = None

            if model_config:
                # model_config comes from ModelResolver, possibly enriched by project custom_config.
                model_id = model_config.get("model_id", model_id)
                api_base = model_config.get("api_base")
                api_key = model_config.get("api_key")

            from app.core.config import settings
            # Fallback to global key only when project-level key is not configured.
            if not api_key:
                api_key = settings.OPENAI_API_KEY or None

            kwargs = {"model": model_id, "temperature": 0.7}
            if api_base:
                kwargs["openai_api_base"] = api_base
            if api_key:
                kwargs["openai_api_key"] = api_key
            llm = ChatOpenAI(**kwargs)
            # Keep message structure explicit to make prompt composition easy to audit.
            messages = [
                SystemMessage(content=prompt_result.system_prompt),
                HumanMessage(content=prompt_result.user_prompt),
            ]
            response = llm.invoke(messages)
            return {"result": response.content, "model": model_id}
        except ImportError:
            return {"result": "LangChain not available - stub response", "model": "stub"}
        except Exception as e:
            return {"result": f"Agent execution error: {str(e)}", "model": "error"}
