<template>
  <div class="project-detail-page" data-testid="project-detail-page">
    <section class="detail-grid">
      <div class="glass-card section-card" data-testid="project-summary-panel">
        <span class="chip" data-testid="project-summary-status">active</span>
        <h2 data-testid="project-summary-name">{{ currentProject?.name || '项目' }}</h2>
        <p data-testid="project-summary-description">{{ currentProject?.description || '-' }}</p>
        <div class="meta-grid" data-testid="project-summary-meta-grid">
          <div data-testid="project-summary-meta-model">
            <span>默认模型</span>
            <strong>{{ currentProject?.default_model_id ?? '-' }}</strong>
          </div>
          <div data-testid="project-summary-meta-updated">
            <span>最近更新</span>
            <strong>{{ currentProject?.updated_at || '-' }}</strong>
          </div>
        </div>
      </div>
      <div class="glass-card section-card" data-testid="project-quick-stats">
        <h2>快速统计</h2>
        <div class="dashboard-row">
          <div class="mini-stat" data-testid="project-quick-stats-agents">
            <span>Agents</span>
            <strong>{{ agents.length }}</strong>
          </div>
          <div class="mini-stat" data-testid="project-quick-stats-workflows">
            <span>Workflows</span>
            <strong>{{ workflows.length }}</strong>
          </div>
          <div class="mini-stat" data-testid="project-quick-stats-runs">
            <span>Runs</span>
            <strong>{{ runs.length }}</strong>
          </div>
        </div>
      </div>
    </section>
    <section class="content-grid">
      <div class="glass-card section-card" data-testid="project-recent-workflows">
        <h2>已绑定 Workflows</h2>
        <template v-if="workflows.length">
          <div
            v-for="wf in workflows.slice(0, 5)"
            :key="wf.id"
            class="list-card clickable"
            data-testid="project-recent-workflow-item"
            @click="$router.push(`/workflows/${wf.id}/editor`)"
          >
            {{ wf.name }} / {{ wf.nodes?.length || 0 }} nodes / {{ wf.edges?.length || 0 }} edges
          </div>
        </template>
        <div v-else class="empty-card" data-testid="project-detail-workflows-empty-state">暂无 Workflow</div>
      </div>
      <div class="glass-card section-card" data-testid="project-recent-runs">
        <h2>最近 Runs</h2>
        <template v-if="runs.length">
          <div v-for="run in runs.slice(0, 5)" :key="run.id" class="list-card clickable" data-testid="project-recent-run-item" @click="$router.push(`/runs/${run.id}`)">
            run_{{ run.id }} / workflow_{{ run.workflow_id }} / {{ run.status }}
          </div>
        </template>
        <div v-else class="empty-card" data-testid="project-detail-runs-empty-state">暂无 Runs</div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useProjectStore } from '@/stores/project'
import { useAgentStore } from '@/stores/agent'
import { useWorkflowStore } from '@/stores/workflow'
import { useRunStore } from '@/stores/run'
import type { Workflow } from '@/types/workflow'
import type { Run } from '@/types/execution'

const route = useRoute()
const projectStore = useProjectStore()
const agentStore = useAgentStore()
const workflowStore = useWorkflowStore()
const runStore = useRunStore()
const { currentProject } = storeToRefs(projectStore)
const { agents } = storeToRefs(agentStore)
const workflows = ref<Workflow[]>([])
const runs = ref<Run[]>([])

onMounted(async () => {
  const id = Number(route.params.id)
  await projectStore.fetchProject(id)
  await loadData()
})

async function loadData() {
  const id = Number(route.params.id)
  await agentStore.fetchAgents(id)
  await workflowStore.fetchWorkflows(id)
  workflows.value = workflowStore.workflows
  const runList: Run[] = []
  for (const wf of workflows.value.slice(0, 10)) {
    await runStore.fetchRuns(wf.id)
    runList.push(...runStore.runs)
  }
  runs.value = runList.sort((a, b) => (b.id || 0) - (a.id || 0))
}
</script>

<style scoped>
.project-detail-page {
  padding: 20px 24px;
}

.detail-grid,
.content-grid,
.dashboard-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.section-card {
  padding: 18px;
  border-radius: 22px;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.meta-grid span,
.mini-stat span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.meta-grid strong,
.mini-stat strong {
  display: block;
  margin-top: 8px;
}

.chip {
  display: inline-flex;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 12px;
}

.list-card {
  padding: 14px;
  margin-top: 10px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
}

.list-card.clickable {
  cursor: pointer;
  transition: border-color 0.2s;
}

.list-card.clickable:hover {
  border-color: rgba(86, 240, 192, 0.3);
}

.empty-card {
  color: var(--text-muted);
  text-align: center;
  padding: 40px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
  margin-top: 10px;
}

@media (max-width: 1200px) {
  .detail-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .project-detail-page {
    padding: 16px;
  }
}
</style>
