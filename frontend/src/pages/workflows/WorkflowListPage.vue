<template>
  <div class="workflow-page" data-testid="workflow-workspace-page">
    <section class="glass-card section-card" data-testid="workflow-card-region">
      <header class="section-header">
        <h2>Workflow 资产</h2>
        <button class="primary-btn" data-testid="workflow-col-create" @click="openCreateDialog">新建 Workflow</button>
      </header>
      <div v-if="workflowStore.workflows.length" class="card-grid" data-testid="workflow-list-region">
        <article v-for="workflow in workflowStore.workflows" :key="workflow.id" class="content-card" data-testid="workflow-card-item">
          <span class="chip" data-testid="workflow-col-status">{{ workflow.status || 'draft' }}</span>
          <strong data-testid="workflow-col-name">{{ workflow.name }}</strong>
          <p>
            <span data-testid="workflow-col-version">版本 {{ workflow.version ?? 1 }}</span> / 
            <span data-testid="workflow-col-nodes">节点 {{ workflow.nodes?.length || 0 }}</span>
          </p>
          <small data-testid="workflow-col-updated">{{ workflow.updated_relative || '刚刚更新' }}</small>
          <div class="card-actions">
            <button class="btn-secondary" data-testid="workflow-row-action-edit" @click="$router.push(`/workflows/${workflow.id}/editor`)">编辑</button>
            <button class="btn-primary" data-testid="workflow-row-action-run" @click="handleRun()">运行</button>
            <button class="btn-danger" data-testid="workflow-row-action-delete" @click="handleDelete(workflow.id)">删除</button>
          </div>
        </article>
      </div>
      <div v-else class="empty-card" data-testid="workflow-empty-state">暂无 Workflow，请先创建。</div>
    </section>

    <el-dialog v-model="showCreateDialog" title="Create Workflow" class="workspace-dialog">
      <el-form :model="createForm">
        <el-form-item label="Name"><el-input v-model="createForm.name" /></el-form-item>
        <el-form-item label="Description"><el-input v-model="createForm.description" type="textarea" /></el-form-item>
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
import { useWorkflowStore } from '@/stores/workflow'
import { ElMessage, ElMessageBox } from 'element-plus'

const workflowStore = useWorkflowStore()
const showCreateDialog = ref(false)
const createForm = ref({ name: '', description: '', project_id: 1 })

onMounted(async () => {
  await workflowStore.fetchWorkflows(1)
})

function openCreateDialog() {
  createForm.value = { name: '', description: '', project_id: 1 }
  showCreateDialog.value = true
}

async function handleCreate() {
  await workflowStore.createWorkflow(createForm.value)
  ElMessage.success('Workflow created')
  showCreateDialog.value = false
  await workflowStore.fetchWorkflows(1)
}

async function handleRun() {
  ElMessage.success('Workflow started')
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('Delete this workflow?', 'Confirm')
  await workflowStore.deleteWorkflow(id)
  ElMessage.success('Workflow deleted')
  await workflowStore.fetchWorkflows(1)
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

@media (max-width: 1200px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .workflow-page {
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
