export interface Project {
  id: number
  name: string
  description: string | null
  owner_id: number
  default_model_id: number | null
  default_model_name?: string
  status?: string
  updated_relative?: string
  created_at: string | null
  updated_at: string | null
}

export interface ProjectCreateRequest {
  name: string
  description?: string
  default_model_id?: number
}

export interface ProjectUpdateRequest {
  name?: string
  description?: string
  default_model_id?: number
}
