import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P08 Workflow Editor 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Workflow Editor (/workflows/:id/editor)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P08-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [{ id: 801, project_id: 1, name: 'WF-EDITOR-5D', description: '', nodes: [] }],
    })
    await page.goto('/workflows/801/editor')
    await expect(page.getByTestId('workflow-editor-page')).toBeVisible()
    await expect(page.getByTestId('editor-toolbar')).toBeVisible()
    await expect(page.getByTestId('editor-body')).toBeVisible()
  })

  test('P08-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [{ id: 801, project_id: 1, name: 'WF-EDITOR-5D', description: '', nodes: [] }],
    })
    await page.goto('/workflows/801/editor')
    await page.getByTestId('editor-btn-run').click()
    await expect(page.getByText(/run #9001/i)).toBeVisible()
  })

  test('P08-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [{ id: 801, project_id: 1, name: 'API-WF-NAME-EDITOR', description: '', nodes: [] }],
    })
    await page.goto('/workflows/801/editor')
    await expect(page.getByTestId('editor-workflow-name')).toContainText('API-WF-NAME-EDITOR')
  })

  test('P08-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [{ id: 801, project_id: 1, name: 'WF-EDITOR-5D', description: '', nodes: [] }],
    })
    await page.goto('/workflows/801/editor')
    await expect(page.getByTestId('node-palette')).toBeVisible()
    await expect(page.getByTestId('node-config-panel')).toBeVisible()
  })

  test('P08-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, {
      workflows: [{ id: 801, project_id: 1, name: 'WF-EDITOR-5D', description: '', nodes: [] }],
    })
    await page.goto('/workflows/801/editor')
    await page.getByTestId('editor-btn-save').click()
    await expect(page.getByText('Workflow 已保存')).toBeVisible()
  })
})

