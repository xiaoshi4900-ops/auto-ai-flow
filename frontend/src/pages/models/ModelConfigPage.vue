<template>
  <div class="models-page" data-testid="models-workspace-page">
    <section class="glass-card section-card" data-testid="model-config-page">
      <header class="section-header">
        <div class="title-row">
          <h2>模型配置</h2>
          <select v-model.number="selectedProjectId" class="native-select project-select" @change="loadData">
            <option v-for="p in projectStore.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="header-actions">
          <button class="ghost-btn" data-testid="model-add-provider-btn" @click="openProviderDialog">新增 Provider</button>
          <button class="ghost-btn" data-testid="model-add-definition-btn" @click="openModelDialog">新增模型</button>
          <button class="primary-btn" data-testid="model-add-config-btn" @click="openAddDialog">新增配置</button>
        </div>
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
            <span>{{ getProviderName(cfg.model_definition_id) }}</span>
            <span>{{ getModelLabel(cfg) }}</span>
            <span :class="cfg.is_default ? 'ok' : ''">{{ cfg.is_default ? 'default' : 'active' }}</span>
            <span>{{ cfg.has_api_key ? '已配置' : '未配置' }}</span>
          </div>
        </template>
        <div v-else class="empty-card" data-testid="model-empty-state">
          当前项目暂无模型配置，请先添加。
        </div>
      </div>
    </section>

    <div v-if="showAddDialog" class="dialog-overlay" @click.self="showAddDialog = false">
      <div role="dialog" aria-label="Add Model Config" class="dialog-panel">
        <div class="dialog-header">
          <h2>Add Model Config</h2>
          <button class="dialog-close" @click="showAddDialog = false">x</button>
        </div>
        <div class="dialog-body">
          <label class="form-label">Model</label>
          <select v-model="addForm.model_definition_id" class="native-select" :disabled="!availableModels.length">
            <option v-for="m in availableModels" :key="m.id" :value="m.id">{{ toModelLabel(m) }}</option>
          </select>
          <p v-if="!availableModels.length" class="hint-text">暂无模型定义，请先点击“新增模型”。</p>

          <label class="form-label">API Key (optional)</label>
          <input v-model="addForm.api_key" class="native-input" type="password" placeholder="sk-..." autocomplete="off" />

          <label class="form-label">Base URL (optional)</label>
          <input
            v-model="addForm.api_base_url"
            class="native-input"
            type="text"
            placeholder="https://api.vendor.com/v1"
            autocomplete="off"
          />

          <label class="form-label">Override Model ID (optional)</label>
          <input
            v-model="addForm.override_model_id"
            class="native-input"
            type="text"
            placeholder="vendor-chat-model"
            autocomplete="off"
          />

          <label class="switch-row">
            <input v-model="addForm.is_default" type="checkbox" />
            <span>Set as default</span>
          </label>
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="showAddDialog = false">Cancel</button>
          <button class="btn-confirm" :disabled="!canSubmit || submitting" @click="handleAddConfig">
            {{ submitting ? 'Submitting...' : 'Confirm' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showProviderDialog" class="dialog-overlay" @click.self="showProviderDialog = false">
      <div role="dialog" aria-label="Add Provider" class="dialog-panel">
        <div class="dialog-header">
          <h2>Add Provider</h2>
          <button class="dialog-close" @click="showProviderDialog = false">x</button>
        </div>
        <div class="dialog-body">
          <label class="form-label">Provider Name</label>
          <input v-model="providerForm.name" class="native-input" type="text" placeholder="My Vendor" />
          <label class="form-label">Provider Type</label>
          <input v-model="providerForm.provider_type" class="native-input" type="text" placeholder="openai_compatible" />
          <label class="form-label">Default Base URL (optional)</label>
          <input v-model="providerForm.api_base" class="native-input" type="text" placeholder="https://api.vendor.com/v1" />
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="showProviderDialog = false">Cancel</button>
          <button class="btn-confirm" :disabled="creatingProvider" @click="handleCreateProvider">
            {{ creatingProvider ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showModelDialog" class="dialog-overlay" @click.self="showModelDialog = false">
      <div role="dialog" aria-label="Add Model Definition" class="dialog-panel">
        <div class="dialog-header">
          <h2>Add Model Definition</h2>
          <button class="dialog-close" @click="showModelDialog = false">x</button>
        </div>
        <div class="dialog-body">
          <label class="form-label">Provider</label>
          <select v-model="modelForm.provider_id" class="native-select" :disabled="!providers.length">
            <option v-for="p in providers" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <label class="form-label">Display Name</label>
          <input v-model="modelForm.name" class="native-input" type="text" placeholder="Vendor Chat Model" />
          <label class="form-label">Model ID</label>
          <input v-model="modelForm.model_id" class="native-input" type="text" placeholder="vendor-chat-model" />
          <label class="form-label">Description (optional)</label>
          <input v-model="modelForm.description" class="native-input" type="text" placeholder="internal model" />
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="showModelDialog = false">Cancel</button>
          <button class="btn-confirm" :disabled="creatingModel || !providers.length" @click="handleCreateModelDefinition">
            {{ creatingModel ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as modelApi from '@/api/model'
import type { ModelDefinition, ModelProvider, ProjectModelConfig } from '@/types/model'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()
const selectedProjectId = ref<number>(1)
const providers = ref<ModelProvider[]>([])
const models = ref<ModelDefinition[]>([])
const configs = ref<ProjectModelConfig[]>([])

const showAddDialog = ref(false)
const showProviderDialog = ref(false)
const showModelDialog = ref(false)
const submitting = ref(false)
const creatingProvider = ref(false)
const creatingModel = ref(false)

const addForm = ref({
  model_definition_id: null as number | null,
  api_key: '',
  api_base_url: '',
  override_model_id: '',
  is_default: false,
})
const providerForm = ref({ name: '', provider_type: 'openai_compatible', api_base: '' })
const modelForm = ref({ provider_id: null as number | null, name: '', model_id: '', description: '' })

const availableModels = computed(() => models.value)
const canSubmit = computed(() => addForm.value.model_definition_id !== null && selectedProjectId.value > 0)

function getModelDefinition(modelDefinitionId: number): ModelDefinition | undefined {
  return models.value.find((m) => m.id === modelDefinitionId)
}

function getProviderForModel(modelDefinitionId: number): ModelProvider | undefined {
  const modelDef = getModelDefinition(modelDefinitionId)
  if (!modelDef) return undefined
  return providers.value.find((p) => p.id === modelDef.provider_id)
}

function toModelLabel(modelDef: ModelDefinition): string {
  const title = modelDef.name || modelDef.model_id || '-'
  if (modelDef.model_id && modelDef.model_id !== title) {
    return `${title} (${modelDef.model_id})`
  }
  return title
}

function getModelLabel(config: ProjectModelConfig): string {
  const modelDef = getModelDefinition(config.model_definition_id)
  if (!modelDef) return '-'
  const custom = config.custom_config && typeof config.custom_config === 'object' ? config.custom_config : null
  const overrideModelId = custom && typeof custom.model_id === 'string' ? custom.model_id : ''
  if (overrideModelId) return `${toModelLabel(modelDef)} -> ${overrideModelId}`
  return toModelLabel(modelDef)
}

function getProviderName(modelDefinitionId: number): string {
  return getProviderForModel(modelDefinitionId)?.name || '-'
}

async function loadProjects() {
  await projectStore.fetchProjects()
  if (projectStore.projects.length && !projectStore.projects.some((p) => p.id === selectedProjectId.value)) {
    selectedProjectId.value = projectStore.projects[0].id
  }
}

async function loadData() {
  if (!selectedProjectId.value) return
  try {
    const [modelList, configList] = await Promise.all([
      modelApi.listModels(),
      modelApi.listProjectModelConfigs(selectedProjectId.value),
    ])
    providers.value = modelList.providers
    models.value = modelList.models
    configs.value = configList
    if (providers.value.length && !modelForm.value.provider_id) {
      modelForm.value.provider_id = providers.value[0].id
    }
  } catch (err) {
    console.error('load model config data failed', err)
    ElMessage.error('加载模型配置失败')
  }
}

function openAddDialog() {
  addForm.value = {
    model_definition_id: availableModels.value.length ? availableModels.value[0].id : null,
    api_key: '',
    api_base_url: '',
    override_model_id: '',
    is_default: false,
  }
  showAddDialog.value = true
}

function openProviderDialog() {
  providerForm.value = { name: '', provider_type: 'openai_compatible', api_base: '' }
  showProviderDialog.value = true
}

function openModelDialog() {
  modelForm.value = {
    provider_id: providers.value.length ? providers.value[0].id : null,
    name: '',
    model_id: '',
    description: '',
  }
  showModelDialog.value = true
}

async function handleAddConfig() {
  if (!canSubmit.value || submitting.value) return
  submitting.value = true
  try {
    const customConfig: Record<string, unknown> = {}
    if (addForm.value.api_base_url.trim()) customConfig.api_base_url = addForm.value.api_base_url.trim()
    if (addForm.value.override_model_id.trim()) customConfig.model_id = addForm.value.override_model_id.trim()
    await modelApi.createProjectModelConfig(selectedProjectId.value, {
      model_definition_id: addForm.value.model_definition_id as number,
      api_key: addForm.value.api_key || null,
      custom_config: Object.keys(customConfig).length ? customConfig : undefined,
      is_default: addForm.value.is_default,
    })
    ElMessage.success('Model config added')
    showAddDialog.value = false
    await loadData()
  } catch (err) {
    console.error('create project model config failed', err)
    ElMessage.error('新增模型配置失败')
  } finally {
    submitting.value = false
  }
}

async function handleCreateProvider() {
  if (!providerForm.value.name.trim() || creatingProvider.value) return
  creatingProvider.value = true
  try {
    await modelApi.createModelProvider({
      name: providerForm.value.name.trim(),
      provider_type: providerForm.value.provider_type.trim() || 'openai_compatible',
      api_base: providerForm.value.api_base.trim() || null,
    })
    ElMessage.success('Provider created')
    showProviderDialog.value = false
    await loadData()
  } catch (err) {
    console.error('create model provider failed', err)
    ElMessage.error('新增 Provider 失败')
  } finally {
    creatingProvider.value = false
  }
}

async function handleCreateModelDefinition() {
  if (!modelForm.value.provider_id || !modelForm.value.name.trim() || !modelForm.value.model_id.trim() || creatingModel.value) return
  creatingModel.value = true
  try {
    await modelApi.createModelDefinition({
      provider_id: modelForm.value.provider_id,
      name: modelForm.value.name.trim(),
      model_id: modelForm.value.model_id.trim(),
      description: modelForm.value.description.trim() || null,
    })
    ElMessage.success('Model definition created')
    showModelDialog.value = false
    await loadData()
  } catch (err) {
    console.error('create model definition failed', err)
    ElMessage.error('新增模型定义失败')
  } finally {
    creatingModel.value = false
  }
}

onMounted(async () => {
  await loadProjects()
  await loadData()
})
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
  gap: 16px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-header h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.primary-btn,
.ghost-btn {
  border: none;
  padding: 10px 16px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.primary-btn {
  background: var(--accent-primary);
  color: var(--bg-dark);
}

.ghost-btn {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-primary);
  border: 1px solid var(--border-soft);
}

.primary-btn:hover,
.ghost-btn:hover {
  opacity: 0.85;
}

.project-select {
  min-width: 220px;
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

.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.dialog-panel {
  background: rgba(28, 32, 42, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  width: 520px;
  max-width: 92vw;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.dialog-header h2 {
  margin: 0;
  font-size: 16px;
  color: var(--text-primary);
}

.dialog-close {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 16px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
}

.dialog-close:hover {
  background: rgba(255, 255, 255, 0.05);
}

.dialog-body {
  padding: 20px;
}

.form-label {
  display: block;
  color: var(--text-secondary);
  font-size: 13px;
  margin-top: 10px;
  margin-bottom: 6px;
}

.native-select,
.native-input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.native-select:focus,
.native-input:focus {
  border-color: rgba(86, 240, 192, 0.5);
  box-shadow: 0 0 0 2px rgba(86, 240, 192, 0.2);
}

.hint-text {
  margin: 8px 0 0;
  color: var(--text-muted);
  font-size: 12px;
}

.switch-row {
  margin-top: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-cancel,
.btn-confirm {
  padding: 8px 20px;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-cancel {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.btn-cancel:hover {
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-confirm {
  background: var(--accent-primary);
  border: none;
  color: var(--bg-dark);
  font-weight: 600;
}

.btn-confirm:hover:not(:disabled) {
  opacity: 0.85;
}

.btn-confirm:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

@media (max-width: 1200px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 960px) {
  .models-page {
    padding: 16px;
  }
  .table-row {
    grid-template-columns: 1fr;
  }
}
</style>
