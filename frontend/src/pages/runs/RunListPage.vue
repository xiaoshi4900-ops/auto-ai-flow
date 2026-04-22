<template>
  <div class="runs-page" data-testid="runs-workspace-page">
    <section class="glass-card section-card" data-testid="run-list-page">
      <header class="section-header">
        <h2>执行记录</h2>
        <div class="filters">
          <button class="chip" data-testid="runs-filter-all" :class="{ active: currentFilter === 'all' }" @click="setFilter('all')">all</button>
          <button class="chip" data-testid="runs-filter-success" :class="{ active: currentFilter === 'success' }" @click="setFilter('success')">success</button>
          <button class="chip" data-testid="runs-filter-failed" :class="{ active: currentFilter === 'failed' }" @click="setFilter('failed')">failed</button>
        </div>
      </header>
      <div class="table-list" data-testid="run-list-region">
        <div v-for="run in filteredRuns" :key="run.id" class="table-row" :data-testid="`run-row-${run.id}`">
          <strong data-testid="run-col-id">{{ run.id }}</strong>
          <span data-testid="run-col-workflow">{{ run.workflow_id }}</span>
          <span :class="run.status === 'failed' ? 'bad' : 'ok'" data-testid="run-col-status">{{ run.status }}</span>
          <span data-testid="run-col-latency">{{ formatLatency(run.latency_ms) }}</span>
          <span data-testid="run-col-tokens">{{ run.token_usage_total ?? '-' }}</span>
          <div class="actions">
            <button class="btn-secondary" data-testid="run-row-detail" @click="goToDetail(run.id)">Detail</button>
          </div>
        </div>
        <div v-if="!filteredRuns.length" class="empty-card" data-testid="run-empty-state">暂无执行记录。</div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRunStore } from '@/stores/run'
import { storeToRefs } from 'pinia'

const router = useRouter()
const runStore = useRunStore()
const { runs } = storeToRefs(runStore)
const currentFilter = ref('all')

const filteredRuns = computed(() => {
  if (currentFilter.value === 'all') return runs.value
  return runs.value.filter((r) => r.status === currentFilter.value)
})

onMounted(async () => {
  await runStore.fetchRuns()
})

function setFilter(status: string) {
  currentFilter.value = status
  router.replace({ path: '/runs', query: status === 'all' ? {} : { status } })
}

function goToDetail(id: number) {
  router.push(`/runs/${id}`)
}

function formatLatency(ms?: number): string {
  if (ms == null) return '-'
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`
  return `${ms}ms`
}
</script>

<style scoped>
.runs-page {
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

.filters {
  display: flex;
  gap: 8px;
}

.chip {
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 13px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.chip.active {
  background: var(--accent-primary);
  color: var(--bg-dark);
}

.chip:hover {
  opacity: 0.85;
}

.table-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1.1fr 0.7fr 0.7fr 0.7fr 0.8fr;
  gap: 12px;
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
  align-items: center;
}

.ok { color: var(--accent-primary); }
.bad { color: var(--accent-danger); }

.actions {
  display: flex;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 6px 12px;
  border-radius: 10px;
  border: 1px solid var(--border-soft);
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(86, 240, 192, 0.3);
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
  .runs-page {
    padding: 16px;
  }
  .table-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>
