<template>
  <ReferenceShell eyebrow="Reference / Workflow" title="Workflow 列表页原型" subtitle="让用户快速理解当前有哪些可编排、可运行、可追踪的工作流。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section class="glass-card section-card" data-testid="workflow-list-page">
      <header class="section-header">
        <h2>Workflow 资产</h2>
        <button class="primary-btn">新建 Workflow</button>
      </header>
      <div class="card-grid">
        <article v-for="workflow in workflows" :key="workflow.name" class="content-card">
          <span class="chip">{{ workflow.status }}</span>
          <strong>{{ workflow.name }}</strong>
          <p>版本 {{ workflow.version }} / 节点 {{ workflow.nodeCount }}</p>
          <small>更新于 {{ workflow.updatedAt }}</small>
        </article>
      </div>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const workflows = [
  { name: '内容生成流程', version: 3, nodeCount: 5, status: 'draft', updatedAt: '12 分钟前' },
  { name: '质量审查流程', version: 2, nodeCount: 4, status: 'active', updatedAt: '1 小时前' },
]
</script>

<style scoped>
.section-card {
  padding: 18px;
  border-radius: 22px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
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

@media (max-width: 1200px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
