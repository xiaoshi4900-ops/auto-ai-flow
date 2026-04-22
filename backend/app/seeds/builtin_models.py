BUILTIN_MODELS = {
    "providers": [
        {"name": "OpenAI", "provider_type": "openai", "api_base": "https://api.openai.com/v1", "is_builtin": True},
        {"name": "Azure OpenAI", "provider_type": "azure_openai", "api_base": "", "is_builtin": True},
        {"name": "Anthropic", "provider_type": "anthropic", "api_base": "https://api.anthropic.com", "is_builtin": True},
    ],
    "models": [
        {"provider_name": "OpenAI", "name": "GPT-4o", "model_id": "gpt-4o", "description": "Most capable OpenAI model", "capabilities": {"vision": True, "function_calling": True}},
        {"provider_name": "OpenAI", "name": "GPT-4o-mini", "model_id": "gpt-4o-mini", "description": "Fast and affordable", "capabilities": {"vision": True, "function_calling": True}},
        {"provider_name": "OpenAI", "name": "GPT-3.5 Turbo", "model_id": "gpt-3.5-turbo", "description": "Legacy fast model", "capabilities": {"function_calling": True}},
        {"provider_name": "Anthropic", "name": "Claude 3.5 Sonnet", "model_id": "claude-3-5-sonnet-20241022", "description": "Balanced performance", "capabilities": {"vision": True}},
    ],
}
