import { apiGet, apiPost } from './client'
import type { ModelListResponse, ProjectModelConfig, ProjectModelConfigCreateRequest } from '@/types/model'

export function listModels(): Promise<ModelListResponse> {
  return apiGet<ModelListResponse>('/models')
}

export function listProjectModelConfigs(projectId: number): Promise<ProjectModelConfig[]> {
  return apiGet<ProjectModelConfig[]>(`/models/project/${projectId}/configs`)
}

export function createProjectModelConfig(projectId: number, data: ProjectModelConfigCreateRequest): Promise<ProjectModelConfig> {
  return apiPost<ProjectModelConfig>(`/models/project/${projectId}/configs`, data)
}
