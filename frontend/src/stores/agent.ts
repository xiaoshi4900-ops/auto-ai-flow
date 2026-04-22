import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Agent } from '@/types/agent'
import * as agentApi from '@/api/agent'

export const useAgentStore = defineStore('agent', () => {
  const agents = ref<Agent[]>([])
  const currentAgent = ref<Agent | null>(null)
  const total = ref(0)

  async function fetchAgents(projectId: number, page = 1) {
    const res = await agentApi.listAgents(projectId, page)
    agents.value = res.items
    total.value = res.total
  }

  async function fetchAgent(id: number) {
    currentAgent.value = await agentApi.getAgent(id)
  }

  async function createAgent(data: Parameters<typeof agentApi.createAgent>[0]) {
    await agentApi.createAgent(data)
  }

  async function updateAgent(id: number, data: Parameters<typeof agentApi.updateAgent>[1]) {
    await agentApi.updateAgent(id, data)
  }

  async function deleteAgent(id: number) {
    await agentApi.deleteAgent(id)
  }

  async function bindSkills(agentId: number, skillIds: number[]) {
    await agentApi.bindSkills(agentId, skillIds)
  }

  async function bindTools(agentId: number, toolIds: number[]) {
    await agentApi.bindTools(agentId, toolIds)
  }

  return { agents, currentAgent, total, fetchAgents, fetchAgent, createAgent, updateAgent, deleteAgent, bindSkills, bindTools }
})
