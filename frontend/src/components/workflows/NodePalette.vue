<template>
  <div class="node-palette">
    <h4>节点面板</h4>
    <div
      v-for="(info, type) in NODE_TYPES"
      :key="type"
      class="palette-item"
      draggable="true"
      @dragstart="onDragStart($event, type)"
    >
      <span class="palette-dot" :style="{ background: info.color }"></span>
      <span>{{ info.label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NODE_TYPES } from '@/constants/workflow'

function onDragStart(event: DragEvent, type: string) {
  event.dataTransfer?.setData('nodeType', type)
}
</script>

<style scoped>
.node-palette {
  width: 180px;
  padding: 16px;
  background: var(--bg-panel);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
}
.node-palette h4 {
  margin: 0 0 12px;
  color: var(--text-secondary);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.palette-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  margin-bottom: 6px;
  border-radius: var(--radius-sm);
  cursor: grab;
  color: var(--text-primary);
  font-size: 14px;
  background: var(--bg-muted);
  border: 1px solid transparent;
  transition: all 0.15s;
}
.palette-item:hover {
  background: var(--bg-elevated);
  border-color: var(--border-soft);
}
.palette-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
</style>
