# Execution Architecture v1.3

## Goal

AutoAiFlow should not compete with a single model runtime.

Its value is:

1. workflow orchestration
2. task/state persistence
3. operator control and review points
4. unified execution protocol across multiple model backends

This means the platform must own the outer shell and treat the inner AI engine
as a replaceable backend.

## Architecture Decision

### Platform-Owned Layer

The platform keeps ownership of:

- workflow graph topology
- run and node-run lifecycle
- runtime context merge rules
- condition routing
- execution logs and artifacts
- operator-visible status and handoff payloads

Current examples:

- `backend/app/runtime/workflow_executor.py`
- `backend/app/runtime/executors/agent_node.py`

These files remain the outer orchestration layer and are not replaced by a
framework runtime.

### Executor-Owned Layer

The executor backend owns only the inner task execution of one node, such as:

- normal agent completion
- code-task iterative loop
- tool use within one node
- structured result production
- provider-specific request formatting

The executor backend must not own:

- workflow graph traversal
- cross-node state merge
- project-level run persistence
- page/API contract decisions

## Required Runtime Split

Execution code must be split into four layers.

### 1. Task Runtime

This is the outer shell.

Responsibilities:

- select current node
- prepare runtime context
- call executor backend
- persist node result
- route next node
- stop or fail the run

### 2. Executor Interface

This is the stable internal contract.

Each executor implementation must accept:

- task goal
- instructions
- runtime context
- tool registry
- model configuration
- policy configuration

Each executor implementation must return:

- status
- plain result
- structured output
- tool call trace
- usage if available
- failure reason if failed
- handoff payload

The outer runtime must depend on this interface, not on a concrete framework.

### 3. Provider Adapter

This converts model configuration into provider-specific calls.

Initial policy for v1.3:

- all providers are treated as `openai_native` or `openai_compatible`
- the first implementation path targets `openai_compatible`
- provider-specific SDKs are optional future optimizations, not a prerequisite

### 4. Feature Matrix

Every provider/model route must declare capabilities explicitly.

No runtime path may assume that all providers support:

- tool calling
- structured output
- reasoning fields
- tracing
- usage accounting
- vision

## Backend Modes

v1.3 defines three backend modes.

### `direct_high_tier`

Used when a high-end model directly performs the task.

Typical use:

- complex coding task
- lower orchestration depth
- higher quality expectation

### `openai_compatible_agent`

Used when one provider exposes an OpenAI-compatible API.

Typical use:

- Zhipu
- DeepSeek
- Kimi
- OpenAI-compatible gateways

This is the default backend mode in v1.3.

### `deterministic_runner`

Used for non-LLM or script-driven execution.

Typical use:

- static transforms
- schema checks
- fixed rule pipelines

## Framework Decision

### What Not To Do

The project must not hand the whole workflow runtime to:

- LangChain agents
- OpenAI Agents SDK
- any provider-specific multi-agent runtime

Reason:

- AutoAiFlow already owns the outer state machine
- replacing outer orchestration would duplicate lifecycle logic
- DB run records and graph routing would become framework-coupled

### What To Do

Frameworks may be used only inside one executor backend.

Allowed examples:

- use OpenAI SDK inside one executor
- use OpenAI Agents SDK inside the code-task loop only
- use a custom OpenAI-compatible adapter for normal agent nodes

## Current Migration Direction

### Phase 1

Keep outer runtime unchanged and remove unnecessary framework dependence.

Actions:

- preserve `WorkflowExecutor`
- preserve `AgentNodeExecutor`
- keep `CodeSkillRunner` contract shape
- replace the thin LangChain wrapper with a provider adapter path

### Phase 2

Introduce a real executor interface for inner-loop execution.

Actions:

- normal agent executor
- code runtime executor
- optional high-tier direct executor

### Phase 3

Add provider capability declarations and downgrade logic.

Actions:

- capability flags on provider/model route
- conditional tool usage
- conditional structured output
- tracing disabled by default for non-OpenAI providers

## Hard Rules

1. outer workflow state remains project-owned
2. all provider access must pass through model config plus adapter logic
3. feature support must be capability-checked before use
4. `openai_compatible` is the default provider path in v1.3
5. framework choice must stay behind the executor interface

## Recommended Code Targets

The first refactor wave should center on:

- `backend/app/runtime/agent_runner.py`
- `backend/app/runtime/normal_agent_runner.py`
- `backend/app/runtime/code_skill_runner.py`
- `backend/app/runtime/model_resolver.py`

Possible new files:

- `backend/app/runtime/executors/base_executor.py`
- `backend/app/runtime/providers/openai_compatible.py`
- `backend/app/runtime/providers/feature_matrix.py`

## Non-Goals In v1.3

These are explicitly out of scope for the first v1.3 pass:

- provider-specific bespoke SDK support for every vendor
- multi-provider perfect parity
- replacing workflow graph traversal
- replacing run persistence contracts
- replacing page/API packet system in `spec-v2`
