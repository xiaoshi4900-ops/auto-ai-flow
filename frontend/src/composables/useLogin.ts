import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

export function useLogin() {
  const authStore = useAuthStore()
  const loading = ref(false)

  async function login(username: string, password: string) {
    loading.value = true
    try {
      await authStore.login(username, password)
      return true
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Login failed'
      ElMessage.error(msg)
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(username: string, email: string, password: string, displayName?: string) {
    loading.value = true
    try {
      await authStore.register(username, email, password, displayName)
      ElMessage.success('Registration successful')
      return true
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Registration failed'
      ElMessage.error(msg)
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    authStore.logout()
  }

  return { loading, login, register, logout }
}
