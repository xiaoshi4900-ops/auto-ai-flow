import { apiGet } from './client'
import type { Tool } from '@/types/tool'
import type { PaginatedData } from '@/types/common'

export function listTools(page = 1, pageSize = 20): Promise<PaginatedData<Tool>> {
  return apiGet<PaginatedData<Tool>>('/tools', { page, page_size: pageSize })
}

export function getTool(id: number): Promise<Tool> {
  return apiGet<Tool>(`/tools/${id}`)
}
