from app.runtime.prompt_builder import PromptBuildResult


class AgentRunner:
    def run(self, prompt_result: PromptBuildResult, model_config: dict | None = None) -> dict:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage

            model_id = "gpt-3.5-turbo"
            api_base = None
            api_key = None

            if model_config:
                model_id = model_config.get("model_id", model_id)
                api_base = model_config.get("api_base")

            from app.core.config import settings
            api_key = settings.OPENAI_API_KEY or None

            llm = ChatOpenAI(model=model_id, openai_api_base=api_base, openai_api_key=api_key, temperature=0.7)
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
