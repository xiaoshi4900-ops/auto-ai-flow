from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCapabilities:
    supports_tools: bool
    supports_structured_output: bool
    supports_reasoning: bool
    supports_streaming: bool
    supports_vision: bool
    supports_usage: bool
    supports_tracing: bool


OPENAI_NATIVE_CAPABILITIES = ProviderCapabilities(
    supports_tools=True,
    supports_structured_output=True,
    supports_reasoning=True,
    supports_streaming=True,
    supports_vision=True,
    supports_usage=True,
    supports_tracing=True,
)

OPENAI_COMPATIBLE_CAPABILITIES = ProviderCapabilities(
    supports_tools=True,
    supports_structured_output=True,
    supports_reasoning=False,
    supports_streaming=True,
    supports_vision=False,
    supports_usage=False,
    supports_tracing=False,
)


def resolve_provider_family(provider_type: str | None) -> str:
    provider = (provider_type or "").strip().lower()
    return "openai_native" if provider in {"openai"} else "openai_compatible"


def resolve_capabilities(provider_type: str | None) -> ProviderCapabilities:
    family = resolve_provider_family(provider_type)
    if family == "openai_native":
        return OPENAI_NATIVE_CAPABILITIES
    return OPENAI_COMPATIBLE_CAPABILITIES
