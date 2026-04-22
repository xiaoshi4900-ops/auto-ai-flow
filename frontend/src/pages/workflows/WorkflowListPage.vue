<template>
  <div class="workflow-page" data-testid="workflow-workspace-page">
    <section class="glass-card section-card" data-testid="workflow-card-region">
      <header class="section-header">
        <div class="title-row">
          <h2>Workflow 资产</h2>
          <select v-model.number="selectedProjectId" class="native-select project-select" @change="loadData">
            <option v-for="p in projectStore.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <button class="primary-btn" data-testid="workflow-col-create" @click="openCreateDialog">新建 Workflow</button>
      </header>

      <div v-if="workflowStore.workflows.length" class="card-grid" data-testid="workflow-list-region">
        <article v-for="workflow in workflowStore.workflows" :key="workflow.id" class="content-card" data-testid="workflow-card-item">
          <span class="chip" data-testid="workflow-col-status">{{ workflow.status || 'draft' }}</span>
          <strong data-testid="workflow-col-name">{{ workflow.name }}</strong>
          <p>
            <span data-testid="workflow-col-version">版本 {{ workflow.version ?? 1 }}</span>
            /
            <span data-testid="workflow-col-nodes">节点 {{ workflow.nodes?.length || 0 }}</span>
            /
            <span data-testid="workflow-col-project">项目 {{ workflow.project_id }}</span>
          </p>
          <small data-testid="workflow-col-updated">{{ workflow.updated_relative || '-' }}</small>
          <div class="card-actions">
            <button class="btn-secondary" data-testid="workflow-row-action-edit" @click="$router.push(`/workflows/${workflow.id}/editor`)">编辑</button>
            <button class="btn-primary" data-testid="workflow-row-action-run" @click="handleRun(workflow.id)">运行</button>
            <button class="btn-danger" data-testid="workflow-row-action-delete" @click="handleDelete(workflow.id)">删除</button>
          </div>
        </article>
      </div>
      <div v-else class="empty-card" data-testid="workflow-empty-state">当前项目暂无 Workflow。</div>
    </section>

    <div v-if="showCreateDialog" class="dialog-overlay" @click.self="showCreateDialog = false">
      <div role="dialog" aria-label="Create Workflow" class="dialog-panel">
        <div class="dialog-header">
          <h2>Create Workflow</h2>
          <button class="dialog-close" @click="showCreateDialog = false">x</button>
        </div>
        <div class="dialog-body">
          <label class="form-label">Project</label>
          <select v-model.number="createForm.project_id" class="native-select">
            <option v-for="p in projectStore.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <label class="form-label">Name</label>
          <input v-model="createForm.name" class="native-input" type="text" />
          <label class="form-label">Description</label>
          <textarea v-model="createForm.description" class="native-textarea" rows="3" />
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
import { useWorkflowStore } from '@/stores/workflow'
import { useProjectStore } from '@/stores/project'
import { useRunStore } from '@/stores/run'
import { ElMessage, ElMessageBox } from 'element-plus'

const workflowStore = useWorkflowStore()
const projectStore = useProjectStore()
const runStore = useRunStore()
const showCreateDialog = ref(false)
const selectedProjectId = ref(1)
const createForm = ref({ name: '', description: '', project_id: 1 })

async function loadData() {
  if (!selectedProjectId.value) return
  await workflowStore.fetchWorkflows(selectedProjectId.value)
}

onMounted(async () => {
  await projectStore.fetchProjects()
  if (projectStore.projects.length) {
    selectedProjectId.value = projectStore.projects[0].id
    createForm.value.project_id = selectedProjectId.value
  }
  await loadData()
})

function openCreateDialog() {
  createForm.value = { name: '', description: '', project_id: selectedProjectId.value }
  showCreateDialog.value = true
}

async function handleCreate() {
  if (!createForm.value.name.trim()) {
    ElMessage.warning('Please input workflow name')
    return
  }
  await workflowStore.createWorkflow({
    ...createForm.value,
    name: createForm.value.name.trim(),
    nodes: [
      { node_key: 'start_1', node_type: 'start', label: 'Start', config: {}, position_x: 120, position_y: 140 },
      { node_key: 'output_1', node_type: 'output', label: 'Output', config: { source_keys: [], output_format: 'raw' }, position_x: 420, position_y: 140 },
    ],
    edges: [{ source_node_key: 'start_1', target_node_key: 'output_1', condition: null, label: null }],
  })
  ElMessage.success('Workflow created')
  showCreateDialog.value = false
  selectedProjectId.value = createForm.value.project_id
  await loadData()
}

async function handleRun(workflowId: number) {
  await runStore.triggerExecution(workflowId)
  ElMessage.success('Workflow started')
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('Delete this workflow?', 'Confirm')
  await workflowStore.deleteWorkflow(id)
  ElMessage.success('Workflow deleted')
  await loadData()
}
</script>

<style scoped>
.workflow-page {
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
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
.btn-danger,
.btn-primary {
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

.btn-primary {
  background: var(--accent-primary);
  color: var(--bg-dark);
  border-color: var(--accent-primary);
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
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 960px) {
  .workflow-page {
    padding: 16px;
  }
}
</style>
