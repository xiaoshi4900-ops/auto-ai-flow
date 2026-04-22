export interface ModelProvider {
  id: number
  name: string
  provider_type: string
  api_base: string | null
  is_builtin: boolean
}

export interface ModelDefinition {
  id: number
  provider_id: number
  name: string
  model_id: string
  description: string | null
  capabilities: Record<string, unknown> | null
  is_builtin: boolean
}

export interface ProjectModelConfig {
  id: number
  project_id: number
  model_definition_id: number
  custom_config?: Record<string, unknown> | null
  has_api_key?: boolean
  is_default: boolean
  created_at?: string | null
}

export interface ModelListResponse {
  providers: ModelProvider[]
  models: ModelDefinition[]
}

export interface ModelProviderCreateRequest {
  name: string
  provider_type: string
  api_base?: string | null
}

export interface ModelDefinitionCreateRequest {
  provider_id: number
  name: string
  model_id: string
  description?: string | null
  capabilities?: Record<string, unknown> | null
}

export interface ProjectModelConfigCreateRequest {
  model_definition_id: number
  api_key?: string | null
  custom_config?: Record<string, unknown>
  is_default?: boolean
}
