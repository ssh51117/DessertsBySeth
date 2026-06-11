/**
 * Checkout user flow.
 *
 * The menu page is a Next.js server component — its products fetch runs server-side
 * and cannot be intercepted by page.route(). These tests start the Django backend
 * automatically (via playwright.config.ts webServer) and rely on it having at least
 * one available product.
 *
 * Client-side API calls (preorder-window, preorders POST) are intercepted with
 * page.route() so checkout behavior can be controlled without touching real Stripe.
 *
 * The @stripe-tagged test requires a real Stripe test client_secret — set
 * STRIPE_TEST_CLIENT_SECRET in .env.local to enable it.
 */
import { test, expect } from '@playwright/test'

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8000'

/** Add the first available product to cart and navigate to /cart via the nav link. */
async function addFirstProductToCartAndGoToCart(page: import('@playwright/test').Page) {
  await page.goto('/menu')
  await page.getByRole('button', { name: 'Add to Cart' }).first().click()
  await page.getByRole('link', { name: 'Cart' }).click()
}

test.describe('checkout flow', () => {
  test('empty cart shows empty message', async ({ page }) => {
    await page.goto('/cart')
    await expect(page.getByText('Your cart is empty.')).toBeVisible()
  })

  test('checkout button is disabled until both name and email are filled', async ({ page }) => {
    await page.route(`${BACKEND}/preorder-window/current/`, route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([{
          id: 1,
          opens_at: new Date(Date.now() - 3600000).toISOString(),
          closes_at: new Date(Date.now() + 86400000).toISOString(),
          pickup_date: '2026-06-14',
          active: true,
          notified_at: null,
          listings: [{ name: 'Chocolate Cake', unit_price: '12.00', limit: 10, remaining: 10 }],
        }]),
      })
    )

    await addFirstProductToCartAndGoToCart(page)

    const checkoutBtn = page.getByRole('button', { name: 'Checkout' })
    await expect(checkoutBtn).toBeDisabled()

    await page.getByPlaceholder('Name').fill('Jane Smith')
    await expect(checkoutBtn).toBeDisabled()

    await page.getByPlaceholder('Email').fill('jane@example.com')
    await expect(checkoutBtn).toBeEnabled()
  })

  test('no active preorder window shows error message', async ({ page }) => {
    await page.route(`${BACKEND}/preorder-window/current/`, route =>
      route.fulfill({ status: 200, contentType: 'application/json', body: '[]' })
    )

    await addFirstProductToCartAndGoToCart(page)
    await page.getByPlaceholder('Name').fill('Jane Smith')
    await page.getByPlaceholder('Email').fill('jane@example.com')
    await page.getByRole('button', { name: 'Checkout' }).click()

    await expect(page.getByText('No active preorder window')).toBeVisible()
  })

  test('stripe payment form appears after successful preorder creation @stripe', async ({ page }) => {
    const clientSecret = process.env.STRIPE_TEST_CLIENT_SECRET
    if (!clientSecret) {
      test.skip(true, 'Set STRIPE_TEST_CLIENT_SECRET in .env.local to run this test')
    }

    await page.route(`${BACKEND}/preorder-window/current/`, route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([{
          id: 1,
          opens_at: new Date(Date.now() - 3600000).toISOString(),
          closes_at: new Date(Date.now() + 86400000).toISOString(),
          pickup_date: '2026-06-14',
          active: true,
          notified_at: null,
          listings: [{ name: 'Chocolate Cake', unit_price: '12.00', limit: 10, remaining: 10 }],
        }]),
      })
    )
    await page.route(`${BACKEND}/preorders/`, route =>
      route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({
          client_secret: clientSecret,
          window: { pickup_date: '2026-06-14' },
          customer_name: 'Jane Smith',
          customer_email: 'jane@example.com',
          customer_phone: null,
          stripe_payment_status: 'requires_payment_method',
          total: '12.00',
          items: [{ product_listing: 1, quantity: 1 }],
        }),
      })
    )

    await addFirstProductToCartAndGoToCart(page)
    await page.getByPlaceholder('Name').fill('Jane Smith')
    await page.getByPlaceholder('Email').fill('jane@example.com')
    await page.getByRole('button', { name: 'Checkout' }).click()

    // Stripe Elements iframe should appear
    await expect(
      page.frameLocator('iframe[name*="stripe"]').first().getByRole('textbox').first()
    ).toBeVisible({ timeout: 10000 })
  })
})
