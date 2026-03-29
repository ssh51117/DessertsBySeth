# Backend Design — Desserts By Seth

## Stack
- **Framework:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Payments:** Stripe
- **Email:** SendGrid (transactional emails + guinea pig notifications)
- **Task queue:** Celery + Redis (for async email sending)

---

## Models

### `MailingListSubscriber`
| Field | Type | Notes |
|-------|------|-------|
| `email` | EmailField (unique) | |
| `subscribed_at` | DateTimeField (auto) | |
| `auth_token` | UUIDField | Used in one-click unsubscribe links |

---

### `GuineaPig`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField | |
| `email` | EmailField (unique) | |
| `notes` | TextField (optional) | Dietary restrictions, preferences |
| `subscribed_at` | DateTimeField (auto) | |
| `active` | BooleanField | Can be deactivated without deletion |
| `auth_token` | UUIDField | Used in one-click unsubscribe links |

---

### `GuineaPigDrop`
Represents a batch of food available for guinea pigs to claim.

| Field | Type | Notes |
|-------|------|-------|
| `title` | CharField | e.g. "Extra Basque Cheesecakes" |
| `description` | TextField | What's available, any context |
| `available_from` | DateTimeField | Earliest pickup time |
| `available_until` | DateTimeField | Deadline to claim |
| `total_slots` | IntegerField | How many guinea pigs can claim this drop |
| `created_at` | DateTimeField (auto) | |
| `notified_at` | DateTimeField (nullable) | Set when emails are sent out |
| `registration_until` | DateTimeField | Deadline to register for the drop |

---

### `GuineaPigClaim`
A guinea pig's RSVP to a specific drop.

| Field | Type | Notes |
|-------|------|-------|
| `drop` | FK → GuineaPigDrop | |
| `guinea_pig` | FK → GuineaPig | |
| `pickup_time` | DateTimeField | Chosen by guinea pig from available slots |
| `registered_at` | DateTimeField (auto) | |
| `canceled` | BooleanField | Soft cancel |

**Constraint:** `unique_together(drop, guinea_pig)` — one claim per person per drop.
**Constraint:** Claims where `canceled=False` must not exceed `drop.total_slots`.

---

### `Product`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField | |
| `description` | TextField (optional) | |
| `price` | DecimalField | In dollars |
| `available` | BooleanField | Toggleable without deletion |
| `image` | CharField | Path/URL to image |

---

### `PreorderWindow`
Controls when orders are open and how many can be accepted for a given pickup week.

| Field | Type | Notes |
|-------|------|-------|
| `opens_at` | DateTimeField | When ordering opens (Monday evening) |
| `closes_at` | DateTimeField | When ordering closes (Thursday evening) |
| `pickup_date` | DateField | The Monday pickup date this window is for |
| `active` | BooleanField | Admin can manually open/close |
| `location` | CharField | Pickup location |
| `type` | CharField | `R` (Regular) / `P` (Pop-up) |

A cron job or admin action creates a new `PreorderWindow` each week.

---

### `PreorderListing`
Holds item name and price snapshot, controls max number of items that can be ordered

| Field | Type | Notes |
|-------|------|-------|
| `window` | FK → PreorderWindow | |
| `name` | CharField | Name of product |
| `unit_price` | DecimalField | Unit price of product |
| `product` | FK → Product | |
| `limit` | IntegerField | Max number of this item that can be ordered across all orders |

---

### `Preorder`
| Field | Type | Notes |
|-------|------|-------|
| `window` | FK → PreorderWindow | |
| `customer_name` | CharField | |
| `customer_email` | EmailField | |
| `customer_phone` | CharField (optional) | |
| `created_at` | DateTimeField (auto) | |
| `status` | CharField | `pending_payment` / `confirmed` / `fulfilled` / `canceled` |
| `stripe_payment_intent_id` | CharField (unique) | |
| `stripe_payment_status` | CharField | Mirror of Stripe's status |
| `total` | DecimalField | Snapshot total at time of order |

**Note:** Orders are only confirmed after Stripe webhook confirms payment. `pending_payment` orders that aren't paid within ~30 minutes should be expired and not count against the limit.

---

### `PreorderItem`
| Field | Type | Notes |
|-------|------|-------|
| `order` | FK → Preorder | |
| `product_listing` | FK → PreorderListing | Listing with price and name |
| `quantity` | IntegerField | |

---

### `CustomOrderRequest`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField | |
| `email` | EmailField | |
| `request_description` | TextField | |
| `requested_pickup_date` | DateTimeField | |
| `delivery_details` | TextField (optional) | |
| `submitted_at` | DateTimeField (auto) | |
| `status` | CharField | `new` / `in_review` / `accepted` / `declined` / `complete` |

---

## API Endpoints

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/mailing-list/subscribe/` | Subscribe email to mailing list |
| `GET` | `/api/mailing-list/unsubscribe/<token>/` | One-click unsubscribe via email link |
| `POST` | `/api/guinea-pigs/` | Sign up as guinea pig |
| `GET` | `/api/guinea-pigs/unsubscribe/<token>/` | One-click unsubscribe |
| `GET` | `/api/products/` | List available products |
| `GET` | `/api/order-window/current/` | Get the current open window (or 404 if closed) |
| `POST` | `/api/orders/` | Create an order, returns Stripe client secret |
| `GET` | `/api/orders/<id>/status/` | Poll order status (for post-payment confirmation page) |
| `POST` | `/api/custom-orders/` | Submit a custom order request |
| `GET` | `/api/guinea-pig-drops/<id>/` | View a drop (linked from email) |
| `POST` | `/api/guinea-pig-drops/<id>/claim/` | Claim a slot on a drop |
| `PATCH` | `/api/guinea-pig-drops/<id>/claim/` | Cancel a claim |

### Admin
Admin functionality (managing orders, custom orders, guinea pig drops, mailing list) is handled via the Django admin UI at `/admin/`. No custom admin API endpoints are needed.

---

## Checkout Flow

1. Frontend calls `GET /api/order-window/current/` — if 404, show "orders closed" UI
2. User builds cart, submits to `POST /api/orders/`
3. Backend validates:
   - Order window is open
   - Confirmed order count for each product is below `limit`
   - All products are still available
4. Backend creates `Preorder` with status `pending_payment`, creates a Stripe `PaymentIntent`, returns the `client_secret` to the frontend
5. Frontend uses Stripe.js to collect payment
6. Stripe sends webhook to `POST /api/stripe/webhook/`
7. Webhook handler updates `Preorder.status` to `confirmed` and sends confirmation email
8. Frontend polls `GET /api/orders/<id>/status/` to show confirmation

**Capacity enforcement:** The order limit check in step 3 counts only `confirmed` orders (not `pending_payment`). A short expiry (30 min) on `pending_payment` orders prevents them from blocking slots indefinitely.

---

## Guinea Pig Drop Flow

1. Admin creates a `GuineaPigDrop` via Django admin or `POST /api/admin/guinea-pig-drops/`
2. Creating the drop triggers a Celery task to email all active guinea pigs
3. Email contains a link to `/guinea-pigs/drops/<id>/` with their `auth_token` for auth (no login needed)
4. Guinea pig picks a time slot and submits — creates a `GuineaPigClaim`
5. If `total_slots` is already reached, return 409 (slots full)
6. Confirmation email sent to the guinea pig with their pickup time
7. Guinea pig can cancel via a link in their confirmation email

---

## Email Events (SendGrid)

| Trigger | Recipient | Content |
|---------|-----------|---------|
| Order confirmed | Customer | Order summary, pickup time |
| Custom order received | Customer | Confirmation + timeline |
| Custom order accepted/declined | Customer | Status update |
| Guinea pig drop available | All active guinea pigs | Drop details + claim link |
| Guinea pig claim confirmed | Guinea pig | Pickup time confirmation |
| Guinea pig claim canceled | Guinea pig | Cancellation confirmation |
| Mailing list welcome | New subscriber | Welcome message |

---

## Open Questions

- **Stripe fees:** Are you absorbing them or passing them to the customer?
- **Guinea pig slots:** Are pickup slots fixed time windows (e.g. 6–6:30, 6:30–7) or just a loose time the guinea pig picks?
- **Order limit type:** Is the limit per number of *orders* or per number of *items*? A limit on orders is simpler; a limit on items is more accurate to capacity.
- **Custom order payment:** Is a deposit collected upfront via Stripe, or is it pay-on-pickup?
