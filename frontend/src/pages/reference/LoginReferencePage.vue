<template>
  <ReferenceShell
    eyebrow="Reference / Auth"
    title="登录页原型"
    subtitle="深色品牌入口 + 玻璃卡片表单，用来约束登录页的层级和状态，而不是最终交互。"
    :metrics="referenceMetrics"
    :items="referenceNavItems"
  >
    <section class="login-grid">
      <div class="login-brand glass-card">
        <p class="panel-kicker">AI Agent Platform</p>
        <h2>让项目、人物、Workflow 和运行追踪在同一工作台内闭环。</h2>
        <ul>
          <li>项目制智能体管理</li>
          <li>结构化 Workflow 执行</li>
          <li>运行过程可观测</li>
        </ul>
      </div>

      <form class="login-form glass-card" data-testid="login-form" @submit.prevent="submit">
        <div v-if="message" class="login-message" :class="message.type" data-testid="login-message">
          {{ message.text }}
        </div>
        <label>
          <span>邮箱</span>
          <input v-model="email" data-testid="login-email" type="email" placeholder="demo@test.com" />
        </label>
        <label>
          <span>密码</span>
          <input v-model="password" data-testid="login-password" type="password" placeholder="123456" />
        </label>
        <button class="primary-btn" data-testid="login-submit" type="submit">
          {{ submitting ? '提交中' : '登录平台' }}
        </button>
      </form>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const email = ref('')
const password = ref('')
const submitting = ref(false)
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null)

async function submit() {
  submitting.value = true
  message.value = null
  await new Promise((resolve) => setTimeout(resolve, 500))
  if (email.value === 'demo@test.com' && password.value === '123456') {
    message.value = { type: 'success', text: '登录成功' }
  } else {
    message.value = { type: 'error', text: '账号或密码错误' }
  }
  submitting.value = false
}
</script>

<style scoped>
.login-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 18px;
}

.login-brand,
.login-form {
  padding: 24px;
  border-radius: 24px;
}

.panel-kicker {
  margin: 0 0 10px;
  color: var(--accent-primary);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.login-brand h2 {
  margin: 0;
  font-size: 32px;
  line-height: 1.2;
}

.login-brand ul {
  margin: 18px 0 0;
  padding-left: 20px;
  color: var(--text-secondary);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.login-form label span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.login-form input {
  width: 100%;
  height: 46px;
  padding: 0 14px;
  border-radius: 14px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.login-message {
  padding: 12px 14px;
  border-radius: 14px;
}

.login-message.success {
  background: rgba(86, 240, 192, 0.1);
  color: var(--accent-primary);
}

.login-message.error {
  background: rgba(255, 111, 127, 0.1);
  color: var(--accent-danger);
}

@media (max-width: 1200px) {
  .login-grid {
    grid-template-columns: 1fr;
  }
}
</style>
