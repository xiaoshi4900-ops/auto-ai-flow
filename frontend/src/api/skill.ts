import { apiGet } from './client'
import type { Skill } from '@/types/skill'
import type { PaginatedData } from '@/types/common'

export function listSkills(page = 1, pageSize = 20): Promise<PaginatedData<Skill>> {
  return apiGet<PaginatedData<Skill>>('/skills', { page, page_size: pageSize })
}

export function getSkill(id: number): Promise<Skill> {
  return apiGet<Skill>(`/skills/${id}`)
}
