import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Run, RunDetail } from '@/types/execution'
import * as execApi from '@/api/execution'

export const useRunStore = defineStore('run', () => {
  const runs = ref<Run[]>([])
  const currentRun = ref<RunDetail | null>(null)
  const total = ref(0)

  async function fetchRuns(workflowId?: number, page = 1) {
    const res = await execApi.listRuns(workflowId, page)
    runs.value = res.items
    total.value = res.total
  }

  async function fetchRunDetail(runId: number) {
    currentRun.value = await execApi.getRunDetail(runId)
  }

  async function triggerExecution(workflowId: number, inputPayload?: Record<string, unknown>) {
    return await execApi.triggerExecution({ workflow_id: workflowId, input_payload: inputPayload })
  }

  return { runs, currentRun, total, fetchRuns, fetchRunDetail, triggerExecution }
})
