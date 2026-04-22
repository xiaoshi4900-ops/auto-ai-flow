import { expect, test } from '@playwright/test'
import { setupAuth, setupWorkspaceApis } from './matrix-fixtures'

/**
 * P01 Login 5D contract suite.
 * Split from the original workspace-page-5d-matrix contract file to keep
 * page-level context isolated.
 */

test.describe('Page 5D Matrix - Login (/login)', () => {
  test('P01-D1 style', async ({ page }) => {
    await page.goto('/login')
    await expect(page.getByTestId('login-page')).toBeVisible()
    await expect(page.getByTestId('login-brand')).toBeVisible()
    await expect(page.getByTestId('login-panel')).toBeVisible()
  })

  test('P01-D2 click event', async ({ page }) => {
    await page.route('**/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 0,
          message: 'ok',
          data: { access_token: 'a', refresh_token: 'b', token_type: 'bearer' },
        }),
      })
    })
    await page.route('**/api/v1/auth/me', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ code: 0, message: 'ok', data: { id: 1, username: 'operator' } }),
      })
    })
    await page.goto('/login')
    await page.getByTestId('login-username').fill('operator')
    await page.getByTestId('login-password').fill('123456')
    await page.getByTestId('login-submit').click()
    await expect(page).toHaveURL(/\/projects$/)
  })

  test('P01-D3 field mapping', async ({ page }) => {
    await page.route('**/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ code: 401, message: 'API-LOGIN-ERROR-MESSAGE' }),
      })
    })
    await page.goto('/login')
    await page.getByTestId('login-username').fill('x')
    await page.getByTestId('login-password').fill('y')
    await page.getByTestId('login-submit').click()
    await expect(page.getByTestId('login-message')).toContainText('API-LOGIN-ERROR-MESSAGE')
  })

  test('P01-D4 state validation', async ({ page }) => {
    await page.route('**/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 0,
          message: 'ok',
          data: { access_token: 'a', refresh_token: 'b', token_type: 'bearer' },
        }),
      })
    })
    await page.route('**/api/v1/auth/me', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ code: 0, message: 'ok', data: { id: 1, username: 'operator' } }),
      })
    })
    await page.goto('/login')
    await page.getByTestId('login-username').fill('operator')
    await page.getByTestId('login-password').fill('123456')
    await page.getByTestId('login-submit').click()
    await expect(page.getByTestId('login-submit')).toBeDisabled()
  })

  test('P01-D5 data interaction/constraints', async ({ page }) => {
    let payload: Record<string, unknown> | null = null
    await page.route('**/api/v1/auth/login', async (route) => {
      payload = route.request().postDataJSON() as Record<string, unknown>
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ code: 401, message: 'INVALID' }),
      })
    })
    await page.goto('/login')
    await page.getByTestId('login-username').fill('U-API')
    await page.getByTestId('login-password').fill('P-API')
    await page.getByTestId('login-submit').click()
    expect(payload).toMatchObject({ username: 'U-API', password: 'P-API' })
  })
})

