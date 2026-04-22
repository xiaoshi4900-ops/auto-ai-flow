from unittest.mock import MagicMock, patch
from app.runtime.agent_runner import AgentRunner
from app.runtime.prompt_builder import PromptBuildResult


def test_agent_runner_with_mock_llm():
    runner = AgentRunner()
    prompt = PromptBuildResult(system_prompt="You are helpful", user_prompt="Hello")
    with patch("langchain_openai.ChatOpenAI") as mock_llm_cls:
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Hi there!"
        mock_llm.invoke.return_value = mock_response
        mock_llm_cls.return_value = mock_llm
        result = runner.run(prompt, {"model_id": "gpt-4"})
    assert "result" in result
    assert result["result"] == "Hi there!"


def test_agent_runner_no_tools():
    runner = AgentRunner()
    prompt = PromptBuildResult(system_prompt="You are helpful", user_prompt="Hello")
    with patch("langchain_openai.ChatOpenAI") as mock_llm_cls:
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "No tools needed"
        mock_llm.invoke.return_value = mock_response
        mock_llm_cls.return_value = mock_llm
        result = runner.run(prompt, None)
    assert "result" in result


def test_agent_runner_import_error_fallback():
    runner = AgentRunner()
    prompt = PromptBuildResult(system_prompt="sys", user_prompt="usr")
    with patch.dict("sys.modules", {"langchain_openai": None, "langchain_core": None, "langchain_core.messages": None}):
        result = runner.run(prompt, None)
    assert "result" in result
    assert "stub" in result["result"].lower() or "error" in result["result"].lower() or "not available" in result["result"].lower()
