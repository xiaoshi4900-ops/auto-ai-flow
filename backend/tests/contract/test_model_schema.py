import pytest
from app.schemas.model import ModelProviderResponse, ModelDefinitionResponse


def test_model_provider_response_fields():
    resp = ModelProviderResponse(id=1, name="OpenAI", provider_type="openai")
    dumped = resp.model_dump()
    assert "id" in dumped
    assert "name" in dumped
    assert "provider_type" in dumped


def test_model_definition_response_fields():
    resp = ModelDefinitionResponse(id=1, model_id="gpt-4", provider_id=1, name="GPT-4")
    dumped = resp.model_dump()
    assert "model_id" in dumped
    assert "provider_id" in dumped
    assert "name" in dumped
