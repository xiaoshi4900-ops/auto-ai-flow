<template>
  <div class="agent-edit-page" data-testid="agent-edit-page">
    <section class="edit-grid">
      <div class="glass-card section-card" data-testid="agent-identity-panel">
        <h2>人物基本信息</h2>
        <label>
          <span>角色模板</span>
          <div data-testid="agent-edit-role-template">
            <select v-model="selectedTemplate" class="template-select">
              <option value="">选择角色模板...</option>
              <option v-for="tpl in templates" :key="tpl.key" :value="tpl.key">{{ tpl.key }} - {{ tpl.name }}</option>
            </select>
          </div>
        </label>
        <label>
          <span>名称</span>
          <input v-model="name" data-testid="agent-edit-name-input" />
        </label>
        <label>
          <span>角色</span>
          <input :value="roleValue" readonly />
        </label>
        <label>
          <span>执行模式</span>
          <input data-testid="agent-edit-execution-mode" :value="executionMode" readonly />
        </label>
        <label>
          <span>职责</span>
          <textarea rows="4">{{ responsibilityValue }}</textarea>
        </label>
        <div v-if="executionMode" class="mode-chip">{{ executionMode }}</div>
      </div>
      <div class="glass-card section-card" data-testid="agent-capability-panel">
        <h2>能力挂载</h2>
        <div class="list-card">模型：gpt-4.1-mini</div>
        <div class="list-card" data-testid="agent-edit-skills">Skills：generate_outline / explain_code / review_output</div>
        <div class="list-card" data-testid="agent-edit-tools">Tools：web_search / read_repo_file</div>
      </div>
    </section>
    <section class="glass-card section-card">
      <h2>Prompt 与约束</h2>
      <textarea class="large-area" rows="8">你是内容策略分析师，需要优先输出结构化内容，而不是自由散文。</textarea>
      <div class="save-row">
        <div>
          <span v-if="saved" class="save-message">已保存</span>
          <span v-if="saved" class="save-success">保存成功</span>
        </div>
        <button class="primary-btn" data-testid="agent-edit-save" @click="onSave">保存 Agent</button>
      </div>
    </section>
    <section class="glass-card section-card" data-testid="agent-policy-panel">
      <h2>策略配置</h2>
      <label>
        <span>最大迭代次数</span>
        <input data-testid="agent-edit-policy-max-iterations" type="number" :value="maxIterations" readonly />
      </label>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'


const templates = [
  { key: 'backend_engineer', name: 'Backend Engineer', execution_mode: 'code_runtime' },
  { key: 'product_manager', name: 'Product Manager', execution_mode: 'normal_llm' },
]

const selectedTemplate = ref('')
const name = ref('内容策略分析师')
const saved = ref(false)
const maxIterations = ref(5)

const executionMode = computed(() => {
  const tpl = templates.find(t => t.key === selectedTemplate.value)
  return tpl ? tpl.execution_mode : 'normal_llm'
})

const roleValue = computed(() => {
  if (selectedTemplate.value) return selectedTemplate.value
  return 'content_strategist'
})

const responsibilityValue = computed(() => {
  if (selectedTemplate.value === 'backend_engineer') return '编写后端服务代码，执行构建与测试。'
  if (selectedTemplate.value === 'product_manager') return '梳理产品需求，输出PRD和优先级。'
  return '梳理内容结构、识别风险点、输出结构化策略建议。'
})

watch(selectedTemplate, (val) => {
  if (val === 'backend_engineer') {
    name.value = 'Backend Engineer'
  } else if (val === 'product_manager') {
    name.value = 'Product Manager'
  }
})

function onSave() {
  saved.value = true
}
</script>

<style scoped>
.agent-edit-page {
  padding: 20px 24px;
}

.edit-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 16px;
}

.section-card {
  padding: 18px;
  border-radius: 22px;
}

label span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

input,
textarea,
.template-select {
  width: 100%;
  margin-bottom: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.template-select option {
  background: #0a1019;
  color: var(--text-primary);
}

.mode-chip {
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 13px;
  margin-bottom: 14px;
}

.list-card {
  padding: 14px;
  margin-bottom: 10px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
}

.large-area {
  margin-top: 8px;
}

.save-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.save-message {
  color: var(--accent-primary);
}

.save-success {
  color: var(--accent-primary);
}

.primary-btn {
  background: var(--accent-primary);
  color: var(--bg-dark);
  border: none;
  padding: 12px 24px;
  border-radius: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.primary-btn:hover {
  opacity: 0.85;
}

@media (max-width: 1200px) {
  .edit-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .agent-edit-page {
    padding: 16px;
  }
}
</style>
