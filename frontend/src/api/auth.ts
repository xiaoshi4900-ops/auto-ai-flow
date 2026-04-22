import { apiPost, apiGet } from './client'
import type { LoginRequest, RegisterRequest, TokenPair, CurrentUser } from '@/types/auth'

export function login(data: LoginRequest): Promise<TokenPair> {
  return apiPost<TokenPair>('/auth/login', data)
}

export function register(data: RegisterRequest): Promise<CurrentUser> {
  return apiPost<CurrentUser>('/auth/register', data)
}

export function getCurrentUser(): Promise<CurrentUser> {
  return apiGet<CurrentUser>('/auth/me')
}

export function refreshToken(refresh_token: string): Promise<TokenPair> {
  return apiPost<TokenPair>('/auth/refresh', { refresh_token })
}
