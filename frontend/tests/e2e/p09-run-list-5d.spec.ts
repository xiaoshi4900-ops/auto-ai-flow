import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P09 Run List 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Run List (/runs)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P09-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [] })
    await page.goto('/runs')
    await expect(page.getByTestId('runs-workspace-page')).toBeVisible()
    await expect(page.getByTestId('run-list-page')).toBeVisible()
    await expect(page.getByTestId('run-list-region')).toBeVisible()
  })

  test('P09-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [{ id: 901, workflow_id: 1, status: 'success' }] })
    await page.goto('/runs')
    await page.getByTestId('run-row-detail').first().click()
    await expect(page).toHaveURL(/\/runs\/901$/)
  })

  test('P09-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      runs: [{ id: 901, workflow_id: 1, status: 'failed', latency_ms: 4100, token_usage_total: 9876 }],
    })
    await page.goto('/runs')
    await expect(page.getByTestId('run-col-id').first()).toContainText(/901/)
    await expect(page.getByTestId('run-col-status').first()).toContainText(/failed/i)
    await expect(page.getByTestId('run-col-latency').first()).toContainText(/4\.1s|4100/i)
    await expect(page.getByTestId('run-col-tokens').first()).toContainText(/9876/)
  })

  test('P09-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [] })
    await page.goto('/runs')
    await expect(page.getByTestId('run-empty-state')).toBeVisible()
    await expect(page.locator('[data-testid^="run-row-"]')).toHaveCount(0)
    await expect(page.locator('[data-testid="run-list-region"] .el-table__header-wrapper')).toHaveCount(0)
    await expect(page.getByText('No Data')).toHaveCount(0)
  })

  test('P09-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, {
      runs: [{ id: 901, workflow_id: 1, status: 'failed' }],
    })
    await page.goto('/runs')
    await page.getByTestId('runs-filter-failed').click()
    await expect(page).toHaveURL(/status=failed/)
  })
})

