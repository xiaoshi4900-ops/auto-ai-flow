<template>
  <ReferenceShell eyebrow="Reference / Project" title="项目详情页原型" subtitle="项目级聚合视图，承接 Agent、Workflow 和 Run。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section class="detail-grid">
      <div class="glass-card section-card" data-testid="project-summary-panel">
        <span class="chip">active</span>
        <h2>内容智能体平台</h2>
        <p>面向内容生成和工作流编排的一期 MVP 项目空间。</p>
        <div class="meta-grid">
          <div><span>默认模型</span><strong>gpt-4.1-mini</strong></div>
          <div><span>最近更新</span><strong>10 分钟前</strong></div>
        </div>
      </div>
      <div class="glass-card section-card" data-testid="project-quick-stats">
        <h2>快速统计</h2>
        <div class="dashboard-row">
          <div v-for="stat in stats" :key="stat.label" class="mini-stat">
            <span>{{ stat.label }}</span>
            <strong>{{ stat.value }}</strong>
          </div>
        </div>
      </div>
    </section>
    <section class="content-grid">
      <div class="glass-card section-card">
        <h2>最近 Workflow</h2>
        <div class="list-card">内容生成流程 / draft / 5 nodes</div>
        <div class="list-card">质检分发流程 / active / 4 nodes</div>
      </div>
      <div class="glass-card section-card">
        <h2>最近 Runs</h2>
        <div class="list-card">run_128 / success / 2.4s</div>
        <div class="list-card">run_127 / failed / 1.1s</div>
      </div>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const stats = [
  { label: 'Agents', value: '6' },
  { label: 'Workflows', value: '8' },
  { label: 'Runs', value: '128' },
]
</script>

<style scoped>
.detail-grid,
.content-grid,
.dashboard-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.section-card {
  padding: 18px;
  border-radius: 22px;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.meta-grid span,
.mini-stat span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.meta-grid strong,
.mini-stat strong {
  display: block;
  margin-top: 8px;
}

.list-card {
  padding: 14px;
  margin-top: 10px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
}

@media (max-width: 1200px) {
  .detail-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
