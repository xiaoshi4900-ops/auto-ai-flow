import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Workflow } from '@/types/workflow'
import * as workflowApi from '@/api/workflow'

export const useWorkflowStore = defineStore('workflow', () => {
  const workflows = ref<Workflow[]>([])
  const currentWorkflow = ref<Workflow | null>(null)
  const total = ref(0)

  async function fetchWorkflows(projectId: number, page = 1) {
    const res = await workflowApi.listWorkflows(projectId, page)
    workflows.value = res.items
    total.value = res.total
  }

  async function fetchWorkflow(id: number) {
    currentWorkflow.value = await workflowApi.getWorkflow(id)
  }

  async function createWorkflow(data: Parameters<typeof workflowApi.createWorkflow>[0]) {
    await workflowApi.createWorkflow(data)
  }

  async function updateWorkflow(id: number, data: Parameters<typeof workflowApi.updateWorkflow>[1]) {
    await workflowApi.updateWorkflow(id, data)
  }

  async function deleteWorkflow(id: number) {
    await workflowApi.deleteWorkflow(id)
  }

  return { workflows, currentWorkflow, total, fetchWorkflows, fetchWorkflow, createWorkflow, updateWorkflow, deleteWorkflow }
})
