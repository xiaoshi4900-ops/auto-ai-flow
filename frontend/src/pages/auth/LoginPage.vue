<template>
  <div class="login-page" data-testid="login-page">
    <div class="login-surface">
      <section class="login-brand glass-card" data-testid="login-brand">
        <p class="brand-kicker">AI Agent Platform</p>
        <h1>AutoAiFlow</h1>
        <p class="brand-desc">
          Build and observe project-based agent workflows with structured runtime logs.
        </p>
        <ul>
          <li>Project workspace and ownership isolation</li>
          <li>Agent, workflow and run trace in one console</li>
          <li>Execution-first observability and handoff visibility</li>
        </ul>
      </section>

      <section class="login-panel glass-card" data-testid="login-panel">
        <h2>Sign in</h2>
        <p class="panel-subtitle">Use your platform account to enter workspace.</p>

        <form class="login-form" data-testid="login-form" @submit.prevent="handleLogin">
          <label>
            <span>Username</span>
            <input
              v-model="form.username"
              data-testid="login-username"
              type="text"
              autocomplete="username"
              placeholder="demo"
            />
          </label>
          <label>
            <span>Password</span>
            <input
              v-model="form.password"
              data-testid="login-password"
              type="password"
              autocomplete="current-password"
              placeholder="123456"
            />
          </label>
          <button class="primary-btn" data-testid="login-submit" type="submit" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Enter Workspace' }}
          </button>
        </form>

        <p
          v-if="loginMessage"
          class="login-message"
          :class="`is-${loginMessageType}`"
          data-testid="login-message"
        >
          {{ loginMessage }}
        </p>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AxiosError } from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const form = ref({ username: '', password: '' })
const loginMessage = ref('')
const loginMessageType = ref<'success' | 'error'>('error')

async function handleLogin() {
  loginMessage.value = ''
  loading.value = true
  try {
    await authStore.login(form.value.username, form.value.password)
    loginMessageType.value = 'success'
    loginMessage.value = 'Login successful'
    ElMessage.success('Login successful')
    router.push('/projects')
  } catch (e: unknown) {
    const axiosError = e as AxiosError<{ message?: string; detail?: string }>
    const backendMessage = axiosError.response?.data?.message || axiosError.response?.data?.detail
    const errorMessage = backendMessage || 'Login failed'
    loginMessageType.value = 'error'
    loginMessage.value = errorMessage
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  background:
    radial-gradient(circle at 12% 10%, rgba(60, 185, 255, 0.14), transparent 32%),
    radial-gradient(circle at 86% 6%, rgba(86, 240, 192, 0.12), transparent 30%),
    linear-gradient(180deg, #09121c 0%, #081019 55%, #09131d 100%);
}

.login-surface {
  width: min(1060px, 100%);
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 18px;
}

.login-brand,
.login-panel {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-soft);
  padding: 28px;
}

.brand-kicker {
  margin: 0 0 10px;
  color: var(--accent-primary);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.login-brand h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 44px;
  line-height: 1.05;
}

.brand-desc {
  margin: 12px 0 0;
  color: var(--text-secondary);
  font-size: 16px;
}

.login-brand ul {
  margin: 18px 0 0;
  padding-left: 20px;
  color: var(--text-secondary);
  display: grid;
  gap: 8px;
}

.login-panel {
  align-self: center;
}

.login-panel h2 {
  margin: 0;
  font-size: 30px;
}

.panel-subtitle {
  margin: 8px 0 0;
  color: var(--text-secondary);
}

.login-form {
  display: grid;
  gap: 14px;
  margin-top: 18px;
}

.login-form label span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-size: 13px;
}

.login-form input {
  width: 100%;
  height: 46px;
  border-radius: 14px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  padding: 0 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
}

.login-form input:focus {
  outline: none;
  border-color: rgba(86, 240, 192, 0.42);
  box-shadow: 0 0 0 3px rgba(86, 240, 192, 0.12);
}

.primary-btn {
  height: 46px;
  border: 1px solid transparent;
  border-radius: 14px;
  color: #032123;
  font-weight: 700;
  background: linear-gradient(135deg, #56f0c0, #3cb9ff);
  cursor: pointer;
  transition: transform 0.14s ease, box-shadow 0.2s ease, opacity 0.2s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 28px rgba(60, 185, 255, 0.3);
}

.primary-btn:disabled {
  cursor: default;
  opacity: 0.75;
  transform: none;
  box-shadow: none;
}

.login-message {
  margin-top: 14px;
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 14px;
}

.login-message.is-success {
  color: var(--accent-primary);
  background: rgba(86, 240, 192, 0.12);
  border: 1px solid rgba(86, 240, 192, 0.24);
}

.login-message.is-error {
  color: var(--accent-danger);
  background: rgba(255, 111, 127, 0.12);
  border: 1px solid rgba(255, 111, 127, 0.24);
}

@media (max-width: 980px) {
  .login-page {
    padding: 18px;
  }

  .login-surface {
    grid-template-columns: 1fr;
  }

  .login-brand h1 {
    font-size: 36px;
  }
}
</style>
