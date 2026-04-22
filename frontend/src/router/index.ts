import { createRouter, createWebHistory } from 'vue-router'
import { ROUTES } from '@/constants/routes'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: ROUTES.PROJECTS,
    },
    {
      path: ROUTES.LOGIN,
      name: 'Login',
      component: () => import('@/pages/auth/LoginPage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_HOME,
      name: 'ReferenceHome',
      component: () => import('@/pages/reference/ReferenceHomePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_LOGIN,
      name: 'ReferenceLogin',
      component: () => import('@/pages/reference/LoginReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_PROJECT_LIST,
      name: 'ReferenceProjectList',
      component: () => import('@/pages/reference/ProjectListReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_PROJECT_DETAIL,
      name: 'ReferenceProjectDetail',
      component: () => import('@/pages/reference/ProjectDetailReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_AGENT_LIST,
      name: 'ReferenceAgentList',
      component: () => import('@/pages/reference/AgentListReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_AGENT_EDIT,
      name: 'ReferenceAgentEdit',
      component: () => import('@/pages/reference/AgentEditReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_MODEL_CONFIG,
      name: 'ReferenceModelConfig',
      component: () => import('@/pages/reference/ModelConfigReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_WORKFLOW_LIST,
      name: 'ReferenceWorkflowList',
      component: () => import('@/pages/reference/WorkflowListReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_WORKFLOW_EDITOR,
      name: 'ReferenceWorkflowEditor',
      component: () => import('@/pages/reference/WorkflowStudioReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/ui-reference/workflows/editor',
      name: 'ReferenceWorkflowEditorAlt',
      component: () => import('@/pages/reference/WorkflowStudioReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_RUN_LIST,
      name: 'ReferenceRunList',
      component: () => import('@/pages/reference/RunListReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: ROUTES.UI_REFERENCE_RUN_DETAIL,
      name: 'ReferenceRunDetail',
      component: () => import('@/pages/reference/RunDetailReferencePage.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/layouts/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'projects',
          name: 'ProjectList',
          component: () => import('@/pages/projects/ProjectListPage.vue'),
        },
        {
          path: 'projects/:id',
          name: 'ProjectDetail',
          component: () => import('@/pages/projects/ProjectDetailPage.vue'),
        },
        {
          path: 'agents',
          name: 'AgentList',
          component: () => import('@/pages/agents/AgentListPage.vue'),
        },
        {
          path: 'agents/:id',
          name: 'AgentEdit',
          component: () => import('@/pages/agents/AgentEditPage.vue'),
        },
        {
          path: 'models',
          name: 'ModelConfig',
          component: () => import('@/pages/models/ModelConfigPage.vue'),
        },
        {
          path: 'workflows',
          name: 'WorkflowList',
          component: () => import('@/pages/workflows/WorkflowListPage.vue'),
        },
        {
          path: 'workflows/:id/editor',
          name: 'WorkflowEditor',
          component: () => import('@/pages/workflows/WorkflowEditorPage.vue'),
        },
        {
          path: 'runs',
          name: 'RunList',
          component: () => import('@/pages/runs/RunListPage.vue'),
        },
        {
          path: 'runs/:id',
          name: 'RunDetail',
          component: () => import('@/pages/runs/RunDetailPage.vue'),
        },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth !== false && !token) {
    return { path: ROUTES.LOGIN }
  }
})

export default router
