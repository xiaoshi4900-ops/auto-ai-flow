export interface Tool {
  id: number
  name: string
  description: string | null
  tool_type: string
  config: string | null
  is_builtin: boolean
  created_at: string | null
  updated_at: string | null
}
