import { type Page } from '@playwright/test'

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

async function setupAuth(page: Page) {
  await page.addInitScript(() => {
    localStorage.setItem('access_token', 'token-5d-matrix')
    localStorage.setItem('refresh_token', 'refresh-5d-matrix')
  })

  await page.route('**/api/v1/auth/me', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      headers: CORS_HEADERS,
      body: JSON.stringify({
        code: 0,
        message: 'ok',
        data: {
          id: 1,
          username: 'operator',
          email: 'operator@test.com',
          display_name: 'Operator',
          is_active: true,
        },
      }),
    })
  })
}

async function setupWorkspaceApis(
  page: Page,
  input?: {
    projects?: Array<Record<string, unknown>>
    projectDetail?: Record<string, unknown>
    agents?: Array<Record<string, unknown>>
    workflows?: Array<Record<string, unknown>>
    runs?: Array<Record<string, unknown>>
    providers?: Array<Record<string, unknown>>
    models?: Array<Record<string, unknown>>
    modelConfigs?: Array<Record<string, unknown>>
  },
) {
  const projects = input?.projects ?? []
  const projectDetail = input?.projectDetail ?? projects[0] ?? { id: 1, owner_id: 1, name: 'P-EMPTY', description: '' }
  const agents = input?.agents ?? []
  const workflows = input?.workflows ?? []
  const runs = input?.runs ?? []
  const providers = input?.providers ?? []
  const models = input?.models ?? []
  const modelConfigs = input?.modelConfigs ?? []

  await page.route('**/api/v1/**', async (route) => {
    const method = route.request().method()
    const url = route.request().url()

    if (method === 'OPTIONS') {
      await route.fulfill({ status: 204, headers: { ...CORS_HEADERS, 'Access-Control-Max-Age': '86400' }, body: '' })
      return
    }

    if (url.includes('/api/v1/auth/me')) {
      await route.fallback()
      return
    }

    if (url.match(/\/api\/v1\/projects\/\d+$/)) {
      if (method !== 'GET') {
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: null }) })
        return
      }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: projectDetail }),
      })
      return
    }

    if (url.includes('/api/v1/projects')) {
      if (method === 'POST') {
        const payload = route.request().postDataJSON() as { name: string; description?: string }
        const created = { id: 999, owner_id: 1, name: payload.name, description: payload.description ?? null }
        projects.push(created)
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: created }) })
        return
      }
      if (method === 'DELETE') {
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: null }) })
        return
      }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { items: projects, page: 1, page_size: 20, total: projects.length } }),
      })
      return
    }

    if (url.match(/\/api\/v1\/agents\/\d+$/)) {
      if (method !== 'GET') {
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: null }) })
        return
      }
      const id = Number(url.split('/').pop() || '0')
      const found = agents.find((x) => Number(x.id) === id) ?? null
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: found }) })
      return
    }

    if (url.includes('/api/v1/agents')) {
      if (method === 'POST') {
        const payload = route.request().postDataJSON() as Record<string, unknown>
        const created = { id: 888, project_id: payload.project_id, name: payload.name, role_name: payload.role_name, skill_ids: payload.skill_ids ?? [], tool_ids: payload.tool_ids ?? [] }
        agents.push(created)
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: created }) })
        return
      }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { items: agents, page: 1, page_size: 20, total: agents.length } }),
      })
      return
    }

    if (url.match(/\/api\/v1\/workflows\/\d+$/)) {
      if (method === 'GET') {
        const id = Number(url.split('/').pop() || '0')
        const found = workflows.find((x) => Number(x.id) === id) ?? { id: 0, project_id: 1, name: 'WF-EMPTY', description: '', nodes: [], edges: [] }
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: found }) })
        return
      }
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: { id: 777 } }) })
      return
    }

    if (url.includes('/api/v1/workflows')) {
      if (method === 'POST') {
        const payload = route.request().postDataJSON() as Record<string, unknown>
        const created = { id: 777, project_id: payload.project_id, name: payload.name, description: payload.description ?? '', nodes: [] }
        workflows.push(created)
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: created }) })
        return
      }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { items: workflows, page: 1, page_size: 20, total: workflows.length } }),
      })
      return
    }

    if (url.includes('/code-iterations')) {
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: { items: [] } }) })
      return
    }

    if (url.match(/\/api\/v1\/runs\/\d+$/)) {
      if (method !== 'GET') {
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: null }) })
        return
      }
      const run = runs[0] ?? { id: 0, workflow_id: 0, status: 'queued', started_at: null, finished_at: null }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { run, node_runs: [] } }),
      })
      return
    }

    if (url.includes('/api/v1/runs')) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { items: runs, page: 1, page_size: 20, total: runs.length } }),
      })
      return
    }

    if (url.includes('/api/v1/executions/trigger')) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { run_id: 9001, status: 'queued', message: 'triggered' } }),
      })
      return
    }

    if (url.match(/\/api\/v1\/models\/project\/\d+\/configs$/)) {
      if (method === 'POST') {
        const payload = route.request().postDataJSON() as Record<string, unknown>
        const created = { id: 666, project_id: 1, model_definition_id: payload.model_definition_id, custom_config: null, is_default: Boolean(payload.is_default) }
        modelConfigs.push(created)
        await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: created }) })
        return
      }
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: modelConfigs }) })
      return
    }

    if (url.match(/\/api\/v1\/models$/)) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: CORS_HEADERS,
        body: JSON.stringify({ code: 0, message: 'ok', data: { providers, models } }),
      })
      return
    }

    if (url.includes('/api/v1/skills')) {
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: { items: [], page: 1, page_size: 20, total: 0 } }) })
      return
    }

    if (url.includes('/api/v1/tools')) {
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: { items: [], page: 1, page_size: 20, total: 0 } }) })
      return
    }

    if (url.includes('/api/v1/role-templates')) {
      await route.fulfill({ status: 200, contentType: 'application/json', headers: CORS_HEADERS, body: JSON.stringify({ code: 0, message: 'ok', data: { items: [] } }) })
      return
    }

    await route.continue()
  })
}

export { setupAuth, setupWorkspaceApis }
