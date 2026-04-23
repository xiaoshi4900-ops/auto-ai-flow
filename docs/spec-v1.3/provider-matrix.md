# Provider Matrix v1.3

## Goal

Providers must be integrated by capability, not by marketing name.

v1.3 therefore classifies providers into two protocol families first, and only
then considers vendor-specific behavior.

## Protocol Families

### `openai_native`

Definition:

- official OpenAI endpoints
- OpenAI SDK native path
- highest confidence for full platform features

### `openai_compatible`

Definition:

- OpenAI-like API surface
- custom `base_url`
- provider-specific behavior hidden behind a compatible request shape

Examples likely to fit this family:

- Zhipu
- DeepSeek
- Kimi
- compatible gateways and proxy layers

## Default Policy

For v1.3, all non-OpenAI model integrations must first be treated as
`openai_compatible`.

The project must not assume vendor-specific SDK use unless one of these is true:

1. the compatible path cannot deliver required features
2. the vendor SDK materially improves stability
3. the vendor exposes capabilities unavailable through the compatible path

## Capability Fields

Each provider route must declare at least these flags:

- `supports_tools`
- `supports_structured_output`
- `supports_reasoning`
- `supports_streaming`
- `supports_vision`
- `supports_usage`
- `supports_tracing`

Optional flags:

- `supports_parallel_tool_calls`
- `supports_json_schema`
- `supports_system_prompt`

## Required Degrade Rules

### Tool Calling

If `supports_tools` is false:

- the executor must disable tool planning
- the node may fall back to plain text generation
- the run log must record that tools were disabled by capability

### Structured Output

If `supports_structured_output` is false:

- do not force schema-mode output
- use plain text plus post-parse fallback
- mark the result as downgraded

### Tracing

If `supports_tracing` is false:

- disable tracing by default
- do not treat missing traces as runtime failure

### Usage

If `supports_usage` is false:

- usage fields remain optional
- dashboards must not fake token data

## Recommended Initial Matrix

### OpenAI

- protocol family: `openai_native`
- role in v1.3: reference implementation
- expected support: all primary capabilities

### Zhipu

- protocol family: `openai_compatible`
- role in v1.3: first non-OpenAI target
- expected support: completion, tools, structured output must be verified by tests

### DeepSeek

- protocol family: `openai_compatible`
- role in v1.3: second target
- expected support: treat as compatible but not identical

### Other Domestic Providers

- protocol family: `openai_compatible`
- role in v1.3: future integrations through the same adapter path

## Integration Order

1. OpenAI reference path
2. Zhipu through `openai_compatible`
3. DeepSeek through `openai_compatible`
4. others only after the adapter path is stable

## Testing Rule

A provider is not considered supported only because requests succeed.

Support must be confirmed separately for:

1. plain completion
2. tool call roundtrip
3. structured output stability
4. usage field handling
5. failure-mode degrade behavior

## Product Rule

UI and workflow configuration must expose provider identity and model id, but the
runtime must choose behavior from capability flags instead of hard-coded vendor
conditions whenever possible.
