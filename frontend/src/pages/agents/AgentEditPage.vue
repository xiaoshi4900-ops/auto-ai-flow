<template>
  <div class="agent-edit-page" data-testid="agent-edit-page">
    <section class="edit-grid">
      <div class="glass-card section-card" data-testid="agent-identity-panel">
        <h2>人物基本信息</h2>

        <label>
          <span>名称</span>
          <input v-model="form.name" data-testid="agent-edit-name-input" />
        </label>

        <label>
          <span>角色</span>
          <input v-model="form.role_name" />
        </label>

        <label>
          <span>模型</span>
          <select v-model="form.model_id" class="template-select">
            <option :value="null">使用项目默认模型</option>
            <option v-for="m in models" :key="m.id" :value="m.id">{{ modelLabel(m) }}</option>
          </select>
        </label>

        <label>
          <span>System Prompt</span>
          <textarea v-model="form.system_prompt" rows="5" />
        </label>
      </div>

      <div class="glass-card section-card" data-testid="agent-capability-panel">
        <h2>能力关联</h2>

        <label>
          <span>Skills</span>
          <select v-model="selectedSkillIds" class="template-select" multiple size="6" data-testid="agent-edit-skills">
            <option v-for="s in skills" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </label>

        <label>
          <span>Tools</span>
          <select v-model="selectedToolIds" class="template-select" multiple size="6" data-testid="agent-edit-tools">
            <option v-for="t in tools" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
        </label>

        <label class="switch-row">
          <input v-model="form.allow_tool_use" type="checkbox" />
          <span>Allow Tool Use</span>
        </label>
      </div>
    </section>

    <section class="glass-card section-card">
      <h2>背景与约束</h2>
      <div class="two-col">
        <label>
          <span>Identity</span>
          <textarea v-model="form.background_identity" rows="3" />
        </label>
        <label>
          <span>Experience</span>
          <textarea v-model="form.background_experience" rows="3" />
        </label>
        <label>
          <span>Knowledge</span>
          <textarea v-model="form.domain_knowledge" rows="3" />
        </label>
        <label>
          <span>Responsibility</span>
          <textarea v-model="form.responsibility" rows="3" />
        </label>
      </div>
      <label>
        <span>Constraints</span>
        <textarea v-model="form.constraints" rows="3" />
      </label>
      <div class="save-row">
        <span v-if="saved" class="save-success">保存成功</span>
        <button class="primary-btn" data-testid="agent-edit-save" :disabled="saving" @click="onSave">
          {{ saving ? '保存中...' : '保存 Agent' }}
        </button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAgentStore } from '@/stores/agent'
import * as modelApi from '@/api/model'
import * as skillApi from '@/api/skill'
import * as toolApi from '@/api/tool'
import type { ModelDefinition } from '@/types/model'
import type { Skill } from '@/types/skill'
import type { Tool } from '@/types/tool'

const route = useRoute()
const agentStore = useAgentStore()

const models = ref<ModelDefinition[]>([])
const skills = ref<Skill[]>([])
const tools = ref<Tool[]>([])
const selectedSkillIds = ref<number[]>([])
const selectedToolIds = ref<number[]>([])
const saved = ref(false)
const saving = ref(false)

const form = ref({
  name: '',
  role_name: 'assistant',
  system_prompt: '',
  background_identity: '',
  background_experience: '',
  domain_knowledge: '',
  responsibility: '',
  constraints: '',
  model_id: null as number | null,
  allow_tool_use: false,
})

function modelLabel(model: ModelDefinition): string {
  return model.name && model.name !== model.model_id ? `${model.name} (${model.model_id})` : model.model_id
}

async function loadData() {
  const id = Number(route.params.id)
  if (!id) return
  await agentStore.fetchAgent(id)
  const agent = agentStore.currentAgent
  if (!agent) return

  form.value = {
    name: agent.name || '',
    role_name: agent.role_name || 'assistant',
    system_prompt: agent.system_prompt || '',
    background_identity: agent.background_identity || '',
    background_experience: agent.background_experience || '',
    domain_knowledge: agent.domain_knowledge || '',
    responsibility: agent.responsibility || '',
    constraints: agent.constraints || '',
    model_id: agent.model_id ?? null,
    allow_tool_use: !!agent.allow_tool_use,
  }
  selectedSkillIds.value = [...(agent.skill_ids || [])]
  selectedToolIds.value = [...(agent.tool_ids || [])]

  const [modelRes, skillRes, toolRes] = await Promise.all([
    modelApi.listModels(),
    skillApi.listSkills(1, 200),
    toolApi.listTools(1, 200),
  ])
  models.value = modelRes.models
  skills.value = skillRes.items
  tools.value = toolRes.items
}

async function onSave() {
  const id = Number(route.params.id)
  if (!id) return
  saving.value = true
  saved.value = false
  try {
    await agentStore.updateAgent(id, {
      ...form.value,
      model_id: form.value.model_id ?? undefined,
    })
    await agentStore.bindSkills(id, selectedSkillIds.value)
    await agentStore.bindTools(id, selectedToolIds.value)
    saved.value = true
    ElMessage.success('保存成功')
    await agentStore.fetchAgent(id)
  } catch (err) {
    console.error('save agent failed', err)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  void loadData()
})
</script>

<style scoped>
.agent-edit-page {
  padding: 20px 24px;
}

.edit-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
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

.switch-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
}

.switch-row input {
  width: auto;
  margin: 0;
}

.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.save-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: 8px;
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

.primary-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

@media (max-width: 1200px) {
  .edit-grid,
  .two-col {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .agent-edit-page {
    padding: 16px;
  }
}
</style>
