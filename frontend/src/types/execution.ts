export interface ExecutionTriggerRequest {
  workflow_id: number
  input_payload?: Record<string, unknown>
}

export interface ExecutionTriggerResponse {
  run_id: number
  status: string
  message: string
}

export interface Run {
  id: number
  workflow_id: number
  status: string
  input_payload: Record<string, unknown> | null
  output_payload: Record<string, unknown> | null
  error_message: string | null
  started_at: string | null
  finished_at: string | null
  created_at: string | null
  latency_ms?: number
  token_usage_total?: number
}

export interface NodeRun {
  id: number
  workflow_run_id: number
  node_key: string
  node_type: string
  status: string
  input_data: Record<string, unknown> | null
  output_data: Record<string, unknown> | null
  error_message: string | null
  started_at: string | null
  finished_at: string | null
  duration_ms: number | null
}

export interface RunDetail {
  run: Run
  node_runs: NodeRun[]
}
