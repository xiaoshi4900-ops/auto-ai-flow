import { apiPost, apiGet } from './client'
import type { ExecutionTriggerRequest, ExecutionTriggerResponse, RunDetail, Run } from '@/types/execution'
import type { PaginatedData } from '@/types/common'

export function triggerExecution(data: ExecutionTriggerRequest): Promise<ExecutionTriggerResponse> {
  return apiPost<ExecutionTriggerResponse>('/executions/trigger', data)
}

export function listRuns(workflowId?: number, page = 1, pageSize = 20): Promise<PaginatedData<Run>> {
  const params: Record<string, unknown> = { page, page_size: pageSize }
  if (workflowId != null) params.workflow_id = workflowId
  return apiGet<PaginatedData<Run>>('/runs', params)
}

export function getRunDetail(runId: number): Promise<RunDetail> {
  return apiGet<RunDetail>(`/runs/${runId}`)
}
