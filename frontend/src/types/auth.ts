export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  display_name?: string
}

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface CurrentUser {
  id: number
  username: string
  email: string
  display_name: string | null
  is_active: boolean
}
