import { apiGet, apiPost, apiPut, apiDelete } from './client'
import type { Agent, AgentCreateRequest, AgentUpdateRequest } from '@/types/agent'
import type { PaginatedData } from '@/types/common'

export function listAgents(projectId: number, page = 1, pageSize = 20): Promise<PaginatedData<Agent>> {
  return apiGet<PaginatedData<Agent>>('/agents', { project_id: projectId, page, page_size: pageSize })
}

export function getAgent(id: number): Promise<Agent> {
  return apiGet<Agent>(`/agents/${id}`)
}

export function createAgent(data: AgentCreateRequest): Promise<Agent> {
  return apiPost<Agent>('/agents', data)
}

export function updateAgent(id: number, data: AgentUpdateRequest): Promise<Agent> {
  return apiPut<Agent>(`/agents/${id}`, data)
}

export function deleteAgent(id: number): Promise<void> {
  return apiDelete(`/agents/${id}`)
}

export function bindSkills(agentId: number, skillIds: number[]): Promise<Agent> {
  return apiPost<Agent>(`/agents/${agentId}/skills`, { skill_ids: skillIds })
}

export function bindTools(agentId: number, toolIds: number[]): Promise<Agent> {
  return apiPost<Agent>(`/agents/${agentId}/tools`, { tool_ids: toolIds })
}
