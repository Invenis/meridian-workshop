import { test, expect } from '@playwright/test'

test.describe('Inventory', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/inventory')
    await page.waitForLoadState('networkidle')
  })

  test('loads with page title and table', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Inventory' })).toBeVisible()
    await expect(page.getByText('Track and manage all inventory items')).toBeVisible()
    await expect(page.getByRole('table')).toBeVisible()
  })

  test('shows table with required columns', async ({ page }) => {
    const table = page.getByRole('table')
    await expect(table.getByRole('columnheader', { name: 'SKU' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Item Name' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Category' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Quantity on Hand' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Status' })).toBeVisible()
  })

  test('search filters table rows', async ({ page }) => {
    const searchInput = page.getByPlaceholder('Search by item name...')
    await expect(searchInput).toBeVisible()

    const initialRows = await page.getByRole('table').getByRole('row').count()
    await searchInput.fill('Servo')
    await page.waitForTimeout(300)

    const filteredRows = await page.getByRole('table').getByRole('row').count()
    expect(filteredRows).toBeLessThan(initialRows)
    expect(filteredRows).toBeGreaterThan(1) // header + at least one result
  })

  test('clear search button appears after typing', async ({ page }) => {
    const searchInput = page.getByPlaceholder('Search by item name...')
    await searchInput.fill('PCB')
    await expect(page.locator('.clear-search')).toBeVisible()
    await page.locator('.clear-search').click()
    await expect(searchInput).toHaveValue('')
  })

  test('shows SKU count in card header', async ({ page }) => {
    await expect(page.getByText(/Stock Levels \(\d+ SKUs\)/)).toBeVisible()
  })

  test('table rows are clickable', async ({ page }) => {
    const firstRow = page.getByRole('table').getByRole('row').nth(1)
    await expect(firstRow).toBeVisible()
    await firstRow.click()
    await expect(page.locator('.modal-overlay')).toBeVisible()
  })
})
