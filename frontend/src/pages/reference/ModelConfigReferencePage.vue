<template>
  <ReferenceShell eyebrow="Reference / Model" title="Model Config" subtitle="突出 provider、模型、密钥托管状态和默认模型。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section class="glass-card section-card" data-testid="model-config-page">
      <header class="section-header">
        <h2>模型配置</h2>
        <button class="primary-btn">新增配置</button>
      </header>
      <div class="table-list">
        <div class="table-row table-row--head">
          <span>Provider</span>
          <span>Model</span>
          <span>状态</span>
          <span>密钥</span>
        </div>
        <div class="table-row">
          <span>OpenAI</span>
          <span>gpt-4.1-mini</span>
          <span class="ok">enabled</span>
          <span>已托管</span>
        </div>
        <div class="table-row">
          <span>NVIDIA</span>
          <span>z-ai/glm-5.1</span>
          <span class="ok">enabled</span>
          <span>已托管</span>
        </div>
      </div>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'
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

.table-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.table-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
}

.table-row--head {
  color: var(--text-muted);
  background: transparent;
}

.ok {
  color: var(--accent-primary);
}
</style>
