<template>
  <div class="vue-flow-wrapper">
    <VueFlow
      v-model:nodes="flowNodes"
      v-model:edges="flowEdges"
      :default-viewport="{ zoom: 1, x: 0, y: 0 }"
      :min-zoom="0.2"
      :max-zoom="2"
      fit-view-on-init
      @node-click="onNodeClick"
      @connect="onConnect"
    >
      <Background :gap="24" />
      <Controls />
      <template #node-start="nodeProps">
        <StartNode :data="nodeProps.data" :selected="nodeProps.selected" />
      </template>
      <template #node-input="nodeProps">
        <InputNode :data="nodeProps.data" :selected="nodeProps.selected" />
      </template>
      <template #node-agent="nodeProps">
        <AgentNode :data="nodeProps.data" :selected="nodeProps.selected" />
      </template>
      <template #node-condition="nodeProps">
        <ConditionNode :data="nodeProps.data" :selected="nodeProps.selected" />
      </template>
      <template #node-output="nodeProps">
        <OutputNode :data="nodeProps.data" :selected="nodeProps.selected" />
      </template>
      <template #node-tool="nodeProps">
        <ToolNode :data="nodeProps.data" :selected="nodeProps.selected" />
      </template>
    </VueFlow>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import StartNode from './nodes/StartNode.vue'
import InputNode from './nodes/InputNode.vue'
import AgentNode from './nodes/AgentNode.vue'
import ConditionNode from './nodes/ConditionNode.vue'
import OutputNode from './nodes/OutputNode.vue'
import ToolNode from './nodes/ToolNode.vue'
import type { NodeMouseEvent } from '@vue-flow/core'
import type { WorkflowNode, WorkflowEdge } from '@/types/workflow'

const props = defineProps<{
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
}>()

const emit = defineEmits<{
  nodeClick: [nodeKey: string]
  connect: [source: string, target: string]
}>()

const NODE_COLORS: Record<string, string> = {
  start: '#67C23A',
  input: '#409EFF',
  agent: '#E6A23C',
  condition: '#F56C6C',
  output: '#909399',
  tool: '#9B59B6',
}

const flowNodes = computed(() =>
  props.nodes.map((n, i) => ({
    id: n.node_key,
    type: n.node_type,
    position: { x: n.position_x || 100 + i * 200, y: n.position_y || 100 + i * 100 },
    data: { label: n.label || n.node_key, config: n.config, color: NODE_COLORS[n.node_type] || '#909399' },
  })),
)

const flowEdges = computed(() =>
  props.edges.map((e) => ({
    id: `${e.source_node_key}-${e.target_node_key}`,
    source: e.source_node_key,
    target: e.target_node_key,
    label: e.label || undefined,
    animated: true,
    style: { stroke: '#3cb9ff' },
  })),
)

function onNodeClick(nodeMouseEvent: NodeMouseEvent) {
  emit('nodeClick', nodeMouseEvent.node.id)
}

function onConnect(params: { source: string; target: string }) {
  emit('connect', params.source, params.target)
}
</script>

<style scoped>
.vue-flow-wrapper {
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: var(--bg-shell);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-soft);
}
</style>
