import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P03 Project Detail 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Project Detail (/projects/:id)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P03-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page)
    await page.goto('/projects/1')
    await expect(page.getByTestId('project-detail-page')).toBeVisible()
    await expect(page.getByTestId('project-summary-panel')).toBeVisible()
    await expect(page.getByTestId('project-quick-stats')).toBeVisible()
  })

  test('P03-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [{ id: 301, project_id: 1, name: 'WF-A', description: '', nodes: [] }],
    })
    await page.goto('/projects/1')
    await page.getByTestId('project-recent-workflow-item').first().click()
    await expect(page).toHaveURL(/\/workflows\/301\/editor$/)
  })

  test('P03-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      projectDetail: {
        id: 1,
        owner_id: 1,
        name: 'API-PROJECT-DETAIL',
        description: 'API-PROJECT-DETAIL-DESC',
        status: 'paused',
        default_model_name: 'API-DEFAULT-MODEL',
        updated_relative: '39 minutes ago',
      },
      workflows: [],
      runs: [],
    })
    await page.goto('/projects/1')
    await expect(page.getByTestId('project-summary-name')).toContainText('API-PROJECT-DETAIL')
    await expect(page.getByTestId('project-summary-status')).toContainText(/paused/i)
    await expect(page.getByTestId('project-summary-meta-model')).toContainText('API-DEFAULT-MODEL')
    await expect(page.getByTestId('project-summary-meta-updated')).toContainText(/39\s*minutes\s*ago/i)
  })

  test('P03-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { workflows: [], runs: [] })
    await page.goto('/projects/1')
    await expect(page.getByTestId('project-detail-workflows-empty-state')).toBeVisible()
    await expect(page.getByTestId('project-detail-runs-empty-state')).toBeVisible()
    await expect(page.locator('[data-testid="project-recent-workflow-item"]')).toHaveCount(0)
    await expect(page.locator('[data-testid="project-recent-run-item"]')).toHaveCount(0)
    await expect(page.getByText('No Data')).toHaveCount(0)
  })

  test('P03-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, { workflows: [], runs: [] })
    await page.goto('/projects/1')
    await expect(page.getByText('run_128')).toHaveCount(0)
    await expect(page.getByText('run_127')).toHaveCount(0)
  })
})

