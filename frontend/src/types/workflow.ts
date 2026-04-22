export interface WorkflowNode {
  node_key: string
  node_type: string
  label: string | null
  config: Record<string, unknown>
  position_x: number | null
  position_y: number | null
}

export interface WorkflowEdge {
  source_node_key: string
  target_node_key: string
  condition: Record<string, unknown> | null
  label: string | null
}

export interface Workflow {
  id: number
  project_id: number
  name: string
  description: string | null
  status?: string
  version?: number
  updated_relative?: string
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
  canvas_data: Record<string, unknown> | null
  created_at: string | null
  updated_at: string | null
}

export interface WorkflowCreateRequest {
  project_id: number
  name: string
  description?: string
  nodes?: WorkflowNode[]
  edges?: WorkflowEdge[]
}

export interface WorkflowUpdateRequest {
  name?: string
  description?: string
  nodes?: WorkflowNode[]
  edges?: WorkflowEdge[]
  canvas_data?: Record<string, unknown>
}
