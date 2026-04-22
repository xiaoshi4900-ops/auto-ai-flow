from unittest.mock import MagicMock, patch
from app.runtime.model_resolver import ModelResolver
from app.db.models.model import ModelDefinition, ModelProvider
from app.db.models.agent import Agent


def test_node_override_priority():
    resolver = ModelResolver()
    mock_db = MagicMock()
    mock_model = MagicMock(spec=ModelDefinition)
    mock_model.id = 10
    mock_model.model_id = "gpt-4"
    mock_model.provider_id = 1
    mock_provider = MagicMock(spec=ModelProvider)
    mock_provider.provider_type = "openai"
    mock_provider.api_base = None

    def mock_query(model_cls):
        mock_q = MagicMock()
        def mock_filter(*args, **kwargs):
            mock_f = MagicMock()
            mock_f.first.return_value = mock_model if model_cls == ModelDefinition else mock_provider
            return mock_f
        mock_q.filter = mock_filter
        return mock_q

    mock_db.query = mock_query
    result = resolver.resolve(node_model_id=10, db=mock_db)
    assert result is not None
    assert result["model_definition_id"] == 10


def test_agent_model_fallback():
    resolver = ModelResolver()
    mock_db = MagicMock()
    mock_agent = MagicMock(spec=Agent)
    mock_agent.model_id = 20
    mock_model = MagicMock(spec=ModelDefinition)
    mock_model.id = 20
    mock_model.model_id = "gpt-3.5-turbo"
    mock_model.provider_id = 1
    mock_provider = MagicMock(spec=ModelProvider)
    mock_provider.provider_type = "openai"
    mock_provider.api_base = None

    call_count = 0
    def mock_query(model_cls):
        nonlocal call_count
        mock_q = MagicMock()
        def mock_filter(*args, **kwargs):
            nonlocal call_count
            mock_f = MagicMock()
            call_count += 1
            if model_cls == Agent:
                mock_f.first.return_value = mock_agent
            elif model_cls == ModelDefinition:
                mock_f.first.return_value = mock_model
            elif model_cls == ModelProvider:
                mock_f.first.return_value = mock_provider
            else:
                mock_f.first.return_value = None
            return mock_f
        mock_q.filter = mock_filter
        return mock_q

    mock_db.query = mock_query
    result = resolver.resolve(node_model_id=None, agent_id=5, db=mock_db)
    assert result is not None
    assert result["model_id"] == "gpt-3.5-turbo"


def test_no_model_returns_none():
    resolver = ModelResolver()
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = resolver.resolve(node_model_id=None, agent_id=None, project_id=None, db=mock_db)
    assert result is None
