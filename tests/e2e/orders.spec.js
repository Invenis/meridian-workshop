import { test, expect } from '@playwright/test'

test.describe('Orders', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/orders')
    await page.waitForLoadState('networkidle')
  })

  test('loads with page title and table', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Orders', exact: true })).toBeVisible()
    await expect(page.getByText('View and manage customer orders')).toBeVisible()
    await expect(page.getByRole('table')).toBeVisible()
  })

  test('shows status summary cards', async ({ page }) => {
    const statsGrid = page.locator('.stats-grid')
    await expect(statsGrid.locator('.stat-label', { hasText: 'Delivered' })).toBeVisible()
    await expect(statsGrid.locator('.stat-label', { hasText: 'Shipped' })).toBeVisible()
    await expect(statsGrid.locator('.stat-label', { hasText: 'Processing' })).toBeVisible()
    await expect(statsGrid.locator('.stat-label', { hasText: 'Backordered' })).toBeVisible()
  })

  test('shows table with required columns', async ({ page }) => {
    const table = page.getByRole('table')
    await expect(table.getByRole('columnheader', { name: 'Order Number' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Customer' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Status' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Total Value' })).toBeVisible()
  })

  test('shows all orders count in header', async ({ page }) => {
    await expect(page.getByText(/All Orders \(\d+\)/)).toBeVisible()
  })

  test('orders have status badges', async ({ page }) => {
    const badges = page.locator('.badge')
    await expect(badges.first()).toBeVisible()
    const count = await badges.count()
    expect(count).toBeGreaterThan(0)
  })

  test('order rows display order numbers', async ({ page }) => {
    const rows = page.getByRole('table').getByRole('row')
    const rowCount = await rows.count()
    expect(rowCount).toBeGreaterThan(1) // at least header + one order

    const firstDataRow = rows.nth(1)
    await expect(firstDataRow.getByRole('cell').first()).toContainText(/ORD-\d+/)
  })
})
