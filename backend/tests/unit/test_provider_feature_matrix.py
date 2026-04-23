from app.runtime.providers.feature_matrix import resolve_capabilities, resolve_provider_family


def test_resolve_provider_family_openai_native():
    assert resolve_provider_family("openai") == "openai_native"


def test_resolve_provider_family_openai_compatible_default():
    assert resolve_provider_family("zhipu") == "openai_compatible"
    assert resolve_provider_family(None) == "openai_compatible"


def test_openai_native_capabilities_include_tracing():
    caps = resolve_capabilities("openai")
    assert caps.supports_tools is True
    assert caps.supports_tracing is True


def test_openai_compatible_capabilities_disable_tracing_by_default():
    caps = resolve_capabilities("deepseek")
    assert caps.supports_tools is True
    assert caps.supports_tracing is False
