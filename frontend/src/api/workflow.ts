import { apiGet, apiPost, apiPut, apiDelete } from './client'
import type { Workflow, WorkflowCreateRequest, WorkflowUpdateRequest } from '@/types/workflow'
import type { PaginatedData } from '@/types/common'

export function listWorkflows(projectId: number, page = 1, pageSize = 20): Promise<PaginatedData<Workflow>> {
  return apiGet<PaginatedData<Workflow>>('/workflows', { project_id: projectId, page, page_size: pageSize })
}

export function getWorkflow(id: number): Promise<Workflow> {
  return apiGet<Workflow>(`/workflows/${id}`)
}

export function createWorkflow(data: WorkflowCreateRequest): Promise<Workflow> {
  return apiPost<Workflow>('/workflows', data)
}

export function updateWorkflow(id: number, data: WorkflowUpdateRequest): Promise<Workflow> {
  return apiPut<Workflow>(`/workflows/${id}`, data)
}

export function deleteWorkflow(id: number): Promise<void> {
  return apiDelete(`/workflows/${id}`)
}
