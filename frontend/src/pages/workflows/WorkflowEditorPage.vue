<template>
  <div class="workflow-editor-page" data-testid="workflow-editor-page">
    <div class="editor-toolbar" data-testid="editor-toolbar">
      <div class="toolbar-left" data-testid="toolbar-left">
        <el-button data-testid="editor-btn-back" @click="$router.back()">← 返回</el-button>
        <h2 data-testid="editor-workflow-name">{{ currentWorkflow?.name || 'Workflow Editor' }}</h2>
      </div>
      <div class="toolbar-right" data-testid="toolbar-right">
        <el-button type="primary" data-testid="editor-btn-save" @click="handleSave" :loading="saving">保存</el-button>
        <el-button type="success" data-testid="editor-btn-run" @click="handleRun" :loading="running">运行</el-button>
      </div>
    </div>
    <div class="editor-body" data-testid="editor-body">
      <NodePalette data-testid="node-palette" />
      <div class="canvas-container" data-testid="canvas-container" @drop="onDrop" @dragover.prevent>
        <WorkflowCanvas
          data-testid="workflow-canvas"
          v-if="currentWorkflow"
          :nodes="currentWorkflow.nodes"
          :edges="currentWorkflow.edges"
          @node-click="onNodeClick"
          @connect="onConnect"
        />
      </div>
      <NodeConfigPanel
        data-testid="node-config-panel"
        :selected-node="selectedNode"
        @change="onConfigChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useWorkflowStore } from '@/stores/workflow'
import { useRunStore } from '@/stores/run'
import WorkflowCanvas from '@/components/workflows/WorkflowCanvas.vue'
import NodePalette from '@/components/workflows/NodePalette.vue'
import NodeConfigPanel from '@/components/workflows/NodeConfigPanel.vue'
import type { WorkflowNode } from '@/types/workflow'
import { ElMessage } from 'element-plus'

const route = useRoute()
const workflowStore = useWorkflowStore()
const runStore = useRunStore()
const { currentWorkflow } = storeToRefs(workflowStore)
const selectedNode = ref<WorkflowNode | null>(null)
const saving = ref(false)
const running = ref(false)

onMounted(async () => {
  const id = Number(route.params.id)
  await workflowStore.fetchWorkflow(id)
})

function onNodeClick(nodeKey: string) {
  if (!currentWorkflow.value) return
  selectedNode.value = currentWorkflow.value.nodes.find((n) => n.node_key === nodeKey) || null
}

function onConnect(source: string, target: string) {
  if (!currentWorkflow.value) return
  currentWorkflow.value.edges.push({
    source_node_key: source,
    target_node_key: target,
    condition: null,
    label: null,
  })
}

function onDrop(event: DragEvent) {
  const nodeType = event.dataTransfer?.getData('nodeType')
  if (!nodeType || !currentWorkflow.value) return
  const count = currentWorkflow.value.nodes.length + 1
  const nodeKey = `${nodeType}_${count}`
  currentWorkflow.value.nodes.push({
    node_key: nodeKey,
    node_type: nodeType,
    label: null,
    config: {},
    position_x: 100 + count * 50,
    position_y: 100 + count * 30,
  })
}

function onConfigChange(nodeKey: string, config: Record<string, unknown>, label: string) {
  if (!currentWorkflow.value) return
  const node = currentWorkflow.value.nodes.find((n) => n.node_key === nodeKey)
  if (node) {
    node.config = config
    node.label = label || node.label
  }
}

async function handleSave() {
  if (!currentWorkflow.value) return
  saving.value = true
  try {
    await workflowStore.updateWorkflow(currentWorkflow.value.id, {
      name: currentWorkflow.value.name,
      nodes: currentWorkflow.value.nodes,
      edges: currentWorkflow.value.edges,
    })
    ElMessage.success('Workflow 已保存')
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

async function handleRun() {
  if (!currentWorkflow.value) return
  running.value = true
  try {
    const res = await runStore.triggerExecution(currentWorkflow.value.id)
    ElMessage.success(`运行已触发: Run #${res.run_id}`)
  } catch {
    ElMessage.error('运行触发失败')
  } finally {
    running.value = false
  }
}
</script>

<style scoped>
.workflow-editor-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
}
.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-soft);
}
.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.toolbar-left h2 {
  margin: 0;
  font-size: 18px;
}
.toolbar-right {
  display: flex;
  gap: 8px;
}
.editor-body {
  display: flex;
  flex: 1;
  gap: 0;
  overflow: hidden;
}
.canvas-container {
  flex: 1;
  min-width: 0;
}
</style>
