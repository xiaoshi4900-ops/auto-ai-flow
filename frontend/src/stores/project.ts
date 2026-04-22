import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Project } from '@/types/project'
import * as projectApi from '@/api/project'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const total = ref(0)

  async function fetchProjects(page = 1) {
    const res = await projectApi.listProjects(page)
    projects.value = res.items
    total.value = res.total
  }

  async function fetchProject(id: number) {
    currentProject.value = await projectApi.getProject(id)
  }

  async function createProject(data: { name: string; description?: string }) {
    await projectApi.createProject(data)
    await fetchProjects()
  }

  async function deleteProject(id: number) {
    await projectApi.deleteProject(id)
    await fetchProjects()
  }

  return { projects, currentProject, total, fetchProjects, fetchProject, createProject, deleteProject }
})
