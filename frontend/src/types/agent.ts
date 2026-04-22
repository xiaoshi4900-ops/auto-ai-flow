export interface Agent {
  id: number
  project_id: number
  name: string
  role_name: string
  system_prompt: string | null
  background_identity: string | null
  background_experience: string | null
  domain_knowledge: string | null
  responsibility: string | null
  constraints: string | null
  model_id: number | null
  model_name?: string
  allow_tool_use: boolean
  skill_ids: number[]
  tool_ids: number[]
  created_at: string | null
  updated_at: string | null
}

export interface AgentCreateRequest {
  name: string
  project_id: number
  role_name?: string
  system_prompt?: string
  background_identity?: string
  background_experience?: string
  domain_knowledge?: string
  responsibility?: string
  constraints?: string
  model_id?: number
  allow_tool_use?: boolean
  skill_ids?: number[]
  tool_ids?: number[]
}

export interface AgentUpdateRequest {
  name?: string
  role_name?: string
  system_prompt?: string
  background_identity?: string
  background_experience?: string
  domain_knowledge?: string
  responsibility?: string
  constraints?: string
  model_id?: number
  allow_tool_use?: boolean
}
