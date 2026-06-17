import { test, expect } from '@playwright/test'

test.describe('Restocking', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/restocking')
    await page.waitForLoadState('networkidle')
  })

  test('loads with page title and budget input', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Restocking Recommendations' })).toBeVisible()
    await expect(page.getByText('Budget Parameters')).toBeVisible()
    await expect(page.getByPlaceholder('Enter budget amount...')).toBeVisible()
  })

  test('budget input has default value', async ({ page }) => {
    const budgetInput = page.getByPlaceholder('Enter budget amount...')
    await expect(budgetInput).toHaveValue('50000')
  })

  test('calculate button is visible', async ({ page }) => {
    await expect(page.getByRole('button', { name: 'Calculate' })).toBeVisible()
  })

  test('calculate returns recommendations', async ({ page }) => {
    await page.getByRole('button', { name: 'Calculate' }).click()
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Purchase Recommendations')).toBeVisible()
    const table = page.getByRole('table')
    await expect(table).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'SKU' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Item Name' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Priority' })).toBeVisible()
  })

  test('shows summary bar after calculation', async ({ page }) => {
    await page.getByRole('button', { name: 'Calculate' }).click()
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Recommended Items')).toBeVisible()
    await expect(page.getByText('Total Estimated Cost')).toBeVisible()
    await expect(page.getByText('Remaining Budget')).toBeVisible()
  })

  test('low budget shows empty state', async ({ page }) => {
    const budgetInput = page.getByPlaceholder('Enter budget amount...')
    await budgetInput.fill('1')
    await page.getByRole('button', { name: 'Calculate' }).click()
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('No restocking required')).toBeVisible()
  })

  test('recommendations table has priority badges', async ({ page }) => {
    await page.getByRole('button', { name: 'Calculate' }).click()
    await page.waitForLoadState('networkidle')

    const rows = page.getByRole('table').getByRole('row')
    const rowCount = await rows.count()
    if (rowCount > 1) {
      const badges = page.locator('.badge')
      const badgeCount = await badges.count()
      expect(badgeCount).toBeGreaterThan(0)
    }
  })
})
