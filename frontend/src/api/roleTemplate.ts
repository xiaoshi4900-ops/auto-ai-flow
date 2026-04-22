import { apiGet, apiPost } from './client'

export interface RoleTemplate {
  id: number
  key: string
  name: string
  category: string | null
  description: string | null
  execution_mode: string
  default_role_name: string | null
  default_model_id: number | null
  default_skill_ids: number[]
  default_tool_ids: number[]
  default_code_policy: CodeExecutionPolicy | null
  is_builtin: boolean
  enabled: boolean
}

export interface CodeExecutionPolicy {
  max_iterations: number
  allow_file_write: boolean
  run_lint: boolean
  run_build: boolean
  run_unit_tests: boolean
  require_plan_first: boolean
  require_integration_tests: boolean
  allow_repo_read: boolean
  allow_repo_write: boolean
  allow_auto_commit: boolean
  allow_auto_pr: boolean
  stop_on_critical_error: boolean
  fallback_to_human: boolean
}

export interface CodeIteration {
  id: number
  code_task_id: number
  iteration_no: number
  status: string
  plan_summary: string | null
  changed_files: string | null
  validation_lint: string | null
  validation_build: string | null
  validation_unit_tests: string | null
}

interface RoleTemplateListResponse {
  items: RoleTemplate[]
}

interface CodeIterationListResponse {
  items: CodeIteration[]
}

export function listRoleTemplates(): Promise<RoleTemplateListResponse> {
  return apiGet<RoleTemplateListResponse>('/role-templates')
}

export function getRoleTemplate(id: number): Promise<RoleTemplate> {
  return apiGet<RoleTemplate>(`/role-templates/${id}`)
}

export function createAgentFromTemplate(projectId: number, data: { role_template_id: number; name?: string; description?: string; model_id?: number }): Promise<any> {
  return apiPost(`/projects/${projectId}/agents/from-template`, data)
}

export function listCodeIterationsByRun(runId: number): Promise<CodeIterationListResponse> {
  return apiGet<CodeIterationListResponse>(`/runs/${runId}/code-iterations`)
}
