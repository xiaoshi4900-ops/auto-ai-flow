<template>
  <ReferenceShell eyebrow="Reference / Run" title="Run 列表页原型" subtitle="突出状态筛选、最近执行、失败高亮。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section class="glass-card section-card" data-testid="run-list-page">
      <header class="section-header">
        <h2>执行记录</h2>
        <div class="filters">
          <span class="chip">all</span>
          <span class="chip">success</span>
          <span class="chip">failed</span>
        </div>
      </header>
      <div class="table-list" data-testid="run-list-region">
        <div v-for="run in runs" :key="run.id" class="table-row">
          <strong>{{ run.id }}</strong>
          <span>{{ run.workflow }}</span>
          <span :class="run.status === 'failed' ? 'bad' : 'ok'">{{ run.status }}</span>
          <span>{{ run.latency }}</span>
          <span>{{ run.tokens }}</span>
        </div>
      </div>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const runs = [
  { id: 'run_128', workflow: '内容生成流程', status: 'success', latency: '2.4s', tokens: '1284' },
  { id: 'run_127', workflow: '内容生成流程', status: 'failed', latency: '1.1s', tokens: '644' },
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

.filters {
  display: flex;
  gap: 8px;
}

.table-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1.1fr 0.7fr 0.7fr 0.7fr;
  gap: 12px;
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
}

.ok { color: var(--accent-primary); }
.bad { color: var(--accent-danger); }
</style>
