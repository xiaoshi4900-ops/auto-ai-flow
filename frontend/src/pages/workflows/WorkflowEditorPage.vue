<template>
  <div class="workflow-editor-page" data-testid="workflow-editor-page">
    <div class="editor-toolbar" data-testid="editor-toolbar">
      <div class="toolbar-left" data-testid="toolbar-left">
        <button class="ghost-btn" data-testid="editor-btn-back" @click="$router.back()">返回</button>
        <h2 data-testid="editor-workflow-name">{{ currentWorkflow?.name || 'Workflow Editor' }}</h2>
        <span v-if="currentWorkflow" class="meta-chip">Project {{ currentWorkflow.project_id }}</span>
      </div>
      <div class="toolbar-right" data-testid="toolbar-right">
        <button class="ghost-btn" data-testid="editor-btn-save" @click="handleSave" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <button class="primary-btn" data-testid="editor-btn-run" @click="handleRun" :disabled="running">
          {{ running ? '运行中...' : '运行' }}
        </button>
      </div>
    </div>

    <div class="editor-body" data-testid="editor-body">
      <NodePalette data-testid="node-palette" />
      <div class="canvas-container" data-testid="canvas-container" @drop="onDrop" @dragover.prevent>
        <WorkflowCanvas
          v-if="currentWorkflow"
          data-testid="workflow-canvas"
          :nodes="currentWorkflow.nodes"
          :edges="currentWorkflow.edges"
          @node-click="onNodeClick"
          @connect="onConnect"
        />
      </div>
      <NodeConfigPanel
        data-testid="node-config-panel"
        :selected-node="selectedNode"
        :project-id="currentWorkflow?.project_id ?? null"
        :node-options="nodeKeys"
        @change="onConfigChange"
      />
    </div>

    <div v-if="currentWorkflow" class="edge-panel glass-card" data-testid="workflow-edge-list">
      <div class="edge-panel-header">
        <h3>节点关系</h3>
        <span>{{ currentWorkflow.edges.length }} 条连线</span>
      </div>
      <div v-if="currentWorkflow.edges.length" class="edge-list">
        <div v-for="(edge, idx) in currentWorkflow.edges" :key="`${edge.source_node_key}-${edge.target_node_key}-${idx}`" class="edge-item">
          <span>{{ edge.source_node_key }} -> {{ edge.target_node_key }}</span>
          <button class="danger-link" @click="removeEdge(idx)">移除</button>
        </div>
      </div>
      <div v-else class="edge-empty">还没有节点连接，先拖节点并连线。</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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

const nodeKeys = computed(() => (currentWorkflow.value?.nodes || []).map((n) => n.node_key))

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
  if (source === target) {
    ElMessage.warning('不允许自环连接')
    return
  }
  const exists = currentWorkflow.value.edges.some((e) => e.source_node_key === source && e.target_node_key === target)
  if (exists) return
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
  if (nodeType === 'start' && currentWorkflow.value.nodes.some((n) => n.node_type === 'start')) {
    ElMessage.warning('只能有一个 start 节点')
    return
  }
  const count = currentWorkflow.value.nodes.length + 1
  const nodeKey = `${nodeType}_${count}`
  currentWorkflow.value.nodes.push({
    node_key: nodeKey,
    node_type: nodeType,
    label: `${nodeType}_${count}`,
    config: {},
    position_x: 100 + count * 50,
    position_y: 100 + count * 30,
  })
}

function onConfigChange(nodeKey: string, config: Record<string, unknown>, label: string) {
  if (!currentWorkflow.value) return
  const node = currentWorkflow.value.nodes.find((n) => n.node_key === nodeKey)
  if (!node) return
  node.config = config
  node.label = label
}

function removeEdge(idx: number) {
  if (!currentWorkflow.value) return
  currentWorkflow.value.edges.splice(idx, 1)
}

async function handleSave() {
  if (!currentWorkflow.value) return
  saving.value = true
  try {
    await workflowStore.updateWorkflow(currentWorkflow.value.id, {
      name: currentWorkflow.value.name,
      description: currentWorkflow.value.description || undefined,
      nodes: currentWorkflow.value.nodes,
      edges: currentWorkflow.value.edges,
    })
    ElMessage.success('Workflow 已保存')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleRun() {
  if (!currentWorkflow.value) return
  running.value = true
  try {
    const res = await runStore.triggerExecution(currentWorkflow.value.id)
    ElMessage.success(`运行已触发 Run #${res.run_id}`)
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
  gap: 12px;
  height: calc(100vh - 120px);
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: var(--bg-panel);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toolbar-left h2 {
  margin: 0;
  font-size: 18px;
}

.meta-chip {
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 12px;
}

.toolbar-right {
  display: flex;
  gap: 8px;
}

.ghost-btn,
.primary-btn {
  border: none;
  padding: 8px 14px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.ghost-btn {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-primary);
}

.primary-btn {
  background: var(--accent-primary);
  color: var(--bg-dark);
}

.editor-body {
  display: flex;
  flex: 1;
  gap: 12px;
  overflow: hidden;
}

.canvas-container {
  flex: 1;
  min-width: 0;
}

.edge-panel {
  padding: 12px 16px;
  border-radius: 14px;
  border: 1px solid var(--border-soft);
}

.edge-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.edge-panel-header h3 {
  margin: 0;
  font-size: 14px;
}

.edge-list {
  margin-top: 10px;
  display: grid;
  gap: 8px;
}

.edge-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
}

.danger-link {
  border: none;
  background: transparent;
  color: rgba(255, 107, 107, 0.92);
  cursor: pointer;
}

.edge-empty {
  margin-top: 8px;
  color: var(--text-muted);
  font-size: 13px;
}
</style>
