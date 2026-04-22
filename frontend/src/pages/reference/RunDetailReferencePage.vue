<template>
  <ReferenceShell eyebrow="Reference / Run" title="Run 详情页原型" subtitle="Timeline、结构化输出、handoff、指标同屏展示。" :metrics="referenceMetrics" :items="referenceNavItems">
    <section v-if="loadError" class="glass-card section-card" data-testid="run-code-runtime-load-error">
      <p class="error-text">Failed to load run detail. Please try again.</p>
    </section>
    <template v-else>
      <section class="detail-grid">
        <div class="glass-card section-card" data-testid="run-header-region">
          <span class="chip">success</span>
          <h2>run_128 / 内容生成流程</h2>
          <div class="meta-grid">
            <div><span>总耗时</span><strong>2.4s</strong></div>
            <div><span>Token</span><strong>1284</strong></div>
            <div><span>触发人</span><strong>chat</strong></div>
          </div>
        </div>
      </section>

      <section class="content-grid">
        <div class="glass-card section-card" data-testid="run-timeline-region">
          <h2>节点时间线</h2>
          <div class="list-card">start_1 / success / 35ms</div>
          <div class="list-card">agent_1 / success / 1.7s</div>
          <div class="list-card">output_1 / success / 14ms</div>
        </div>
        <div class="glass-card section-card" data-testid="run-structured-output-region">
          <h2>Structured Output</h2>
          <pre class="code-block">{ "status": "success", "score": 84, "outline": ["行业背景", "实施路径"] }</pre>
        </div>
        <div class="glass-card section-card" data-testid="run-handoff-region">
          <h2>Handoff & Metrics</h2>
          <p>已完成策略分析，下游节点按 outline 扩写，不要重新探索主题。</p>
          <div class="list-card">artifact://outline_v1.json</div>
          <div class="list-card">token_usage_input: 664 / output: 380</div>
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
  </ReferenceShell>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'

const route = useRoute()
const loadError = computed(() => route.query.load_error === '1')

const showCodeRuntime = computed(() => {
  return route.query.mode === 'code_runtime'
})

const codeIterations = [
  { iteration_no: 1, validation_summary: { lint: 'passed', build: 'skipped', unit_tests: 'failed' } },
]
</script>

<style scoped>
.detail-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.content-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr 0.9fr;
  gap: 16px;
}

.section-card {
  padding: 18px;
  border-radius: 22px;
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
</style>
