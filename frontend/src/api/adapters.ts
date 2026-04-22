import type { ModelDefinition, ModelListResponse, ModelProvider } from '@/types/model'
import type { RoleTemplate } from './roleTemplate'

type UnknownRecord = Record<string, unknown>

function asRecord(value: unknown): UnknownRecord {
  return (value && typeof value === 'object' ? value : {}) as UnknownRecord
}

function asString(value: unknown, fallback = ''): string {
  return typeof value === 'string' ? value : fallback
}

function asNumber(value: unknown, fallback = 0): number {
  return typeof value === 'number' ? value : fallback
}

function asBool(value: unknown, fallback = false): boolean {
  return typeof value === 'boolean' ? value : fallback
}

export function normalizeModelProvider(rawValue: unknown): ModelProvider {
  const raw = asRecord(rawValue)
  return {
    id: asNumber(raw.id),
    name: asString(raw.name),
    provider_type: asString(raw.provider_type),
    api_base: asString(raw.api_base, asString(raw.api_base_url, null as unknown as string)),
    is_builtin: asBool(raw.is_builtin, false),
  }
}

export function normalizeModelDefinition(rawValue: unknown): ModelDefinition {
  const raw = asRecord(rawValue)
  const name = asString(raw.name, asString(raw.display_name, asString(raw.model_name)))
  const modelId = asString(raw.model_id, asString(raw.model_name))
  const descriptionRaw = raw.description
  const capabilitiesRaw = raw.capabilities
  return {
    id: asNumber(raw.id),
    provider_id: asNumber(raw.provider_id),
    name,
    model_id: modelId,
    description: typeof descriptionRaw === 'string' ? descriptionRaw : null,
    capabilities: capabilitiesRaw && typeof capabilitiesRaw === 'object' ? (capabilitiesRaw as Record<string, unknown>) : null,
    is_builtin: asBool(raw.is_builtin, false),
  }
}

export function normalizeModelListResponse(rawValue: unknown): ModelListResponse {
  const raw = asRecord(rawValue)
  const providersRaw = Array.isArray(raw.providers) ? raw.providers : []
  const modelsRaw = Array.isArray(raw.models) ? raw.models : []
  return {
    providers: providersRaw.map((item) => normalizeModelProvider(item)),
    models: modelsRaw.map((item) => normalizeModelDefinition(item)),
  }
}

export function normalizeRoleTemplate(rawValue: unknown): RoleTemplate {
  const raw = asRecord(rawValue)
  return {
    id: asNumber(raw.id),
    key: asString(raw.key),
    name: asString(raw.name),
    category: asString(raw.category, null as unknown as string),
    description: asString(raw.description, null as unknown as string),
    execution_mode: asString(raw.execution_mode),
    default_role_name: asString(raw.default_role_name, null as unknown as string),
    default_model_id: typeof raw.default_model_id === 'number' ? raw.default_model_id : null,
    default_skill_ids: Array.isArray(raw.default_skill_ids)
      ? raw.default_skill_ids.filter((x): x is number => typeof x === 'number')
      : [],
    default_tool_ids: Array.isArray(raw.default_tool_ids)
      ? raw.default_tool_ids.filter((x): x is number => typeof x === 'number')
      : [],
    default_code_policy: (raw.default_code_policy && typeof raw.default_code_policy === 'object'
      ? raw.default_code_policy
      : null) as RoleTemplate['default_code_policy'],
    is_builtin: asBool(raw.is_builtin, false),
    enabled: asBool(raw.enabled, true),
  }
}

export function normalizeRoleTemplateList(rawValue: unknown): RoleTemplate[] {
  const raw = asRecord(rawValue)
  const itemsRaw = Array.isArray(raw.items) ? raw.items : []
  return itemsRaw.map((item) => normalizeRoleTemplate(item))
}
