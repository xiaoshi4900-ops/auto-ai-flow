<template>
  <ReferenceShell eyebrow="Reference / Agent" title="Agent 列表页原型" subtitle="以人物卡片而不是原始表格来呈现人物资产。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section class="glass-card section-card" data-testid="agent-list-page">
      <header class="section-header">
        <h2>人物资产</h2>
        <button class="primary-btn">新建人物</button>
      </header>
      <div class="card-grid" data-testid="agent-list-region">
        <article v-for="agent in agents" :key="agent.name" class="content-card">
          <span class="chip">{{ agent.role }}</span>
          <strong>{{ agent.name }}</strong>
          <p>{{ agent.responsibility }}</p>
          <small>{{ agent.model }} / skills {{ agent.skillCount }} / tools {{ agent.toolCount }}</small>
        </article>
      </div>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const agents = [
  { name: '内容策略分析师', role: 'content_strategist', responsibility: '梳理内容大纲与风险点', model: 'gpt-4.1-mini', skillCount: 3, toolCount: 1 },
  { name: '成稿工程师', role: 'content_writer', responsibility: '生成最终文稿与摘要', model: 'gpt-4.1', skillCount: 4, toolCount: 2 },
  { name: '质量审查员', role: 'quality_reviewer', responsibility: '验证结构与输出格式', model: 'gpt-4.1-mini', skillCount: 2, toolCount: 1 },
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
  gap: 16px;
  margin-bottom: 16px;
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
}

.content-card p {
  color: var(--text-secondary);
}

@media (max-width: 1200px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
