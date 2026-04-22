<template>
  <div class="agents-page" data-testid="agents-workspace-page">
    <section class="glass-card section-card" data-testid="agents-card-region">
      <header class="section-header">
        <div class="title-row">
          <h2>人物资产</h2>
          <select v-model.number="selectedProjectId" class="project-select" @change="loadData">
            <option v-for="p in projectStore.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <button class="primary-btn" data-testid="agents-section-create" @click="openCreateDialog">新建人物</button>
      </header>

      <div v-if="agentStore.agents.length" class="card-grid" data-testid="agent-list-region">
        <article v-for="agent in agentStore.agents" :key="agent.id" class="content-card" data-testid="agent-card-item">
          <span class="chip">{{ agent.role_name }}</span>
          <strong>{{ agent.name }}</strong>
          <p>{{ agent.system_prompt || '暂无 prompt' }}</p>
          <small>
            <span data-testid="agent-card-model">model {{ agent.model_id ?? '-' }}</span>
            /
            <span data-testid="agent-card-skill-count">skills {{ (agent.skill_ids || []).length }}</span>
            /
            <span data-testid="agent-card-tool-count">tools {{ (agent.tool_ids || []).length }}</span>
          </small>
          <div class="card-actions">
            <button class="btn-secondary" @click="$router.push(`/agents/${agent.id}`)">编辑</button>
            <button class="btn-danger" @click="handleDelete(agent.id)">删除</button>
          </div>
        </article>
      </div>
      <div v-else class="empty-card" data-testid="agents-empty-state">当前项目暂无人物。</div>
    </section>

    <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
      <div role="dialog" aria-label="Create Agent" class="dialog-panel">
        <div class="dialog-header">
          <h2>Create Agent</h2>
          <button class="dialog-close" @click="showCreateDialog = false">x</button>
        </div>
        <div class="dialog-body">
          <label class="form-label">Project</label>
          <select v-model.number="createForm.project_id" class="native-select">
            <option v-for="p in projectStore.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <label class="form-label">Name</label>
          <input v-model="createForm.name" class="native-input" />
          <label class="form-label">Role</label>
          <input v-model="createForm.role_name" class="native-input" />
          <label class="form-label">System Prompt</label>
          <textarea v-model="createForm.system_prompt" class="native-textarea" rows="3" />
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="showCreateDialog = false">Cancel</button>
          <button class="btn-confirm" @click="handleCreate">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAgentStore } from '@/stores/agent'
import { useProjectStore } from '@/stores/project'
import { ElMessage, ElMessageBox } from 'element-plus'

const agentStore = useAgentStore()
const projectStore = useProjectStore()
const showCreateDialog = ref(false)
const selectedProjectId = ref(1)
const createForm = ref({ name: '', role_name: 'assistant', system_prompt: '', project_id: 1 })

onMounted(async () => {
  await projectStore.fetchProjects()
  if (projectStore.projects.length) {
    selectedProjectId.value = projectStore.projects[0].id
    createForm.value.project_id = selectedProjectId.value
  }
  await loadData()
})

async function loadData() {
  if (!selectedProjectId.value) return
  await agentStore.fetchAgents(selectedProjectId.value)
}

function openCreateDialog() {
  createForm.value = { name: '', role_name: 'assistant', system_prompt: '', project_id: selectedProjectId.value }
  showCreateDialog.value = true
}

async function handleCreate() {
  if (!createForm.value.name.trim()) {
    ElMessage.warning('Please input agent name')
    return
  }
  await agentStore.createAgent({
    ...createForm.value,
    name: createForm.value.name.trim(),
  })
  ElMessage.success('Agent created')
  showCreateDialog.value = false
  selectedProjectId.value = createForm.value.project_id
  await loadData()
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('Delete this agent?', 'Confirm')
  await agentStore.deleteAgent(id)
  ElMessage.success('Agent deleted')
  await loadData()
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

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-header h2 {
  margin: 0;
}

.project-select {
  min-width: 220px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
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

.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.dialog-panel {
  background: rgba(28, 32, 42, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  width: 480px;
  max-width: 92vw;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.dialog-close {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
}

.dialog-body {
  padding: 20px;
}

.form-label {
  display: block;
  margin-top: 10px;
  margin-bottom: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.native-select,
.native-input,
.native-textarea {
  width: 100%;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-cancel,
.btn-confirm {
  padding: 8px 20px;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
}

.btn-cancel {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.btn-confirm {
  background: var(--accent-primary);
  border: none;
  color: var(--bg-dark);
  font-weight: 600;
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
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
