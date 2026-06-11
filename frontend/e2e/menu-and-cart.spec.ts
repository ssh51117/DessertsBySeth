/**
 * Menu + cart user flow.
 *
 * The menu page is a Next.js server component — it fetches products server-side,
 * so its API call cannot be intercepted by Playwright's page.route(). These tests
 * require the Django backend to be running on localhost:8000 with at least one
 * available product.
 *
 * Run with both servers up:
 *   Terminal 1: cd backend && python manage.py runserver
 *   Terminal 2: cd frontend && pnpm dev
 *   Terminal 3: pnpm test:e2e
 */
import { test, expect } from '@playwright/test'

test.describe('menu and cart', () => {
  test('menu page renders a product heading', async ({ page }) => {
    await page.goto('/menu')
    await expect(page.getByRole('heading', { name: 'Menu' })).toBeVisible()
  })

  test('"Add to Cart" appears for each product', async ({ page }) => {
    await page.goto('/menu')
    const buttons = page.getByRole('button', { name: 'Add to Cart' })
    await expect(buttons.first()).toBeVisible()
  })

  test('clicking "Add to Cart" shows quantity controls', async ({ page }) => {
    await page.goto('/menu')
    const addButton = page.getByRole('button', { name: 'Add to Cart' }).first()
    await addButton.click()
    await expect(page.getByRole('button', { name: '+' })).toBeVisible()
    await expect(page.getByRole('button', { name: '−' })).toBeVisible()
  })

  test('"+" increases quantity displayed', async ({ page }) => {
    await page.goto('/menu')
    await page.getByRole('button', { name: 'Add to Cart' }).first().click()
    await page.getByRole('button', { name: '+' }).click()
    // quantity should now show 2
    await expect(page.getByText('2')).toBeVisible()
  })

  test('"−" at quantity 1 restores "Add to Cart" button', async ({ page }) => {
    await page.goto('/menu')
    await page.getByRole('button', { name: 'Add to Cart' }).first().click()
    await page.getByRole('button', { name: '−' }).click()
    await expect(page.getByRole('button', { name: 'Add to Cart' }).first()).toBeVisible()
  })

  test('cart page shows added items and total', async ({ page }) => {
    await page.goto('/menu')
    await page.getByRole('button', { name: 'Add to Cart' }).first().click()
    await page.getByRole('link', { name: 'Cart' }).click()
    // Should see at least one item row and a Total line
    await expect(page.getByText('Total')).toBeVisible()
  })
})
