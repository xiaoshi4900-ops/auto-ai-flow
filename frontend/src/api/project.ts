import { apiGet, apiPost, apiPut, apiDelete } from './client'
import type { Project, ProjectCreateRequest, ProjectUpdateRequest } from '@/types/project'
import type { PaginatedData } from '@/types/common'

export function listProjects(page = 1, pageSize = 20): Promise<PaginatedData<Project>> {
  return apiGet<PaginatedData<Project>>('/projects', { page, page_size: pageSize })
}

export function getProject(id: number): Promise<Project> {
  return apiGet<Project>(`/projects/${id}`)
}

export function createProject(data: ProjectCreateRequest): Promise<Project> {
  return apiPost<Project>('/projects', data)
}

export function updateProject(id: number, data: ProjectUpdateRequest): Promise<Project> {
  return apiPut<Project>(`/projects/${id}`, data)
}

export function deleteProject(id: number): Promise<void> {
  return apiDelete(`/projects/${id}`)
}
