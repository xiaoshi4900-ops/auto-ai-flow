import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P10 Run Detail 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Run Detail (/runs/:id)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P10-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [{ id: 1001, workflow_id: 1, status: 'success' }] })
    await page.goto('/runs/1001')
    await expect(page.getByTestId('run-detail-page')).toBeVisible()
    await expect(page.getByTestId('run-header-region')).toBeVisible()
    await expect(page.getByTestId('run-timeline-region')).toBeVisible()
  })

  test('P10-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [{ id: 1001, workflow_id: 1, status: 'success' }] })
    await page.goto('/runs/1001')
    await expect(page.getByTestId('run-detail-action-back')).toBeVisible()
    await page.getByTestId('run-detail-action-back').click()
    await expect(page).toHaveURL(/\/runs$/)
  })

  test('P10-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      runs: [{ id: 1001, workflow_id: 1, status: 'failed', latency_ms: 5000, token_usage_total: 111 }],
    })
    await page.goto('/runs/1001')
    await expect(page.getByTestId('run-status-chip')).toContainText(/failed/i)
    await expect(page.getByTestId('run-meta-latency')).toContainText(/5\.0s|5000/i)
    await expect(page.getByTestId('run-meta-tokens')).toContainText(/111/)
  })

  test('P10-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [{ id: 1001, workflow_id: 1, status: 'success' }] })
    await page.goto('/runs/1001?load_error=1')
    await expect(page.getByTestId('run-code-runtime-load-error')).toBeVisible()
  })

  test('P10-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, { runs: [{ id: 1001, workflow_id: 1, status: 'success' }] })
    await page.goto('/runs/1001?mode=code_runtime')
    await expect(page.getByTestId('run-code-iterations-region')).toBeVisible()
    await expect(page.getByTestId('run-code-iteration-item')).toHaveCount(1)
  })
})
