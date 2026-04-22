<template>
  <div class="flow-node output-node" :class="{ selected }">
    <div class="node-icon">📤</div>
    <div class="node-label">{{ data.label }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ data: { label: string; color?: string }; selected?: boolean }>()
</script>

<style scoped>
.flow-node {
  padding: 10px 20px;
  border-radius: 12px;
  background: var(--bg-panel-strong);
  border: 2px solid #909399;
  color: var(--text-primary);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
}
.flow-node.selected {
  box-shadow: 0 0 0 2px rgba(144, 147, 153, 0.5);
}
</style>
