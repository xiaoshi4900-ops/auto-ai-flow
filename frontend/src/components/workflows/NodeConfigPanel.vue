<template>
  <div v-if="selectedNode" class="node-config-panel">
    <div class="panel-header">
      <h3>{{ localLabel || selectedNode.node_key }}</h3>
      <el-tag size="small" :color="nodeColor" effect="dark" style="border: none">{{ selectedNode.node_type }}</el-tag>
    </div>

    <el-form label-position="top" size="small">
      <el-form-item label="节点标签">
        <el-input v-model="localLabel" @change="emitChange" />
      </el-form-item>

      <template v-if="selectedNode.node_type === 'agent'">
        <el-form-item label="关联 Agent">
          <el-select v-model="localConfig.agent_id" filterable @change="emitChange">
            <el-option v-for="agent in agents" :key="agent.id" :label="agent.name" :value="agent.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型覆盖 (optional)">
          <el-select v-model="localConfig.model_override_id" clearable filterable @change="emitChange">
            <el-option v-for="model in models" :key="model.id" :label="toModelLabel(model)" :value="model.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Task Instruction">
          <el-input v-model="localConfig.task_instruction" type="textarea" :rows="3" @change="emitChange" />
        </el-form-item>
        <el-form-item label="Input Mapping(JSON)">
          <el-input v-model="inputMappingStr" type="textarea" :rows="3" @change="parseInputMapping" />
        </el-form-item>
        <el-form-item label="Allow Tool Use">
          <el-switch v-model="localConfig.allow_tool_use" @change="emitChange" />
        </el-form-item>
      </template>

      <template v-if="selectedNode.node_type === 'tool'">
        <el-form-item label="关联 Tool">
          <el-select v-model="localConfig.tool_id" filterable @change="emitChange">
            <el-option v-for="tool in tools" :key="tool.id" :label="tool.name" :value="tool.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Input Mapping(JSON)">
          <el-input v-model="inputMappingStr" type="textarea" :rows="3" @change="parseInputMapping" />
        </el-form-item>
      </template>

      <template v-if="selectedNode.node_type === 'condition'">
        <el-form-item label="分支规则">
          <div v-for="(branch, i) in branches" :key="i" class="branch-item">
            <el-input v-model="branch.left_operand" placeholder="left" @change="emitChange" />
            <el-select v-model="branch.operator" style="width: 110px" @change="emitChange">
              <el-option label="==" value="equals" />
              <el-option label="!=" value="not_equals" />
              <el-option label=">" value="greater_than" />
              <el-option label="<" value="less_than" />
              <el-option label="contains" value="contains" />
              <el-option label="exists" value="exists" />
            </el-select>
            <el-input v-model="branch.right_operand" placeholder="right" @change="emitChange" />
            <el-select v-model="branch.target_node_key" filterable placeholder="target" @change="emitChange">
              <el-option v-for="n in nodeOptions" :key="n" :label="n" :value="n" />
            </el-select>
          </div>
          <el-button size="small" @click="addBranch">添加分支</el-button>
        </el-form-item>
        <el-form-item label="默认目标节点">
          <el-select v-model="localConfig.default_target_key" filterable clearable @change="emitChange">
            <el-option v-for="n in nodeOptions" :key="n" :label="n" :value="n" />
          </el-select>
        </el-form-item>
      </template>

      <template v-if="selectedNode.node_type === 'output'">
        <el-form-item label="Source Keys">
          <el-select v-model="localConfig.source_keys" multiple filterable allow-create style="width: 100%" @change="emitChange" />
        </el-form-item>
        <el-form-item label="输出格式">
          <el-select v-model="localConfig.output_format" @change="emitChange">
            <el-option label="Raw" value="raw" />
            <el-option label="JSON" value="json" />
          </el-select>
        </el-form-item>
      </template>
    </el-form>
  </div>
  <div v-else class="node-config-panel empty">
    <p>选择一个节点以编辑配置</p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { NODE_TYPES } from '@/constants/workflow'
import type { WorkflowNode } from '@/types/workflow'
import type { Agent } from '@/types/agent'
import type { Tool } from '@/types/tool'
import type { ModelDefinition } from '@/types/model'
import * as agentApi from '@/api/agent'
import * as toolApi from '@/api/tool'
import * as modelApi from '@/api/model'

const props = defineProps<{
  selectedNode: WorkflowNode | null
  projectId: number | null
  nodeOptions: string[]
}>()

const emit = defineEmits<{
  change: [nodeKey: string, config: Record<string, unknown>, label: string]
}>()

interface BranchRule {
  expression_type: string
  left_operand: string
  operator: string
  right_operand: string
  target_node_key: string
}

const localConfig = ref<Record<string, any>>({})
const localLabel = ref('')
const inputMappingStr = ref('')
const agents = ref<Agent[]>([])
const tools = ref<Tool[]>([])
const models = ref<ModelDefinition[]>([])

const branches = computed<BranchRule[]>(() => (localConfig.value.branches ?? []) as BranchRule[])

const nodeColor = computed(() => {
  if (!props.selectedNode) return '#909399'
  return NODE_TYPES[props.selectedNode.node_type as keyof typeof NODE_TYPES]?.color || '#909399'
})

function toModelLabel(model: ModelDefinition): string {
  return model.name && model.name !== model.model_id ? `${model.name} (${model.model_id})` : model.model_id
}

async function loadBindings() {
  if (!props.projectId) return
  const [agentRes, toolRes, modelRes] = await Promise.all([
    agentApi.listAgents(props.projectId, 1, 200),
    toolApi.listTools(1, 200),
    modelApi.listModels(),
  ])
  agents.value = agentRes.items
  tools.value = toolRes.items
  models.value = modelRes.models
}

watch(
  () => props.selectedNode,
  (node) => {
    if (!node) return
    localLabel.value = node.label || ''
    localConfig.value = { ...(node.config || {}) }
    inputMappingStr.value = node.config?.input_mapping ? JSON.stringify(node.config.input_mapping, null, 2) : ''
  },
  { immediate: true },
)

watch(
  () => props.projectId,
  () => {
    void loadBindings()
  },
  { immediate: true },
)

function emitChange() {
  if (!props.selectedNode) return
  emit('change', props.selectedNode.node_key, { ...localConfig.value }, localLabel.value || props.selectedNode.label || '')
}

function parseInputMapping() {
  try {
    localConfig.value.input_mapping = JSON.parse(inputMappingStr.value)
  } catch {
    // keep current mapping unchanged when invalid JSON
  }
  emitChange()
}

function addBranch() {
  if (!localConfig.value.branches) localConfig.value.branches = []
  ;(localConfig.value.branches as BranchRule[]).push({
    expression_type: 'simple',
    left_operand: '',
    operator: 'equals',
    right_operand: '',
    target_node_key: '',
  })
  emitChange()
}

onMounted(() => {
  void loadBindings()
})
</script>

<style scoped>
.node-config-panel {
  width: 360px;
  padding: 16px;
  background: var(--bg-panel);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  overflow-y: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
}

.empty {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  min-height: 200px;
}

.branch-item {
  display: grid;
  grid-template-columns: 1fr 110px 1fr 1fr;
  gap: 6px;
  margin-bottom: 8px;
  align-items: center;
}
</style>
