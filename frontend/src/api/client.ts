import axios from 'axios'
import type { ApiResponse } from '@/types/common'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const requestUrl = String(error?.config?.url || '')
    const isAuthLoginRequest = requestUrl.includes('/auth/login')
    if (error.response?.status === 401 && !isAuthLoginRequest) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

function unwrapResponseData<T>(payload: ApiResponse<T> | T): T {
  if (
    payload &&
    typeof payload === 'object' &&
    'data' in payload &&
    'code' in payload &&
    'message' in payload
  ) {
    return (payload as ApiResponse<T>).data
  }
  return payload as T
}

export async function apiGet<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  const res = await client.get<ApiResponse<T> | T>(url, { params })
  return unwrapResponseData<T>(res.data)
}

export async function apiPost<T>(url: string, data?: unknown): Promise<T> {
  const res = await client.post<ApiResponse<T> | T>(url, data)
  return unwrapResponseData<T>(res.data)
}

export async function apiPut<T>(url: string, data?: unknown): Promise<T> {
  const res = await client.put<ApiResponse<T> | T>(url, data)
  return unwrapResponseData<T>(res.data)
}

export async function apiDelete<T = void>(url: string): Promise<T> {
  const res = await client.delete<ApiResponse<T> | T>(url)
  return unwrapResponseData<T>(res.data)
}

export default client
