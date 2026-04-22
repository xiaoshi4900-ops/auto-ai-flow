from app.runtime.prompt_builder import PromptBuilder
from app.schemas.runtime import RuntimeContextSchema


def test_prompt_includes_system_prompt():
    builder = PromptBuilder()
    result = builder.build(agent_config={"system_prompt": "You are an expert."})
    assert "You are an expert." in result.system_prompt


def test_prompt_includes_task_instruction():
    builder = PromptBuilder()
    result = builder.build(task_instruction="Summarize the text")
    assert "Summarize the text" in result.user_prompt


def test_prompt_includes_context_input():
    builder = PromptBuilder()
    ctx = RuntimeContextSchema(shared_state={"prev_result": "data"})
    result = builder.build(runtime_context=ctx)
    assert "prev_result" in result.user_prompt


def test_prompt_default_system():
    builder = PromptBuilder()
    result = builder.build()
    assert "helpful" in result.system_prompt.lower() or result.system_prompt != ""


def test_prompt_includes_agent_fields():
    builder = PromptBuilder()
    result = builder.build(agent_config={
        "role_name": "Analyst",
        "background_identity": "Financial expert",
        "responsibility": "Analyze data",
    })
    assert "Analyst" in result.system_prompt
    assert "Financial expert" in result.system_prompt
    assert "Analyze data" in result.system_prompt
