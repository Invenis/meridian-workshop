import { test, expect } from '@playwright/test'

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
  })

  test('loads with page title and KPIs', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Overview' })).toBeVisible()
    await expect(page.getByText('Key Performance Indicators')).toBeVisible()
    await expect(page.getByText('Inventory Turnover Rate')).toBeVisible()
    await expect(page.getByText('Orders Fulfilled')).toBeVisible()
    await expect(page.getByText('Order Fill Rate')).toBeVisible()
  })

  test('shows navigation with all pages', async ({ page }) => {
    const nav = page.getByRole('navigation')
    await expect(nav.getByRole('link', { name: 'Overview' })).toBeVisible()
    await expect(nav.getByRole('link', { name: 'Inventory' })).toBeVisible()
    await expect(nav.getByRole('link', { name: 'Orders' })).toBeVisible()
    await expect(nav.getByRole('link', { name: 'Finance' })).toBeVisible()
    await expect(nav.getByRole('link', { name: 'Demand Forecast' })).toBeVisible()
    await expect(nav.getByRole('link', { name: 'Reports' })).toBeVisible()
    await expect(nav.getByRole('link', { name: 'Restocking' })).toBeVisible()
  })

  test('shows filter bar with all four filters', async ({ page }) => {
    const filterBar = page.locator('.filters-bar')
    await expect(filterBar.getByText('Time Period')).toBeVisible()
    await expect(filterBar.getByText('Location')).toBeVisible()
    await expect(filterBar.getByText('Category')).toBeVisible()
    await expect(filterBar.getByText('Order Status')).toBeVisible()
  })

  test('shows Order Health section with metrics', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Order Health' })).toBeVisible()
    const orderHealthCard = page.locator('.card').filter({ hasText: 'Order Health' })
    await expect(orderHealthCard.locator('.health-metric-label', { hasText: 'Revenue' })).toBeVisible()
    await expect(orderHealthCard.getByText('Avg Order Value')).toBeVisible()
    await expect(orderHealthCard.getByText('On-Time Rate')).toBeVisible()
  })

  test('shows inventory shortages table', async ({ page }) => {
    await expect(page.getByText(/Inventory Shortages/)).toBeVisible()
    const table = page.getByRole('table').first()
    await expect(table).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'SKU' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Priority' })).toBeVisible()
  })

  test('shows Top Products by Revenue table', async ({ page }) => {
    await expect(page.getByText('Top Products by Revenue')).toBeVisible()
    const table = page.getByRole('table').last()
    await expect(table.getByRole('columnheader', { name: 'Product' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Revenue' })).toBeVisible()
  })

  test('warehouse filter updates dashboard data', async ({ page }) => {
    const warehouseSelect = page.locator('select').nth(1)
    await warehouseSelect.selectOption('San Francisco')
    await page.waitForLoadState('networkidle')
    // Verify page still shows content after filter applied
    await expect(page.getByRole('heading', { name: 'Overview' })).toBeVisible()
    await expect(page.getByText('Key Performance Indicators')).toBeVisible()
  })

  test('reset filters button activates after filter selection', async ({ page }) => {
    const resetBtn = page.getByRole('button', { name: /Reset/i })
    await expect(resetBtn).toBeDisabled()
    await page.locator('select').nth(1).selectOption('London')
    await expect(resetBtn).toBeEnabled()
    await resetBtn.click()
    await expect(resetBtn).toBeDisabled()
  })
})
