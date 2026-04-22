<template>
  <div class="run-detail-page" data-testid="run-detail-page">
    <section v-if="loadError" class="glass-card section-card" data-testid="run-code-runtime-load-error">
      <p class="error-text">Failed to load run detail. Please try again.</p>
    </section>
    <template v-else>
      <section class="detail-grid">
        <div class="glass-card section-card" data-testid="run-header-region">
          <div class="header-top">
            <button class="btn-back" data-testid="run-detail-action-back" @click="$router.push('/runs')">← 返回</button>
            <span class="chip" :class="currentRun?.run?.status === 'failed' ? 'bad' : ''" data-testid="run-status-chip">{{ currentRun?.run?.status || 'loading' }}</span>
          </div>
          <h2 data-testid="run-header-title">Run #{{ currentRun?.run?.id || '-' }}</h2>
          <div class="meta-grid">
            <div data-testid="run-meta-latency"><span>总耗时</span><strong>{{ formatLatency(currentRun?.run?.latency_ms) }}</strong></div>
            <div data-testid="run-meta-tokens"><span>Token</span><strong>{{ currentRun?.run?.token_usage_total ?? '-' }}</strong></div>
            <div data-testid="run-meta-trigger"><span>触发人</span><strong>chat</strong></div>
          </div>
        </div>
      </section>

      <section class="content-grid">
        <div class="glass-card section-card" data-testid="run-timeline-region">
          <h2>节点时间线</h2>
          <template v-if="currentRun?.node_runs?.length">
            <div v-for="nr in currentRun.node_runs" :key="nr.id" class="list-card" :data-testid="`run-timeline-${nr.node_key}`">
              {{ nr.node_key }} / {{ nr.status }} / {{ formatDuration(nr.duration_ms) }}
            </div>
          </template>
          <div v-else class="list-card">暂无节点执行记录</div>
        </div>
        <div class="glass-card section-card" data-testid="run-structured-output-region">
          <h2>Structured Output</h2>
          <pre class="code-block" data-testid="run-structured-output">{{ formatOutput(currentRun?.run?.output_payload) }}</pre>
        </div>
        <div class="glass-card section-card" data-testid="run-handoff-region">
          <h2>Handoff & Metrics</h2>
          <p>{{ currentRun?.run?.error_message || '无额外信息' }}</p>
        </div>
      </section>

      <section v-if="showCodeRuntime" class="content-grid">
        <div class="glass-card section-card" data-testid="run-code-iterations-region">
          <h2>Code Iterations</h2>
          <div v-for="iter in codeIterations" :key="iter.iteration_no" class="list-card" data-testid="run-code-iteration-item">
            <strong>Iteration {{ iter.iteration_no }}</strong>
            <div class="validation-row">
              <span v-for="(val, key) in iter.validation_summary" :key="key" class="validation-badge" :class="val === 'passed' ? 'ok' : val === 'failed' ? 'bad' : 'warn'">
                {{ key }}: {{ val }}
              </span>
            </div>
          </div>
        </div>
        <div class="glass-card section-card" data-testid="run-code-handoff-region">
          <h2>Code Runtime Handoff</h2>
          <div class="list-card" data-testid="run-code-handoff-changed-files">Changed Files: src/service.py, tests/test_service.py</div>
          <div class="list-card" data-testid="run-code-handoff-open-issues">Open Issues: 2 lint warnings</div>
          <div class="list-card" data-testid="run-code-handoff-next-actions">Next Actions: Fix lint warnings, add integration tests</div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRunStore } from '@/stores/run'
import { storeToRefs } from 'pinia'

const route = useRoute()
const runStore = useRunStore()
const { currentRun } = storeToRefs(runStore)

const loadError = computed(() => route.query.load_error === '1')

const showCodeRuntime = computed(() => {
  return route.query.mode === 'code_runtime'
})

const codeIterations = [
  { iteration_no: 1, validation_summary: { lint: 'passed', build: 'skipped', unit_tests: 'failed' } },
]

onMounted(async () => {
  const id = Number(route.params.id)
  await runStore.fetchRunDetail(id)
})

function formatLatency(ms?: number): string {
  if (ms == null) return '-'
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`
  return `${ms}ms`
}

function formatDuration(ms: number | null): string {
  if (ms == null) return '-'
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`
  return `${ms}ms`
}

function formatOutput(payload: Record<string, unknown> | null | undefined): string {
  if (!payload) return '{ }'
  return JSON.stringify(payload, null, 2)
}
</script>

<style scoped>
.run-detail-page {
  padding: 20px 24px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.content-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr 0.9fr;
  gap: 16px;
  margin-top: 16px;
}

.section-card {
  padding: 18px;
  border-radius: 22px;
}

.header-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.btn-back {
  padding: 6px 12px;
  border-radius: 10px;
  border: 1px solid var(--border-soft);
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(86, 240, 192, 0.3);
}

.chip {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
  font-size: 13px;
}

.chip.bad {
  background: rgba(255, 111, 127, 0.12);
  color: var(--accent-danger);
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.meta-grid span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.list-card {
  padding: 14px;
  margin-top: 10px;
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
}

.code-block {
  margin: 0;
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
  white-space: pre-wrap;
  color: #b8d9ec;
  font-family: Consolas, "Courier New", monospace;
}

.validation-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.validation-badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.validation-badge.ok {
  background: rgba(86, 240, 192, 0.12);
  color: var(--accent-primary);
}

.validation-badge.bad {
  background: rgba(255, 111, 127, 0.12);
  color: var(--accent-danger);
}

.validation-badge.warn {
  background: rgba(247, 185, 85, 0.12);
  color: #f7b955;
}

.error-text {
  color: var(--accent-danger);
}

@media (max-width: 1280px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 960px) {
  .run-detail-page {
    padding: 16px;
  }
}
</style>
