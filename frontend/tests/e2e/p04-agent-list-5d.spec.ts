import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P04 Agent List 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Agents List (/agents)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P04-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page, { agents: [] })
    await page.goto('/agents')
    await expect(page.getByTestId('agents-workspace-page')).toBeVisible()
    await expect(page.getByTestId('agents-card-region')).toBeVisible()
  })

  test('P04-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, { agents: [] })
    await page.goto('/agents')
    await page.getByTestId('agents-section-create').click()
    await expect(page.getByRole('dialog')).toBeVisible()
  })

  test('P04-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      agents: [
        {
          id: 401,
          project_id: 1,
          name: 'API-AGENT-LIST',
          role_name: 'api_role',
          model_name: 'API-AGENT-MODEL',
          skill_ids: [1, 2, 3, 4],
          tool_ids: [11, 12],
        },
      ],
    })
    await page.goto('/agents')
    await expect(page.getByText('API-AGENT-LIST')).toBeVisible()
    await expect(page.getByTestId('agent-card-model').first()).toContainText('API-AGENT-MODEL')
    await expect(page.getByTestId('agent-card-skill-count').first()).toContainText(/4/)
    await expect(page.getByTestId('agent-card-tool-count').first()).toContainText(/2/)
  })

  test('P04-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { agents: [] })
    await page.goto('/agents')
    await expect(page.getByTestId('agents-empty-state')).toBeVisible()
    await expect(page.getByTestId('agent-card-item')).toHaveCount(0)
    await expect(page.locator('[data-testid="agents-card-region"] .el-table__header-wrapper')).toHaveCount(0)
    await expect(page.getByText('No Data')).toHaveCount(0)
  })

  test('P04-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, { agents: [] })
    await page.goto('/agents')
    await page.getByTestId('agents-section-create').click()
    const dialog = page.getByRole('dialog')
    await dialog.getByLabel('Name').fill('CREATED-AGENT-5D')
    await dialog.getByLabel('Role').fill('assistant')
    await dialog.getByRole('button', { name: 'Create' }).click()
    await expect(page.getByText('CREATED-AGENT-5D')).toBeVisible()
  })
})

