import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P07 Workflow List 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Workflow List (/workflows)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P07-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page, { workflows: [] })
    await page.goto('/workflows')
    await expect(page.getByTestId('workflow-workspace-page')).toBeVisible()
    await expect(page.getByTestId('workflow-card-region')).toBeVisible()
  })

  test('P07-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, { workflows: [] })
    await page.goto('/workflows')
    await page.getByTestId('workflow-col-create').click()
    await expect(page.getByRole('dialog')).toBeVisible()
  })

  test('P07-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [
        {
          id: 701,
          project_id: 1,
          name: 'API-WORKFLOW-5D',
          description: 'wf',
          status: 'active',
          version: 9,
          updated_relative: '44 min ago',
          nodes: [{ id: 'n1' }, { id: 'n2' }],
        },
      ],
    })
    await page.goto('/workflows')
    await expect(page.getByTestId('workflow-col-name').first()).toContainText('API-WORKFLOW-5D')
    await expect(page.getByTestId('workflow-col-status').first()).toContainText(/active/i)
    await expect(page.getByTestId('workflow-col-version').first()).toContainText(/9/)
    await expect(page.getByTestId('workflow-col-updated').first()).toContainText(/44\s*min/i)
  })

  test('P07-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { workflows: [] })
    await page.goto('/workflows')
    await expect(page.getByTestId('workflow-empty-state')).toBeVisible()
    await expect(page.getByTestId('workflow-card-item')).toHaveCount(0)
    await expect(page.locator('[data-testid="workflow-card-region"] .el-table__header-wrapper')).toHaveCount(0)
    await expect(page.getByText('No Data')).toHaveCount(0)
  })

  test('P07-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, { workflows: [] })
    await page.goto('/workflows')
    await page.getByTestId('workflow-col-create').click()
    const dialog = page.getByRole('dialog')
    await dialog.getByLabel('Name').fill('CREATED-WORKFLOW-5D')
    await dialog.getByRole('button', { name: 'Create' }).click()
    await expect(page.getByText('CREATED-WORKFLOW-5D')).toBeVisible()
  })
})

