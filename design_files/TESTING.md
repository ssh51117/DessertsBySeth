# Testing — DessertsBySeth

## Quick Start

```bash
# Backend (42 tests)
cd backend
pytest

# Frontend components (19 tests)
cd frontend
pnpm test

# E2E browser tests (9 tests, 1 skipped)
cd frontend
pnpm test:e2e          # headless
pnpm test:e2e:ui       # interactive Playwright UI
```

> **Node requirement**: E2E and unit tests require Node 22+. Switch with `nvm use 22` before running frontend tests.

---

## Test Inventory

### Backend — `pytest` (42 tests)

| File | Tests | What's covered |
|------|-------|---------------|
| `api/tests/test_flows.py` | 20 | Full HTTP round-trips: preorder creation, mailing list subscribe/unsubscribe, guinea pig register/unregister, drop claim/cancel, custom orders, products endpoint, preorder window, preorder status |
| `api/tests/test_inventory.py` | 7 | Capacity exceeded (409), Stripe error rollback (no DB row), closed/inactive window, mismatched total, drop full, registration closed |
| `api/tests/test_webhook.py` | 8 | Stripe webhook: succeeded→CONFIRMED, mailer failure resilience, payment_failed, canceled, invalid signature (403), unknown event, unknown order, no metadata |
| `api/tests/test_mailer.py` | 7 | Resend email: order confirmation, guinea pig drop notification, preorder window notification, mailing list blast with unsubscribe tokens |

**Setup**: `backend/dessertsbyseth/settings_test.py` overrides all external credentials with fakes and uses an in-memory SQLite DB — no `.env` file needed in CI.

```bash
cd backend
pip install pytest pytest-django factory-boy
pytest
pytest api/tests/test_flows.py -v   # run one file
```

### Frontend Components — `vitest` (19 tests)

| File | Tests | What's covered |
|------|-------|---------------|
| `src/components/CartProvider.test.tsx` | 7 | Cart context: throws outside provider, empty initial state, add/update/remove items, clear, item isolation |
| `src/components/AddToCartButton.test.tsx` | 5 | Button renders, add → quantity controls, + increments, − decrements, − at 1 removes |
| `src/components/CheckoutForm.test.tsx` | 7 | Pay button disabled when stripe/elements null, enabled when both ready, card error message, generic error message, button re-enabled after error |

```bash
cd frontend
pnpm test          # run once
pnpm test:watch    # watch mode
```

### E2E Browser Tests — `playwright` (9 passed, 1 skipped)

Tests launch both servers automatically (Next.js dev on :3000, Django on :8000) if they aren't already running.

| File | Tests | What's covered |
|------|-------|---------------|
| `e2e/menu-and-cart.spec.ts` | 6 | Menu heading, Add to Cart buttons appear, click shows quantity controls, + increments, − at 1 restores button, cart shows items and total |
| `e2e/checkout.spec.ts` | 4 (1 skipped) | Empty cart message, checkout button disabled until name+email filled, no active preorder window error, Stripe payment form after preorder creation (requires `STRIPE_TEST_CLIENT_SECRET`) |

**Important architectural note**: The `/menu` page is a Next.js server component — its product fetch runs server-side and cannot be intercepted by `page.route()`. Only client-side API calls (preorder-window, preorders POST) are interceptable. Tests that need products in the cart navigate via the UI (`/menu` → "Add to Cart" → Cart nav link) so cart state is preserved as a client-side navigation.

```bash
cd frontend
pnpm test:e2e          # all tests
pnpm test:e2e:ui       # interactive UI mode
```

To enable the Stripe E2E test, add to `frontend/.env.local`:
```
STRIPE_TEST_CLIENT_SECRET=pi_test_...
```

---

## Architecture

```
backend/
  pytest.ini                           # points to settings_test, -v --tb=short
  conftest.py                          # shared fixtures: api_client, open_window, listing, etc.
  dessertsbyseth/
    settings_test.py                   # fake credentials + in-memory SQLite
  api/tests/
    factories.py                       # factory_boy: Product, PreorderWindow, Listing, Preorder, etc.
    test_flows.py                      # integration: full HTTP round-trips
    test_inventory.py                  # edge cases: capacity, rollback, closed windows
    test_webhook.py                    # Stripe webhook handling
    test_mailer.py                     # Resend email service

frontend/
  vitest.config.ts                     # jsdom, globals, setupFiles
  playwright.config.ts                 # 2 webServers (Next.js + Django), chromium only
  src/test/
    setup.ts                           # @testing-library/jest-dom
    helpers.tsx                        # renderWithCart() wraps in CartProvider
  src/components/
    CartProvider.test.tsx
    AddToCartButton.test.tsx
    CheckoutForm.test.tsx
  e2e/
    menu-and-cart.spec.ts
    checkout.spec.ts
```

## Stripe Mocking Strategy

- **Backend unit/integration**: `@patch('stripe.PaymentIntent.create')` and `@patch('api.views.stripe.Webhook.construct_event')` — tests run without real credentials
- **Frontend components**: `vi.mock('@stripe/react-stripe-js')` returns controlled hook stubs
- **E2E (optional)**: Real Stripe test-mode `client_secret` via `STRIPE_TEST_CLIENT_SECRET` env var
