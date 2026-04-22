export interface Skill {
  id: number
  name: string
  skill_key: string | null
  description: string | null
  prompt_template: string | null
  execution_mode: string | null
  is_builtin: boolean
  created_at: string | null
  updated_at: string | null
}
