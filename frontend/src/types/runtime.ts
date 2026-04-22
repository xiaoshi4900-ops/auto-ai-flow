export interface RuntimeContext {
  input: Record<string, unknown>
  shared_state: Record<string, unknown>
  node_outputs: Record<string, unknown>
  artifacts: Record<string, unknown>
  messages: Record<string, unknown>
  meta: Record<string, unknown>
}

export interface StructuredOutput {
  status: 'success' | 'failed'
  structured_output: Record<string, unknown>
  artifact_refs: Record<string, unknown>[]
  next_suggestion: Record<string, unknown>
}

export interface HandoffPayload {
  handoff_summary: string
  assumptions: string[]
  risks: string[]
  questions_for_next_node: string[]
}
