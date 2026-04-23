from unittest.mock import patch
from app.runtime.agent_runner import AgentRunner
from app.runtime.prompt_builder import PromptBuildResult


def test_agent_runner_with_mock_llm():
    runner = AgentRunner()
    prompt = PromptBuildResult(system_prompt="You are helpful", user_prompt="Hello")
    with patch("app.runtime.providers.openai_compatible.OpenAICompatibleProvider.complete") as mock_complete:
        mock_complete.return_value = {"result": "Hi there!", "model": "gpt-4"}
        result = runner.run(prompt, {"model_id": "gpt-4"})
    assert "result" in result
    assert result["result"] == "Hi there!"


def test_agent_runner_no_tools():
    runner = AgentRunner()
    prompt = PromptBuildResult(system_prompt="You are helpful", user_prompt="Hello")
    with patch("app.runtime.providers.openai_compatible.OpenAICompatibleProvider.complete") as mock_complete:
        mock_complete.return_value = {"result": "No tools needed", "model": "gpt-5.4"}
        result = runner.run(prompt, None)
    assert "result" in result


def test_agent_runner_import_error_fallback():
    runner = AgentRunner()
    prompt = PromptBuildResult(system_prompt="sys", user_prompt="usr")
    with patch("app.runtime.providers.openai_compatible.OpenAICompatibleProvider.complete", side_effect=ImportError("openai missing")):
        result = runner.run(prompt, None)
    assert "result" in result
    assert "stub" in result["result"].lower() or "error" in result["result"].lower() or "not available" in result["result"].lower()
