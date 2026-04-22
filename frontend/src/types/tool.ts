export interface Tool {
  id: number
  name: string
  description: string | null
  tool_type: string
  config_schema: Record<string, unknown> | null
  is_active: boolean
  created_at: string | null
  updated_at: string | null
}
