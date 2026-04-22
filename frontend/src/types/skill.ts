export interface Skill {
  id: number
  name: string
  description: string | null
  category: string | null
  prompt_template: string | null
  is_active: boolean
  created_at: string | null
  updated_at: string | null
}
