import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CurrentUser } from '@/types/auth'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<CurrentUser | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  async function login(username: string, password: string) {
    const res = await authApi.login({ username, password })
    token.value = res.access_token
    localStorage.setItem('access_token', res.access_token)
    localStorage.setItem('refresh_token', res.refresh_token)
    await fetchUser()
  }

  async function register(username: string, email: string, password: string, displayName?: string) {
    await authApi.register({ username, email, password, display_name: displayName })
  }

  async function fetchUser() {
    try {
      user.value = await authApi.getCurrentUser()
    } catch {
      user.value = null
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { user, token, login, register, fetchUser, logout }
})
