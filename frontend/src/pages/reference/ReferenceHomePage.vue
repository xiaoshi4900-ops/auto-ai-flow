<template>
  <ReferenceShell
    eyebrow="UI Reference Hub"
    title="AutoAiFlow 页面原型总览"
    subtitle="这组原型不是最终业务实现，而是页面级视觉与结构输入，供后续 AI 按 spec 与 Playwright 用例开发。"
    :metrics="referenceMetrics"
    :items="referenceNavItems"
  >
    <section class="overview-grid">
      <RouterLink
        v-for="page in pages"
        :key="page.to"
        :to="page.to"
        class="overview-card glass-card"
      >
        <span class="overview-card__tag">{{ page.tag }}</span>
        <strong>{{ page.title }}</strong>
        <p>{{ page.desc }}</p>
      </RouterLink>
    </section>
  </ReferenceShell>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import ReferenceShell from '@/components/reference/ReferenceShell.vue'
import { referenceMetrics, referenceNavItems } from './reference-config'
import { ROUTES } from '@/constants/routes'

const pages = [
  { to: ROUTES.UI_REFERENCE_LOGIN, title: '登录页', desc: '品牌 + 认证表单原型', tag: 'Auth' },
  { to: ROUTES.UI_REFERENCE_PROJECT_LIST, title: '项目列表', desc: '项目空间与创建入口', tag: 'Project' },
  { to: ROUTES.UI_REFERENCE_PROJECT_DETAIL, title: '项目详情', desc: '项目级聚合工作台', tag: 'Project' },
  { to: ROUTES.UI_REFERENCE_AGENT_LIST, title: 'Agent 列表', desc: '人物资产总览', tag: 'Agent' },
  { to: ROUTES.UI_REFERENCE_AGENT_EDIT, title: 'Agent 编辑', desc: '人物画像与能力绑定', tag: 'Agent' },
  { to: ROUTES.UI_REFERENCE_MODEL_CONFIG, title: '模型配置', desc: '项目模型与密钥状态', tag: 'Model' },
  { to: ROUTES.UI_REFERENCE_WORKFLOW_LIST, title: 'Workflow 列表', desc: '编排资产入口', tag: 'Workflow' },
  { to: ROUTES.UI_REFERENCE_WORKFLOW_EDITOR, title: 'Workflow 编排', desc: '画布、Inspector、运行观测', tag: 'Workflow' },
  { to: ROUTES.UI_REFERENCE_RUN_LIST, title: 'Run 列表', desc: '执行记录与状态筛选', tag: 'Run' },
  { to: ROUTES.UI_REFERENCE_RUN_DETAIL, title: 'Run 详情', desc: 'Timeline、输出、handoff、metrics', tag: 'Run' },
]
</script>

<style scoped>
.overview-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.overview-card {
  display: block;
  padding: 18px;
  border-radius: 22px;
  text-decoration: none;
}

.overview-card__tag {
  display: inline-flex;
  height: 28px;
  align-items: center;
  padding: 0 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: var(--accent-primary);
  font-size: 12px;
}

.overview-card strong {
  display: block;
  margin-top: 14px;
  font-size: 18px;
}

.overview-card p {
  margin: 8px 0 0;
  color: var(--text-secondary);
}

@media (max-width: 1200px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
}
</style>
