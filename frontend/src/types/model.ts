export interface ModelProvider {
  id: number
  name: string
  provider_type: string
  api_base_url: string | null
  is_active: boolean
}

export interface ModelDefinition {
  id: number
  provider_id: number
  model_name: string
  display_name: string
  model_type: string
  context_window: number
  is_active: boolean
}

export interface ProjectModelConfig {
  id: number
  project_id: number
  model_definition_id: number
  custom_config: Record<string, unknown> | null
  is_default: boolean
}

export interface ModelListResponse {
  providers: ModelProvider[]
  models: ModelDefinition[]
}

export interface ProjectModelConfigCreateRequest {
  model_definition_id: number
  custom_config?: Record<string, unknown>
  is_default?: boolean
}
