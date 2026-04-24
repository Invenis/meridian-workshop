import { test, expect } from '@playwright/test'

test.describe('Reports', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/reports')
    await page.waitForLoadState('networkidle')
  })

  test('loads with page title', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Performance Reports' })).toBeVisible()
    await expect(page.getByText('View quarterly performance metrics and monthly trends')).toBeVisible()
  })

  test('shows quarterly performance table', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Quarterly Performance' })).toBeVisible()
    const table = page.getByRole('table').first()
    await expect(table.getByRole('columnheader', { name: 'Quarter' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Total Orders' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Total Revenue' })).toBeVisible()
    await expect(table.getByRole('columnheader', { name: 'Fulfillment Rate' })).toBeVisible()
  })

  test('quarterly table has data rows', async ({ page }) => {
    const table = page.getByRole('table').first()
    const rows = table.getByRole('row')
    const rowCount = await rows.count()
    expect(rowCount).toBeGreaterThan(1) // header + data rows

    // Should show quarter identifiers like Q1, Q2
    await expect(table.getByRole('cell', { name: /Q\d/ }).first()).toBeVisible()
  })

  test('shows monthly revenue trend chart', async ({ page }) => {
    await expect(page.getByText('Monthly Revenue Trend')).toBeVisible()
    await expect(page.locator('.bar-chart')).toBeVisible()
    const bars = page.locator('.bar')
    const barCount = await bars.count()
    expect(barCount).toBeGreaterThan(0)
  })

  test('shows month-over-month analysis table', async ({ page }) => {
    await expect(page.getByText('Month-over-Month Analysis')).toBeVisible()
    const tables = page.getByRole('table')
    const lastTable = tables.last()
    await expect(lastTable.getByRole('columnheader', { name: 'Month' })).toBeVisible()
    await expect(lastTable.getByRole('columnheader', { name: 'Revenue' })).toBeVisible()
    await expect(lastTable.getByRole('columnheader', { name: 'Growth Rate' })).toBeVisible()
  })

  test('shows summary stats', async ({ page }) => {
    await expect(page.getByText('Total Revenue (YTD)')).toBeVisible()
    await expect(page.getByText('Avg Monthly Revenue')).toBeVisible()
    await expect(page.getByText('Total Orders (YTD)')).toBeVisible()
    await expect(page.getByText('Best Performing Quarter')).toBeVisible()
  })
})
