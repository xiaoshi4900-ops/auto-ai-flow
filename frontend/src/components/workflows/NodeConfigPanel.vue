<template>
  <div v-if="selectedNode" class="node-config-panel">
    <div class="panel-header">
      <h3>{{ selectedNode.label || selectedNode.node_key }}</h3>
      <el-tag size="small" :color="nodeColor" effect="dark" style="border: none">{{ selectedNode.node_type }}</el-tag>
    </div>

    <el-form label-position="top" size="small">
      <el-form-item label="节点标签">
        <el-input v-model="localConfig.label" @change="emitChange" />
      </el-form-item>

      <template v-if="selectedNode.node_type === 'agent'">
        <el-form-item label="Agent ID">
          <el-input-number v-model="localConfig.agent_id" :min="1" @change="emitChange" />
        </el-form-item>
        <el-form-item label="Task Instruction">
          <el-input v-model="localConfig.task_instruction" type="textarea" :rows="3" @change="emitChange" />
        </el-form-item>
        <el-form-item label="Input Mapping">
          <el-input v-model="inputMappingStr" type="textarea" :rows="2" @change="parseInputMapping" />
        </el-form-item>
        <el-form-item label="Allow Tool Use">
          <el-switch v-model="localConfig.allow_tool_use" @change="emitChange" />
        </el-form-item>
      </template>

      <template v-if="selectedNode.node_type === 'condition'">
        <el-form-item label="分支规则">
          <div v-for="(branch, i) in branches" :key="i" class="branch-item">
            <el-input v-model="branch.left_operand" placeholder="左操作数" @change="emitChange" />
            <el-select v-model="branch.operator" style="width: 120px" @change="emitChange">
              <el-option label="等于" value="equals" />
              <el-option label="不等于" value="not_equals" />
              <el-option label="大于" value="greater_than" />
              <el-option label="小于" value="less_than" />
              <el-option label="包含" value="contains" />
              <el-option label="存在" value="exists" />
            </el-select>
            <el-input v-model="branch.right_operand" placeholder="右操作数" @change="emitChange" />
            <el-input v-model="branch.target_node_key" placeholder="目标节点" @change="emitChange" />
          </div>
          <el-button size="small" @click="addBranch">添加分支</el-button>
        </el-form-item>
        <el-form-item label="默认目标节点">
          <el-input v-model="localConfig.default_target_key" @change="emitChange" />
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

      <template v-if="selectedNode.node_type === 'input'">
        <el-form-item label="Input Mapping">
          <el-input v-model="inputMappingStr" type="textarea" :rows="3" @change="parseInputMapping" />
        </el-form-item>
      </template>

      <template v-if="selectedNode.node_type === 'tool'">
        <el-form-item label="Tool ID">
          <el-input-number v-model="localConfig.tool_id" :min="1" @change="emitChange" />
        </el-form-item>
        <el-form-item label="Input Mapping">
          <el-input v-model="inputMappingStr" type="textarea" :rows="2" @change="parseInputMapping" />
        </el-form-item>
      </template>
    </el-form>
  </div>
  <div v-else class="node-config-panel empty">
    <p>选择一个节点以编辑配置</p>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { NODE_TYPES } from '@/constants/workflow'
import type { WorkflowNode } from '@/types/workflow'

const props = defineProps<{
  selectedNode: WorkflowNode | null
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

const localConfig = ref<Record<string, unknown>>({})
const branches = computed<BranchRule[]>(() => (localConfig.value.branches ?? []) as BranchRule[])
const inputMappingStr = ref('')

const nodeColor = computed(() => {
  if (!props.selectedNode) return '#909399'
  return NODE_TYPES[props.selectedNode.node_type as keyof typeof NODE_TYPES]?.color || '#909399'
})

watch(
  () => props.selectedNode,
  (node) => {
    if (node) {
      localConfig.value = { ...node.config, label: node.label || '' }
      inputMappingStr.value = node.config?.input_mapping ? JSON.stringify(node.config.input_mapping, null, 2) : ''
    }
  },
  { immediate: true },
)

function emitChange() {
  if (!props.selectedNode) return
  const { label, ...config } = localConfig.value
  emit('change', props.selectedNode.node_key, config as Record<string, unknown>, String(label || ''))
}

function parseInputMapping() {
  try {
    localConfig.value.input_mapping = JSON.parse(inputMappingStr.value)
  } catch {
    // keep raw string
  }
  emitChange()
}

function addBranch() {
  if (!localConfig.value.branches) {
    localConfig.value.branches = []
  }
  ;(localConfig.value.branches as BranchRule[]).push({
    expression_type: 'simple',
    left_operand: '',
    operator: 'equals',
    right_operand: '',
    target_node_key: '',
  })
  emitChange()
}
</script>

<style scoped>
.node-config-panel {
  width: 320px;
  padding: 16px;
  background: var(--bg-panel);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  overflow-y: auto;
  max-height: 600px;
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
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
  align-items: center;
}
.branch-item .el-input,
.branch-item .el-select {
  flex: 1;
}
</style>
