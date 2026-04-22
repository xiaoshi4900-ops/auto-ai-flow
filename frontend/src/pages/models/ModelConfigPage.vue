<template>
  <div class="models-page" data-testid="models-workspace-page">
    <section class="glass-card section-card" data-testid="model-config-page">
      <header class="section-header">
        <h2>模型配置</h2>
        <button class="primary-btn" data-testid="model-add-config-btn" @click="openAddDialog">新增配置</button>
      </header>
      <div class="table-list" data-testid="model-config-table">
        <div class="table-row table-row--head">
          <span data-testid="model-col-provider">Provider</span>
          <span data-testid="model-col-model">Model</span>
          <span data-testid="model-col-status">状态</span>
          <span data-testid="model-col-key">密钥</span>
        </div>
        <template v-if="configs.length">
          <div v-for="cfg in configs" :key="cfg.id" class="table-row" :data-testid="`model-row-${cfg.id}`">
            <span>{{ getProviderForModel(cfg.model_definition_id)?.name || '-' }}</span>
            <span>{{ getModelDefinition(cfg.model_definition_id)?.display_name || '-' }}</span>
            <span :class="cfg.is_default ? 'ok' : ''">{{ cfg.is_default ? 'default' : 'active' }}</span>
            <span>已托管</span>
          </div>
        </template>
        <div v-if="!configs.length" class="empty-card" data-testid="model-empty-state">暂无模型配置，请先添加。</div>
      </div>
    </section>

    <el-dialog v-model="showAddDialog" title="Add Model Config" class="workspace-dialog">
      <el-form :model="addForm">
        <el-form-item label="Model">
          <el-select v-model="addForm.model_definition_id" placeholder="Select model">
            <el-option
              v-for="m in availableModels"
              :key="m.id"
              :label="m.display_name || m.model_name"
              :value="m.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">Cancel</el-button>
        <el-button type="primary" @click="handleAddConfig">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import * as modelApi from '@/api/model'
import type { ModelProvider, ModelDefinition, ProjectModelConfig } from '@/types/model'
import { ElMessage } from 'element-plus'

const providers = ref<ModelProvider[]>([])
const models = ref<ModelDefinition[]>([])
const configs = ref<ProjectModelConfig[]>([])
const showAddDialog = ref(false)
const addForm = ref({ model_definition_id: null as number | null })

const availableModels = computed(() => models.value)

function getProviderForModel(modelDefinitionId: number): ModelProvider | undefined {
  const modelDef = models.value.find((m) => m.id === modelDefinitionId)
  if (!modelDef) return undefined
  return providers.value.find((p) => p.id === modelDef.provider_id)
}

function getModelDefinition(modelDefinitionId: number): ModelDefinition | undefined {
  return models.value.find((m) => m.id === modelDefinitionId)
}

onMounted(async () => {
  await loadData()
})

async function loadData() {
  const projectId = 1
  const [modelList, configList] = await Promise.all([
    modelApi.listModels(),
    modelApi.listProjectModelConfigs(projectId),
  ])
  providers.value = modelList.providers
  models.value = modelList.models
  configs.value = configList
}

function openAddDialog() {
  addForm.value = { model_definition_id: availableModels.value.length ? availableModels.value[0].id : null }
  showAddDialog.value = true
}

async function handleAddConfig() {
  const projectId = 1
  await modelApi.createProjectModelConfig(projectId, {
    model_definition_id: addForm.value.model_definition_id ?? 0,
  })
  ElMessage.success('Model config added')
  showAddDialog.value = false
  addForm.value = { model_definition_id: null }
  await loadData()
}
</script>

<style scoped>
.models-page {
  padding: 20px 24px;
}

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

.section-header h2 {
  margin: 0;
}

.primary-btn {
  background: var(--accent-primary);
  color: var(--bg-dark);
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.primary-btn:hover {
  opacity: 0.85;
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

.empty-card {
  color: var(--text-muted);
  text-align: center;
  padding: 40px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
}

@media (max-width: 960px) {
  .models-page {
    padding: 16px;
  }
}
</style>

<style>
.workspace-dialog .el-dialog {
  background-color: rgba(28, 32, 42, 0.98) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 20px !important;
  backdrop-filter: blur(10px);
}

.workspace-dialog .el-dialog__header {
  color: var(--text-primary) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.workspace-dialog .el-dialog__title {
  color: var(--text-primary) !important;
}

.workspace-dialog .el-dialog__body {
  color: var(--text-primary) !important;
}

.workspace-dialog .el-input__wrapper,
.workspace-dialog .el-textarea__inner,
.workspace-dialog .el-select__wrapper {
  background-color: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: var(--text-primary) !important;
  border-radius: 12px !important;
}

.workspace-dialog .el-input__wrapper:hover,
.workspace-dialog .el-textarea__inner:hover,
.workspace-dialog .el-select__wrapper:hover {
  border-color: rgba(86, 240, 192, 0.3) !important;
}

.workspace-dialog .el-input__wrapper.is-focus,
.workspace-dialog .el-textarea__inner:focus,
.workspace-dialog .el-select__wrapper.is-focus {
  box-shadow: 0 0 0 2px rgba(86, 240, 192, 0.2) !important;
  border-color: rgba(86, 240, 192, 0.5) !important;
}

.workspace-dialog .el-input__inner,
.workspace-dialog .el-textarea__inner {
  color: var(--text-primary) !important;
}

.workspace-dialog .el-input__inner::placeholder,
.workspace-dialog .el-textarea__inner::placeholder {
  color: var(--text-secondary) !important;
}

.workspace-dialog .el-dialog__footer {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.workspace-dialog .el-button {
  border-radius: 12px !important;
}
</style>
