<template>
  <div class="agents-page" data-testid="agents-workspace-page">
    <section class="glass-card section-card" data-testid="agents-card-region">
      <header class="section-header">
        <h2>人物资产</h2>
        <button class="primary-btn" data-testid="agents-section-create" @click="openCreateDialog">新建人物</button>
      </header>
      <div v-if="agentStore.agents.length" class="card-grid" data-testid="agent-list-region">
        <article v-for="agent in agentStore.agents" :key="agent.id" class="content-card" data-testid="agent-card-item">
          <span class="chip">{{ agent.role_name }}</span>
          <strong>{{ agent.name }}</strong>
          <p>{{ agent.system_prompt || '配置中...' }}</p>
          <small>
            <span data-testid="agent-card-model">{{ agent.model_name || '-' }}</span> / 
            <span data-testid="agent-card-skill-count">skills {{ (agent.skill_ids || []).length }}</span> / 
            <span data-testid="agent-card-tool-count">tools {{ (agent.tool_ids || []).length }}</span>
          </small>
          <div class="card-actions">
            <button class="btn-secondary" @click="$router.push(`/agents/${agent.id}`)">编辑</button>
            <button class="btn-danger" @click="handleDelete(agent.id)">删除</button>
          </div>
        </article>
      </div>
      <div v-else class="empty-card" data-testid="agents-empty-state">当前没有人物，请先创建。</div>
    </section>

    <el-dialog v-model="showCreateDialog" title="Create Agent" class="workspace-dialog">
      <el-form :model="createForm">
        <el-form-item label="Name"><el-input v-model="createForm.name" /></el-form-item>
        <el-form-item label="Role"><el-input v-model="createForm.role_name" /></el-form-item>
        <el-form-item label="System Prompt"><el-input v-model="createForm.system_prompt" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">Cancel</el-button>
        <el-button type="primary" @click="handleCreate">Create</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAgentStore } from '@/stores/agent'
import { ElMessage, ElMessageBox } from 'element-plus'

const agentStore = useAgentStore()
const showCreateDialog = ref(false)
const createForm = ref({ name: '', role_name: 'assistant', system_prompt: '', project_id: 1 })

onMounted(async () => {
  await agentStore.fetchAgents(1)
})

function openCreateDialog() {
  createForm.value = { name: '', role_name: 'assistant', system_prompt: '', project_id: 1 }
  showCreateDialog.value = true
}

async function handleCreate() {
  await agentStore.createAgent(createForm.value)
  ElMessage.success('Agent created')
  showCreateDialog.value = false
  await agentStore.fetchAgents(1)
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('Delete this agent?', 'Confirm')
  await agentStore.deleteAgent(id)
  ElMessage.success('Agent deleted')
  await agentStore.fetchAgents(1)
}
</script>

<style scoped>
.agents-page {
  padding: 20px 24px;
}

.section-card {
  padding: 18px;
  border-radius: 22px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.section-header h2 {
  margin: 0;
}

.primary-btn {
  background: var(--accent-primary);
  color: var(--bg-dark);
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.primary-btn:hover {
  opacity: 0.85;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.content-card {
  padding: 18px;
  border-radius: 18px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
}

.content-card strong {
  display: block;
  margin-top: 12px;
  font-size: 18px;
}

.content-card p {
  color: var(--text-secondary);
}

.content-card small {
  color: var(--text-muted);
}

.card-actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
}

.btn-secondary,
.btn-danger {
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid var(--border-soft);
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(86, 240, 192, 0.3);
}

.btn-danger {
  border-color: rgba(255, 107, 107, 0.4);
  color: rgba(255, 107, 107, 0.9);
}

.btn-danger:hover {
  background: rgba(255, 107, 107, 0.1);
}

.chip {
  display: inline-flex;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 12px;
}

.empty-card {
  color: var(--text-muted);
  text-align: center;
  padding: 40px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
}

@media (max-width: 1200px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .agents-page {
    padding: 16px;
  }
}
</style>

<style>
.workspace-dialog .el-dialog {
  background-color: rgba(28, 32, 42, 0.98) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 20px !important;
  backdrop-filter: blur(10px);
}

.workspace-dialog .el-dialog__header {
  color: var(--text-primary) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.workspace-dialog .el-dialog__title {
  color: var(--text-primary) !important;
}

.workspace-dialog .el-dialog__body {
  color: var(--text-primary) !important;
}

.workspace-dialog .el-input__wrapper,
.workspace-dialog .el-textarea__inner,
.workspace-dialog .el-select__wrapper {
  background-color: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: var(--text-primary) !important;
  border-radius: 12px !important;
}

.workspace-dialog .el-input__wrapper:hover,
.workspace-dialog .el-textarea__inner:hover,
.workspace-dialog .el-select__wrapper:hover {
  border-color: rgba(86, 240, 192, 0.3) !important;
}

.workspace-dialog .el-input__wrapper.is-focus,
.workspace-dialog .el-textarea__inner:focus,
.workspace-dialog .el-select__wrapper.is-focus {
  box-shadow: 0 0 0 2px rgba(86, 240, 192, 0.2) !important;
  border-color: rgba(86, 240, 192, 0.5) !important;
}

.workspace-dialog .el-input__inner,
.workspace-dialog .el-textarea__inner {
  color: var(--text-primary) !important;
}

.workspace-dialog .el-input__inner::placeholder,
.workspace-dialog .el-textarea__inner::placeholder {
  color: var(--text-secondary) !important;
}

.workspace-dialog .el-dialog__footer {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.workspace-dialog .el-button {
  border-radius: 12px !important;
}
</style>
