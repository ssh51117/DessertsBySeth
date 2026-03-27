# TODO
## Frontend:
- make loading better
- make other pages
- make buttons clickable

## Backend:
  2. Validation — add validate() methods to serializers as you implement each view, since you'll know exactly what needs checking
  GuineaPigClaimView.post:
  - Guinea pig tries to claim a drop they've already claimed (not cancelled) — unique_together will catch this at the database level
  but you should catch it explicitly and return a clean error before hitting the DB
  - Drop's available_until has passed — should check that the drop is still open before allowing a claim

  GuineaPigMembershipView.post:
  - Email already registered as a guinea pig — unique=True on the model will catch it but again worth a clean error message

  MailingListView.post:
  - Same — email already subscribed should return a clean error rather than a raw DB constraint error

  PreorderView.post:
  - Order window is no longer active — should check preorder_window.active before proceeding
  - items is empty — someone submits an order with no items
  - An item references a listing that doesn't belong to the submitted window — a malformed request could reference a listing from a
  different window
  - Quantity of zero or negative for an item

  GuineaPigClaimView.patch:
  - Trying to cancel an already cancelled claim — should check claim.cancelled before setting it again

  PreorderView generally:
  - Race condition on capacity — two requests could pass the capacity check simultaneously and both succeed, slightly exceeding the
  limit. For your scale this is unlikely to matter, but a database-level transaction would fully prevent it.
  3. Stripe integration — the checkout view is more complex and depends on the basic views working first
  4. Celery + email — async tasks for notifications, done last since they don't block the core functionality

# Frontend
requirements:
- landing page
- menu
- ordering
- schedule
- contact
- recipes maybe
## pages:
customer: 
- landing
- menu
- cart
- checkout
- contact
- tracking
- about
admin
- add/edit products
- update inventory
- view orders
- mark orders completed
# Backend
need:
- data store of orders
- payment processing
- email / text reminders

# Summary
next.js
django REST
postrgreSQL

host on aws
payments with stripe