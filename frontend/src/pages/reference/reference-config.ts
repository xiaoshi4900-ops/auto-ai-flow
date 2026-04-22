import { ROUTES } from '@/constants/routes'

export const referenceNavItems = [
  { to: ROUTES.UI_REFERENCE_HOME, label: '原型总览', color: '#56f0c0' },
  { to: ROUTES.UI_REFERENCE_LOGIN, label: '登录页', color: '#3cb9ff' },
  { to: ROUTES.UI_REFERENCE_PROJECT_LIST, label: '项目列表', color: '#56f0c0' },
  { to: ROUTES.UI_REFERENCE_PROJECT_DETAIL, label: '项目详情', color: '#f7b955' },
  { to: ROUTES.UI_REFERENCE_AGENT_LIST, label: 'Agent 列表', color: '#56f0c0' },
  { to: ROUTES.UI_REFERENCE_AGENT_EDIT, label: 'Agent 编辑', color: '#3cb9ff' },
  { to: ROUTES.UI_REFERENCE_MODEL_CONFIG, label: '模型配置', color: '#ff6f7f' },
  { to: ROUTES.UI_REFERENCE_WORKFLOW_LIST, label: 'Workflow 列表', color: '#3cb9ff' },
  { to: ROUTES.UI_REFERENCE_WORKFLOW_EDITOR, label: 'Workflow 编排', color: '#56f0c0' },
  { to: ROUTES.UI_REFERENCE_RUN_LIST, label: 'Run 列表', color: '#f7b955' },
  { to: ROUTES.UI_REFERENCE_RUN_DETAIL, label: 'Run 详情', color: '#ff6f7f' },
] as const

export const referenceMetrics = [
  { label: '页面原型', value: '10' },
  { label: 'Playwright', value: '11' },
  { label: 'Page Spec', value: '10' },
]
