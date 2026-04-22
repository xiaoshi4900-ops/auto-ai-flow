<template>
  <ReferenceShell eyebrow="Reference / Project" title="项目列表页原型" subtitle="项目空间入口，强调统计、列表、创建动作和空态。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section class="dashboard-row">
      <div v-for="stat in stats" :key="stat.label" class="stat-card glass-card">
        <span>{{ stat.label }}</span>
        <strong>{{ stat.value }}</strong>
      </div>
    </section>

    <section class="glass-card section-card" data-testid="project-list-page">
      <header class="section-header">
        <h2>项目空间</h2>
        <button class="primary-btn" data-testid="project-create-button" @click="createProject">新建项目</button>
      </header>

      <div v-if="projects.length" class="card-grid" data-testid="project-list-region">
        <article v-for="project in projects" :key="project.id" class="content-card">
          <span class="chip">{{ project.status }}</span>
          <strong>{{ project.name }}</strong>
          <p>{{ project.description }}</p>
          <small>更新于 {{ project.updatedAt }}</small>
        </article>
      </div>
      <div v-else class="empty-card" data-testid="project-empty-state">当前没有项目，请先创建。</div>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const stats = [
  { label: '总项目数', value: '4' },
  { label: '活跃运行', value: '12' },
  { label: '最近更新', value: '3h' },
]

const projects = ref([
  { id: 1, name: '内容智能体平台', description: '面向营销内容编排与运行追踪。', status: 'active', updatedAt: '10 分钟前' },
  { id: 2, name: '运营自动化工作台', description: '任务拆分、运行分析和结果归档。', status: 'draft', updatedAt: '2 小时前' },
])

function createProject() {
  projects.value.unshift({
    id: Date.now(),
    name: '新项目原型',
    description: '这是用于验证创建交互的前端原型数据。',
    status: 'active',
    updatedAt: '刚刚',
  })
}
</script>

<style scoped>
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

.chip {
  display: inline-flex;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 12px;
}

@media (max-width: 1200px) {
  .dashboard-row,
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
