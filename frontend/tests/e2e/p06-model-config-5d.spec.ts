import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P06 Model Config 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Model Config (/models)', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuth(page)
  })

  test('P06-D1 style', async ({ page }) => {
    await setupWorkspaceApis(page)
    await page.goto('/models')
    await expect(page.getByTestId('models-workspace-page')).toBeVisible()
    await expect(page.getByTestId('model-config-page')).toBeVisible()
    await expect(page.getByTestId('model-config-table')).toBeVisible()
  })

  test('P06-D2 click event', async ({ page }) => {
    await setupWorkspaceApis(page)
    await page.goto('/models')
    await page.getByTestId('model-add-config-btn').click()
    await expect(page.getByRole('dialog')).toBeVisible()
  })

  test('P06-D3 field mapping', async ({ page }) => {
    await setupWorkspaceApis(page, {
      providers: [{ id: 1, name: 'API-PROVIDER-5D', provider_type: 'api', is_active: true }],
      models: [
        {
          id: 1,
          provider_id: 1,
          model_name: 'api/model-5d',
          display_name: 'API-MODEL-5D',
          model_type: 'chat',
          context_window: 1234,
          is_active: true,
        },
      ],
      modelConfigs: [{ id: 1, project_id: 1, model_definition_id: 1, custom_config: null, is_default: true }],
    })
    await page.goto('/models')
    await expect(page.getByText('API-PROVIDER-5D')).toBeVisible()
    await expect(page.getByText('API-MODEL-5D')).toBeVisible()
  })

  test('P06-D4 state validation', async ({ page }) => {
    await setupWorkspaceApis(page, { providers: [], models: [], modelConfigs: [] })
    await page.goto('/models')
    await expect(page.getByTestId('model-empty-state')).toBeVisible()
    await expect(page.locator('[data-testid^="model-row-"]')).toHaveCount(0)
    await expect(page.locator('[data-testid="model-config-page"] .el-table__header-wrapper')).toHaveCount(0)
    await expect(page.getByText('No Data')).toHaveCount(0)
  })

  test('P06-D5 data interaction/constraints', async ({ page }) => {
    await setupWorkspaceApis(page, {
      providers: [{ id: 1, name: 'API-PROVIDER-5D', provider_type: 'api', is_active: true }],
      models: [
        {
          id: 1,
          provider_id: 1,
          model_name: 'api/model-5d',
          display_name: 'API-MODEL-5D',
          model_type: 'chat',
          context_window: 1234,
          is_active: true,
        },
      ],
      modelConfigs: [],
    })
    await page.goto('/models')
    await page.getByTestId('model-add-config-btn').click()
    await page.getByRole('dialog').getByRole('button', { name: 'Confirm' }).click()
    await expect(page.getByText('API-MODEL-5D')).toBeVisible()
  })
})

