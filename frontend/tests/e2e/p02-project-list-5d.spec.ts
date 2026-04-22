import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P02 Project List 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Projects List (/projects)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P02-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page, { projects: [] })
    await page.goto('/projects')
    await expect(page.getByTestId('projects-workspace-page')).toBeVisible()
    await expect(page.getByTestId('projects-stats-row')).toBeVisible()
    await expect(page.getByTestId('projects-card-region')).toBeVisible()
  })

  test('P02-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, { projects: [] })
    await page.goto('/projects')
    await page.getByTestId('projects-card-create').click()
    await expect(page.getByRole('dialog')).toBeVisible()
  })

  test('P02-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      projects: [
        {
          id: 101,
          owner_id: 1,
          name: 'API-PROJECT-LIST',
          description: 'API-PROJECT-DESC',
          status: 'draft',
          updated_relative: '2 hours ago',
        },
      ],
    })
    await page.goto('/projects')
    await expect(page.getByTestId('project-card-name').first()).toContainText('API-PROJECT-LIST')
    await expect(page.getByTestId('project-card-status').first()).toContainText(/draft/i)
    await expect(page.getByTestId('project-card-updated').first()).toContainText(/2\s*hours\s*ago/i)
  })

  test('P02-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { projects: [] })
    await page.goto('/projects')
    await expect(page.getByTestId('project-empty-state')).toBeVisible()
    await expect(page.getByTestId('project-card-item')).toHaveCount(0)
    await expect(page.locator('[data-testid="projects-card-region"] .el-table__header-wrapper')).toHaveCount(0)
    await expect(page.getByText('No Data')).toHaveCount(0)
  })

  test('P02-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, { projects: [] })
    await page.goto('/projects')
    await page.getByTestId('projects-card-create').click()
    const dialog = page.getByRole('dialog')
    await dialog.getByLabel('Name').fill('CREATED-PROJECT-5D')
    await dialog.getByLabel('Description').fill('CREATED-DESC-5D')
    await dialog.getByRole('button', { name: 'Create' }).click()
    await expect(page.getByText('CREATED-PROJECT-5D')).toBeVisible()
  })
})

