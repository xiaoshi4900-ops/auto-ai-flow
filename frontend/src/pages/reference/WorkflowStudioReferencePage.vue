<template>
  <div class="reference-page" data-testid="workflow-editor-page">
    <section class="hero glass-card">
      <div>
        <p class="eyebrow">UI Reference / Volt-style Observability Adaptation</p>
        <h1>AutoAiFlow Workflow Studio</h1>
        <p class="hero-copy">
          这不是最终实现页，而是给后续 AI 和工程师对齐视觉层级、模块分区、运行时信息密度的参考原型。
        </p>
      </div>
      <div class="hero-metrics">
        <div v-for="metric in heroMetrics" :key="metric.label" class="metric-pill">
          <span>{{ metric.label }}</span>
          <strong>{{ metric.value }}</strong>
        </div>
      </div>
    </section>

    <section class="studio-shell glass-card">
      <aside class="studio-sidebar">
        <div class="sidebar-title">Workflow Studio</div>
        <div class="sidebar-section">
          <p class="sidebar-heading">项目导航</p>
          <button v-for="entry in navEntries" :key="entry.label" class="sidebar-item" :class="{ active: entry.active }">
            <span class="dot" :style="{ background: entry.color }"></span>
            <span>{{ entry.label }}</span>
          </button>
        </div>
        <div class="sidebar-section">
          <p class="sidebar-heading">节点库</p>
          <div v-for="node in libraryNodes" :key="node.type" class="library-card">
            <div class="library-badge node-lib-type" :style="{ background: node.color }">{{ node.label }}</div>
            <div>
              <strong>{{ node.label }}</strong>
              <p>{{ node.desc }}</p>
            </div>
          </div>
        </div>
      </aside>

      <main class="studio-main">
        <header class="toolbar">
          <div>
            <div class="toolbar-breadcrumb">项目空间 / 内容生成平台 / Workflow</div>
            <h2>内容工作流编排</h2>
          </div>
          <div class="toolbar-actions">
            <button class="ghost-btn" data-testid="workflow-save-button" @click="saveWorkflow">保存草稿</button>
            <button class="ghost-btn">验证结构</button>
            <button class="primary-btn">运行 Workflow</button>
            <span v-if="saveError" class="error-badge" data-testid="workflow-save-error">Save failed</span>
          </div>
        </header>

        <div class="canvas-layout">
          <section class="canvas-panel grid-surface" data-testid="workflow-canvas-region">
            <div class="canvas-node start" style="top: 64px; left: 48px;">
              <span class="node-kicker">start</span>
              <strong>开始</strong>
              <p>初始化上下文</p>
            </div>

            <div class="canvas-node input" style="top: 188px; left: 112px;">
              <span class="node-kicker">input</span>
              <strong>接收输入</strong>
              <p>topic / audience / channel</p>
            </div>

            <div class="canvas-node agent" data-testid="node-agent-1" style="top: 88px; left: 356px;" @click="selectAgentNode">
              <span class="node-kicker">agent</span>
              <strong>策略 Agent</strong>
              <p>生成内容大纲与风险点</p>
            </div>

            <div class="canvas-node condition" style="top: 256px; left: 420px;">
              <span class="node-kicker">condition</span>
              <strong>质量门禁</strong>
              <p>score &gt; 75?</p>
            </div>

            <div class="canvas-node agent secondary" style="top: 112px; left: 720px;">
              <span class="node-kicker">agent</span>
              <strong>成稿 Agent</strong>
              <p>输出最终文章草稿</p>
            </div>

            <div class="canvas-node output" style="top: 300px; left: 808px;">
              <span class="node-kicker">output</span>
              <strong>统一输出</strong>
              <p>结构化结果 + artifact refs</p>
            </div>

            <div class="connector connector-1"></div>
            <div class="connector connector-2"></div>
            <div class="connector connector-3"></div>
            <div class="connector connector-4"></div>
            <div class="connector connector-5"></div>
          </section>

          <aside class="inspector-panel" data-testid="workflow-inspector-region">
            <div v-if="!agentSelected" class="panel-header">
              <span class="panel-label">Node Inspector</span>
              <strong>选择节点查看配置</strong>
            </div>
            <div v-else data-testid="workflow-agent-node-form">
              <div class="panel-header">
                <span class="panel-label">Node Inspector</span>
                <strong>Agent 节点配置</strong>
              </div>

              <div class="field-block">
                <label>Agent</label>
                <div class="field-value">内容策略分析师 / content_strategist</div>
              </div>

              <div class="field-block">
                <label>Execution Mode</label>
                <select v-model="executionMode" data-testid="execution-mode-select" class="mode-select">
                  <option value="normal_llm">normal_llm</option>
                  <option value="code_runtime">code_runtime</option>
                </select>
              </div>

              <template v-if="executionMode === 'code_runtime'">
                <div class="field-block">
                  <label>Max Iterations</label>
                  <input v-model.number="maxIterations" data-testid="code-policy-max-iterations" type="number" class="policy-input" />
                </div>
                <div class="field-block">
                  <label>Run Lint</label>
                  <div class="toggle" :class="{ on: runLint }" data-testid="code-policy-run-lint" @click="runLint = !runLint">{{ runLint ? 'ON' : 'OFF' }}</div>
                </div>
              </template>

              <div class="field-block">
                <label>Task Instruction</label>
                <div class="field-area">
                  基于输入主题、目标用户与渠道约束，先输出内容框架、关键论点、风险提示和建议结构化字段。
                </div>
              </div>

              <div class="field-grid">
                <div class="field-block">
                  <label>允许 Tool</label>
                  <div class="toggle on">ON</div>
                </div>
                <div class="field-block">
                  <label>重试次数</label>
                  <div class="field-value">1</div>
                </div>
              </div>

              <div class="field-block">
                <label>Input Mapping</label>
                <pre class="code-block">{{ inputMapping }}</pre>
              </div>

              <div class="field-block">
                <label>Output Schema Preview</label>
                <pre class="code-block">{{ outputSchema }}</pre>
              </div>
            </div>
          </aside>
        </div>

        <section class="runtime-panel" data-testid="workflow-runtime-region">
          <div class="runtime-header">
            <div>
              <span class="panel-label">Latest Run</span>
              <h3>运行可观测面板</h3>
            </div>
            <div class="status-row">
              <span class="status success">SUCCESS</span>
              <span class="status info">2.4s</span>
              <span class="status neutral">1,284 tokens</span>
            </div>
          </div>

          <div class="runtime-grid">
            <div class="runtime-card">
              <strong>节点时间线</strong>
              <ul class="timeline">
                <li v-for="item in timeline" :key="item.title">
                  <span class="timeline-dot" :style="{ background: item.color }"></span>
                  <div>
                    <div class="timeline-title">{{ item.title }}</div>
                    <div class="timeline-meta">{{ item.meta }}</div>
                  </div>
                </li>
              </ul>
            </div>

            <div class="runtime-card">
              <strong>Structured Output</strong>
              <pre class="code-block tall">{{ structuredOutput }}</pre>
            </div>

            <div class="runtime-card">
              <strong>Handoff Summary</strong>
              <p class="runtime-copy">
                已完成内容策略分析，输出主论点、风险点和推荐结构。下游成稿节点需要基于 outline 直接扩写，不要重复探索。
              </p>
              <div class="artifact-list">
                <span class="artifact-chip">outline_v1.json</span>
                <span class="artifact-chip">risk_notes.md</span>
                <span class="artifact-chip">draft_context.json</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const agentSelected = ref(true)
const executionMode = ref('normal_llm')
const maxIterations = ref(3)
const runLint = ref(true)
const saveError = ref(false)

const initialMode = computed(() => {
  const m = route.query.execution_mode as string
  return m || 'normal_llm'
})
if (initialMode.value) {
  executionMode.value = initialMode.value
}

const shouldShowSaveError = computed(() => route.query.save_error === '1')

function selectAgentNode() {
  agentSelected.value = true
}

function saveWorkflow() {
  if (shouldShowSaveError.value) {
    saveError.value = true
  } else {
    saveError.value = false
  }
}

const heroMetrics = [
  { label: '运行成功率', value: '98.2%' },
  { label: '平均耗时', value: '2.4s' },
  { label: '近期 Runs', value: '128' },
]

const navEntries = [
  { label: '项目总览', active: false, color: '#56f0c0' },
  { label: 'Agent 管理', active: false, color: '#3cb9ff' },
  { label: 'Workflow 编排', active: true, color: '#56f0c0' },
  { label: '运行记录', active: false, color: '#f7b955' },
  { label: '模型配置', active: false, color: '#ff6f7f' },
]

const libraryNodes = [
  { type: 'start', short: 'S', label: 'Start', desc: '初始化执行上下文', color: 'linear-gradient(135deg, #56f0c0, #179b9a)' },
  { type: 'input', short: 'I', label: 'Input', desc: '挂载用户输入与映射', color: 'linear-gradient(135deg, #3cb9ff, #1d5eff)' },
  { type: 'agent', short: 'A', label: 'Agent', desc: '调度人物执行具体任务', color: 'linear-gradient(135deg, #8af5d9, #31c09d)' },
  { type: 'condition', short: 'C', label: 'Condition', desc: '判断分支与路线', color: 'linear-gradient(135deg, #f7b955, #ff8b3d)' },
  { type: 'output', short: 'O', label: 'Output', desc: '聚合最终输出', color: 'linear-gradient(135deg, #ff9cb5, #ff6f7f)' },
]

const timeline = [
  { title: 'start_1 / 开始', meta: '35ms · 初始化运行上下文', color: '#56f0c0' },
  { title: 'input_1 / 接收输入', meta: '20ms · 写入 input payload', color: '#3cb9ff' },
  { title: 'agent_1 / 策略 Agent', meta: '1.7s · 664 input / 380 output tokens', color: '#56f0c0' },
  { title: 'condition_1 / 质量门禁', meta: '8ms · score = 84', color: '#f7b955' },
  { title: 'output_1 / 统一输出', meta: '14ms · 生成结果与 artifacts', color: '#ff6f7f' },
]

const inputMapping = `{
  "topic": "$.input.topic",
  "channel": "$.input.channel",
  "audience": "$.input.audience"
}`

const outputSchema = `{
  "outline": "string[]",
  "risk_points": "string[]",
  "score": "number",
  "handoff_summary": "string"
}`

const structuredOutput = `{
  "status": "success",
  "structured_output": {
    "outline": [
      "行业背景与价值主张",
      "实施路径与成本边界",
      "执行节奏与验证方案"
    ],
    "risk_points": [
      "输出结构过长",
      "角色定义过散"
    ],
    "score": 84
  },
  "artifact_refs": [
    "artifact://outline_v1.json"
  ]
}`
</script>

<style scoped>
.reference-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 28px;
}

.hero {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 30px;
  border-radius: var(--radius-lg);
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--accent-primary);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.hero h1 {
  margin: 0;
  font: 600 34px/1.1 var(--font-display);
}

.hero-copy {
  max-width: 720px;
  margin: 14px 0 0;
  color: var(--text-secondary);
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(116px, 1fr));
  gap: 12px;
  min-width: 380px;
}

.metric-pill {
  padding: 16px;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-soft);
}

.metric-pill span {
  display: block;
  font-size: 12px;
  color: var(--text-muted);
}

.metric-pill strong {
  display: block;
  margin-top: 8px;
  font-size: 24px;
}

.studio-shell {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  min-height: 980px;
  border-radius: 28px;
  overflow: hidden;
}

.studio-sidebar {
  padding: 22px;
  border-right: 1px solid var(--border-soft);
  background: rgba(8, 14, 24, 0.94);
}

.sidebar-title {
  padding: 14px 16px;
  margin-bottom: 18px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(86, 240, 192, 0.14), rgba(60, 185, 255, 0.12));
  border: 1px solid var(--border-strong);
  font-weight: 700;
}

.sidebar-section + .sidebar-section {
  margin-top: 24px;
}

.sidebar-heading {
  margin: 0 0 10px;
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.sidebar-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  margin-bottom: 8px;
  border: 1px solid transparent;
  border-radius: 14px;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.sidebar-item.active {
  background: rgba(86, 240, 192, 0.08);
  border-color: var(--border-strong);
  color: var(--text-primary);
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.library-card {
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr);
  gap: 12px;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-soft);
}

.library-card strong {
  display: block;
  font-size: 14px;
}

.library-card p {
  margin: 4px 0 0;
  color: var(--text-muted);
  font-size: 12px;
}

.library-badge {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  color: #041016;
  font-weight: 800;
}

.studio-main {
  padding: 22px;
  background: linear-gradient(180deg, rgba(10, 16, 27, 0.88), rgba(9, 15, 24, 0.94));
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 18px;
}

.toolbar-breadcrumb {
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 12px;
}

.toolbar h2,
.runtime-header h3 {
  margin: 0;
  font-size: 28px;
}

.toolbar-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.error-badge {
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(255, 111, 127, 0.12);
  color: var(--accent-danger);
  font-size: 13px;
}

.mode-select,
.policy-input {
  width: 100%;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.mode-select option {
  background: #0a1019;
  color: var(--text-primary);
}

.ghost-btn,
.primary-btn {
  height: 40px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  cursor: pointer;
}

.primary-btn {
  background: linear-gradient(135deg, rgba(86, 240, 192, 0.9), rgba(60, 185, 255, 0.9));
  color: #061119;
  border-color: transparent;
  font-weight: 700;
}

.canvas-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 18px;
}

.canvas-panel,
.inspector-panel,
.runtime-panel {
  border-radius: 24px;
  border: 1px solid var(--border-soft);
  background: rgba(11, 20, 32, 0.82);
  box-shadow: var(--shadow-glow);
}

.canvas-panel {
  position: relative;
  min-height: 540px;
  overflow: hidden;
}

.canvas-node {
  position: absolute;
  width: 192px;
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(13, 24, 38, 0.96);
  box-shadow: 0 16px 28px rgba(0, 0, 0, 0.25);
}

.canvas-node strong {
  display: block;
  margin: 8px 0 4px;
}

.canvas-node p {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary);
}

.node-kicker {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.canvas-node.start { border-color: rgba(86, 240, 192, 0.34); }
.canvas-node.input { border-color: rgba(60, 185, 255, 0.34); }
.canvas-node.agent { border-color: rgba(112, 239, 205, 0.32); }
.canvas-node.condition { border-color: rgba(247, 185, 85, 0.36); }
.canvas-node.output { border-color: rgba(255, 111, 127, 0.34); }
.canvas-node.secondary { box-shadow: 0 18px 36px rgba(16, 82, 62, 0.18); }

.connector {
  position: absolute;
  border-top: 2px solid rgba(117, 224, 244, 0.45);
}

.connector::after {
  content: "";
  position: absolute;
  right: -6px;
  top: -4px;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--accent-primary);
  box-shadow: 0 0 16px rgba(86, 240, 192, 0.8);
}

.connector-1 { top: 108px; left: 240px; width: 128px; }
.connector-2 { top: 232px; left: 304px; width: 180px; }
.connector-3 { top: 178px; left: 548px; width: 188px; transform: rotate(-25deg); transform-origin: left center; }
.connector-4 { top: 286px; left: 612px; width: 214px; }
.connector-5 { top: 334px; left: 1000px; width: 56px; transform: rotate(-14deg); transform-origin: left center; }

.inspector-panel {
  padding: 18px;
}

.panel-header {
  margin-bottom: 18px;
}

.panel-label {
  display: inline-block;
  margin-bottom: 6px;
  color: var(--accent-secondary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.field-block + .field-block {
  margin-top: 14px;
}

.field-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.field-block label {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 12px;
}

.field-value,
.field-area,
.code-block,
.toggle {
  border-radius: 16px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
}

.field-value,
.toggle {
  padding: 12px 14px;
}

.field-area {
  padding: 14px;
  color: var(--text-secondary);
}

.toggle.on {
  color: var(--accent-primary);
  font-weight: 700;
}

.code-block {
  margin: 0;
  padding: 14px;
  color: #b8d9ec;
  white-space: pre-wrap;
  font-size: 12px;
  line-height: 1.6;
  font-family: Consolas, "Courier New", monospace;
}

.code-block.tall {
  min-height: 218px;
}

.runtime-panel {
  margin-top: 18px;
  padding: 18px;
}

.runtime-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.status-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.status {
  display: inline-flex;
  align-items: center;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid transparent;
}

.status.success {
  color: #70f7d5;
  background: rgba(86, 240, 192, 0.1);
  border-color: rgba(86, 240, 192, 0.24);
}

.status.info {
  color: #8ed7ff;
  background: rgba(60, 185, 255, 0.1);
  border-color: rgba(60, 185, 255, 0.24);
}

.status.neutral {
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--border-soft);
}

.runtime-grid {
  display: grid;
  grid-template-columns: 1.1fr 1.2fr 0.9fr;
  gap: 16px;
}

.runtime-card {
  min-height: 260px;
  padding: 16px;
  border-radius: 20px;
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.04);
}

.runtime-card strong {
  display: block;
  margin-bottom: 12px;
}

.timeline {
  margin: 0;
  padding: 0;
  list-style: none;
}

.timeline li {
  display: grid;
  grid-template-columns: 12px minmax(0, 1fr);
  gap: 12px;
  margin-bottom: 14px;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  margin-top: 4px;
  border-radius: 999px;
}

.timeline-title {
  font-size: 14px;
}

.timeline-meta {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: 12px;
}

.runtime-copy {
  margin: 0;
  color: var(--text-secondary);
}

.artifact-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.artifact-chip {
  display: inline-flex;
  align-items: center;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(86, 240, 192, 0.08);
  color: var(--accent-primary);
  border: 1px solid rgba(86, 240, 192, 0.18);
  font-size: 12px;
}

@media (max-width: 1440px) {
  .canvas-layout,
  .runtime-grid,
  .hero,
  .studio-shell {
    grid-template-columns: 1fr;
  }

  .studio-shell {
    display: block;
  }

  .studio-sidebar {
    border-right: 0;
    border-bottom: 1px solid var(--border-soft);
  }

  .hero-metrics {
    min-width: 0;
  }
}
</style>
