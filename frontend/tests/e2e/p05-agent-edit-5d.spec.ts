import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P05 Agent Edit 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Agent Edit (/agents/:id)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
    await setupWorkspaceApis(page, {
      agents: [
        {
          id: 501,
          project_id: 1,
          name: 'API-AGENT-EDIT',
          role_name: 'assistant',
          skill_ids: [1],
          tool_ids: [1],
        },
      ],
    })
  })

  test('P05-D1 style', async ({ page }) => {
    await page.goto('/agents/501')
    await expect(page.getByTestId('agent-edit-page')).toBeVisible()
    await expect(page.getByTestId('agent-identity-panel')).toBeVisible()
    await expect(page.getByTestId('agent-capability-panel')).toBeVisible()
  })

  test('P05-D2 click event', async ({ page }) => {
    await page.goto('/agents/501')
    await page.getByTestId('agent-edit-save').click()
    await expect(page.getByText('保存成功')).toBeVisible()
  })

  test('P05-D3 field mapping', async ({ page }) => {
    await page.goto('/agents/501')
    await page.getByTestId('agent-edit-role-template').locator('select').selectOption('backend_engineer')
    await expect(page.getByTestId('agent-edit-execution-mode')).toHaveValue('code_runtime')
  })

  test('P05-D4 state validation', async ({ page }) => {
    await page.goto('/agents/501')
    await expect(page.getByTestId('agent-policy-panel')).toBeVisible()
    await expect(page.getByTestId('agent-edit-policy-max-iterations')).toBeVisible()
  })

  test('P05-D5 data interaction/constraints', async ({ page }) => {
    await page.goto('/agents/501')
    await page.getByTestId('agent-edit-role-template').locator('select').selectOption('product_manager')
    await expect(page.getByTestId('agent-edit-name-input')).toHaveValue('Product Manager')
  })
})

