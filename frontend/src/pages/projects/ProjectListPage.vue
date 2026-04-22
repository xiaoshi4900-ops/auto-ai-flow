<template>
  <div class="projects-page" data-testid="projects-workspace-page">
    <section class="dashboard-row" data-testid="projects-stats-row">
      <div class="stat-card glass-card" data-testid="projects-kpi-total">
        <span>总项目数</span>
        <strong data-testid="projects-kpi-total-value">{{ totalProjects }}</strong>
      </div>
      <div class="stat-card glass-card" data-testid="projects-kpi-active-runs">
        <span>活跃运行</span>
        <strong data-testid="projects-kpi-active-runs-value">{{ activeRuns }}</strong>
      </div>
      <div class="stat-card glass-card" data-testid="projects-kpi-recent-update">
        <span>最近更新</span>
        <strong data-testid="projects-kpi-recent-update-value">{{ recentUpdate }}</strong>
      </div>
    </section>

    <section class="glass-card section-card" data-testid="projects-card-region">
      <header class="section-header">
        <h2>项目空间</h2>
        <button class="primary-btn" data-testid="projects-card-create" @click="showCreateDialog = true">新建项目</button>
      </header>

      <div v-if="projectStore.projects.length" class="card-grid" data-testid="project-list-region">
        <article v-for="project in projectStore.projects" :key="project.id" class="content-card" data-testid="project-card-item">
          <span class="chip" data-testid="project-card-status">{{ project.status || 'active' }}</span>
          <strong data-testid="project-card-name">{{ project.name }}</strong>
          <p data-testid="project-card-desc">{{ project.description || '-' }}</p>
          <small data-testid="project-card-updated">
            {{ project.updated_relative || formatRelativeTime(project.updated_at || project.created_at || '') }}
          </small>
          <div class="card-actions">
            <button class="btn-secondary" @click="$router.push(`/projects/${project.id}`)">详情</button>
            <button class="btn-danger" @click="handleDelete(project.id)">删除</button>
          </div>
        </article>
      </div>
      <div v-else class="empty-card" data-testid="project-empty-state">当前没有项目，请先创建。</div>
    </section>

    <el-dialog v-model="showCreateDialog" title="Create Project" class="workspace-dialog">
      <el-form :model="createForm">
        <el-form-item label="Name">
          <el-input v-model="createForm.name" />
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="createForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">Cancel</el-button>
        <el-button type="primary" @click="handleCreate">Create</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()
const showCreateDialog = ref(false)
const createForm = ref({ name: '', description: '' })

const totalProjects = computed(() => projectStore.projects.length)
const activeRuns = computed(() => {
  return projectStore.projects.filter((p) => ['running', 'active_running'].includes((p.status || '').toLowerCase())).length
})
const recentUpdate = computed(() => {
  const timestamps = projectStore.projects
    .map((p) => Date.parse(p.updated_at || p.created_at || ''))
    .filter((v) => Number.isFinite(v))
  if (!timestamps.length) return '-'
  return formatRelativeTime(new Date(Math.max(...timestamps)).toISOString())
})

onMounted(async () => {
  await projectStore.fetchProjects()
})

function formatRelativeTime(dateStr: string): string {
  if (!dateStr) return '-'
  const dateMs = Date.parse(dateStr)
  if (!Number.isFinite(dateMs)) return '-'
  const delta = Date.now() - dateMs
  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour
  if (delta < minute) return '刚刚'
  if (delta < hour) return `${Math.floor(delta / minute)} 分钟前`
  if (delta < day) return `${Math.floor(delta / hour)} 小时前`
  return `${Math.floor(delta / day)} 天前`
}

async function handleCreate() {
  if (!createForm.value.name.trim()) {
    ElMessage.warning('项目名不能为空')
    return
  }
  await projectStore.createProject(createForm.value)
  ElMessage.success('Project created')
  showCreateDialog.value = false
  createForm.value = { name: '', description: '' }
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('Delete this project?', 'Confirm')
  await projectStore.deleteProject(id)
  ElMessage.success('Project deleted')
}
</script>

<style scoped>
.projects-page {
  padding: 20px 24px;
}

.dashboard-row,
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.stat-card,
.section-card {
  padding: 18px;
  border-radius: 22px;
}

.stat-card span,
.content-card small {
  color: var(--text-muted);
}

.stat-card strong {
  display: block;
  margin-top: 8px;
  font-size: 26px;
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

.content-card,
.empty-card {
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
}

@media (max-width: 1200px) {
  .dashboard-row,
  .card-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .projects-page {
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
