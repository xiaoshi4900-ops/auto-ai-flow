import { apiGet, apiPost } from './client'
import type {
  ModelProvider,
  ModelDefinition,
  ModelListResponse,
  ModelProviderCreateRequest,
  ModelDefinitionCreateRequest,
  ProjectModelConfig,
  ProjectModelConfigCreateRequest,
} from '@/types/model'
import { normalizeModelListResponse } from './adapters'

export async function listModels(): Promise<ModelListResponse> {
  const data = await apiGet<unknown>('/models')
  return normalizeModelListResponse(data)
}

export function listProjectModelConfigs(projectId: number): Promise<ProjectModelConfig[]> {
  return apiGet<ProjectModelConfig[]>(`/models/project/${projectId}/configs`)
}

export function createProjectModelConfig(projectId: number, data: ProjectModelConfigCreateRequest): Promise<ProjectModelConfig> {
  return apiPost<ProjectModelConfig>(`/models/project/${projectId}/configs`, data)
}

export function createModelProvider(data: ModelProviderCreateRequest): Promise<ModelProvider> {
  return apiPost<ModelProvider>('/models/providers', data)
}

export function createModelDefinition(data: ModelDefinitionCreateRequest): Promise<ModelDefinition> {
  return apiPost<ModelDefinition>('/models/definitions', data)
}
